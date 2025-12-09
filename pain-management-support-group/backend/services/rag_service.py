"""
RAG Service for document ingestion, embedding, and AI-powered Q&A
Uses LangChain for orchestration and Pinecone/ChromaDB for vector storage
"""
import os
import json
from typing import List, Dict, Optional, Any
from io import BytesIO
import hashlib

# LangChain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone, Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.prompts import PromptTemplate

# Document loaders
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader

# Vector DB clients
import pinecone
import chromadb

from backend.config.settings import settings
from loguru import logger


class RAGService:
    """
    RAG Service for managing document ingestion and AI Q&A

    This service handles:
    1. Document ingestion and chunking
    2. Embedding generation
    3. Vector database operations
    4. Retrieval-augmented generation for queries
    """

    def __init__(self):
        """Initialize RAG service with embeddings and vector store"""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_EMBEDDING_MODEL
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        # Initialize vector store
        if settings.USE_PINECONE and settings.PINECONE_API_KEY:
            self.vector_store = self._init_pinecone()
        else:
            self.vector_store = self._init_chromadb()

        # Initialize chat model
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.3,  # Lower temperature for more factual responses
        )

        # Create custom prompt for pain management context
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an expert pain management educator and healthcare AI assistant for a chronic pain support group program.

Your role is to provide accurate, evidence-based information about:
- Pain physiology and anatomy
- Medication mechanisms and safety
- Alternative pain management techniques
- Nutrition and lifestyle factors
- Self-advocacy and patient rights

Use the following context from educational materials to answer the question. If the answer is not in the context, say so and provide general guidance while recommending they discuss with their healthcare provider for medical advice.

Always:
1. Cite sources when using information from the context
2. Use accessible language (12th-grade reading level)
3. Show empathy for people living with chronic pain
4. Distinguish between educational information and medical advice
5. Encourage self-advocacy and shared decision-making

Context:
{context}

Question: {question}

Answer:"""
        )

    def _init_pinecone(self):
        """Initialize Pinecone vector store"""
        try:
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )

            # Create index if it doesn't exist
            if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                pinecone.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=3072,  # text-embedding-3-large dimension
                    metric="cosine"
                )

            vector_store = LangchainPinecone.from_existing_index(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )

            logger.info(f"Pinecone vector store initialized: {settings.PINECONE_INDEX_NAME}")
            return vector_store

        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            logger.info("Falling back to ChromaDB")
            return self._init_chromadb()

    def _init_chromadb(self):
        """Initialize ChromaDB vector store"""
        try:
            os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)

            client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

            vector_store = Chroma(
                client=client,
                collection_name="pain_management_docs",
                embedding_function=self.embeddings
            )

            logger.info(f"ChromaDB vector store initialized: {settings.CHROMA_DB_PATH}")
            return vector_store

        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise

    async def ingest_document(
        self,
        file_content: bytes,
        filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ingest a document into the vector store

        Args:
            file_content: Raw file bytes
            filename: Original filename
            metadata: Optional metadata to attach to chunks

        Returns:
            Dict with ingestion results
        """
        try:
            # Save temporary file
            temp_path = f"/tmp/{filename}"
            with open(temp_path, "wb") as f:
                f.write(file_content)

            # Load document based on file type
            file_ext = filename.split(".")[-1].lower()

            if file_ext == "pdf":
                loader = PyPDFLoader(temp_path)
            elif file_ext == "txt" or file_ext == "md":
                loader = TextLoader(temp_path)
            elif file_ext == "docx":
                loader = UnstructuredWordDocumentLoader(temp_path)
            else:
                raise ValueError(f"Unsupported file type: {file_ext}")

            # Load and split document
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)

            # Add metadata
            doc_id = hashlib.md5(file_content).hexdigest()
            for i, chunk in enumerate(chunks):
                chunk.metadata.update({
                    "source": filename,
                    "document_id": doc_id,
                    "chunk_index": i,
                    **(metadata or {})
                })

            # Add to vector store
            self.vector_store.add_documents(chunks)

            # Clean up
            os.remove(temp_path)

            logger.info(f"Ingested {filename}: {len(chunks)} chunks created")

            return {
                "document_id": doc_id,
                "filename": filename,
                "chunks_created": len(chunks),
                "status": "success"
            }

        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            raise

    async def query(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        top_k: int = None
    ) -> Dict[str, Any]:
        """
        Query the knowledge base with retrieval-augmented generation

        Args:
            query: User's question
            conversation_history: Previous messages in conversation
            top_k: Number of chunks to retrieve

        Returns:
            Dict with response, sources, and metadata
        """
        try:
            if top_k is None:
                top_k = settings.TOP_K_RESULTS

            # Retrieve relevant documents
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": top_k}
            )

            # Create conversational chain
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )

            # Add conversation history to memory
            if conversation_history:
                for msg in conversation_history:
                    if msg["role"] == "user":
                        memory.chat_memory.add_user_message(msg["content"])
                    else:
                        memory.chat_memory.add_ai_message(msg["content"])

            # Create chain
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                memory=memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": self.prompt_template}
            )

            # Get response
            result = qa_chain({"question": query})

            # Extract source information
            sources = []
            similarity_scores = []

            for doc in result.get("source_documents", []):
                source_info = {
                    "content": doc.page_content[:200] + "...",  # First 200 chars
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_index": doc.metadata.get("chunk_index"),
                }
                sources.append(source_info)

            response = {
                "response": result["answer"],
                "sources": sources,
                "similarity_scores": similarity_scores,
                "model_used": settings.OPENAI_MODEL,
                "chunks_retrieved": len(result.get("source_documents", []))
            }

            logger.info(f"Query processed: {query[:50]}... | Chunks: {len(sources)}")

            return response

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

    async def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform similarity search without LLM generation

        Args:
            query: Search query
            top_k: Number of results
            filter_metadata: Optional metadata filters

        Returns:
            List of relevant documents
        """
        try:
            if filter_metadata:
                results = self.vector_store.similarity_search(
                    query,
                    k=top_k,
                    filter=filter_metadata
                )
            else:
                results = self.vector_store.similarity_search(query, k=top_k)

            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in results
            ]

        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise

    async def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        try:
            # This is implementation-specific
            # For ChromaDB:
            if hasattr(self.vector_store, '_collection'):
                count = self.vector_store._collection.count()
            else:
                count = "Unknown (Pinecone)"

            return {
                "vector_store_type": "Pinecone" if settings.USE_PINECONE else "ChromaDB",
                "documents_indexed": count,
                "embedding_model": settings.OPENAI_EMBEDDING_MODEL,
                "llm_model": settings.OPENAI_MODEL
            }

        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
