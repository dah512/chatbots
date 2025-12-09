# Pain Management Support Group Platform
## Complete Technical and Programming Manual

**Version 1.0**

---

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Development Environment Setup](#development-environment-setup)
5. [Database Architecture](#database-architecture)
6. [Backend API Documentation](#backend-api-documentation)
7. [RAG System Implementation](#rag-system-implementation)
8. [Assessment and Analytics](#assessment-and-analytics)
9. [Frontend Development](#frontend-development)
10. [Deployment](#deployment)
11. [Security and Compliance](#security-and-compliance)
12. [Testing](#testing)
13. [Maintenance and Monitoring](#maintenance-and-monitoring)
14. [Troubleshooting](#troubleshooting)
15. [Contributing Guidelines](#contributing-guidelines)
16. [API Reference](#api-reference)

---

## Introduction

### Purpose

This technical manual provides comprehensive documentation for developers, DevOps engineers, and technical facilitators working on the Pain Management Support Group platform.

### Audience

- **Backend Developers**: Python/FastAPI development
- **Frontend Developers**: React/TypeScript development
- **DevOps Engineers**: Deployment and infrastructure
- **Data Scientists**: Analytics and research
- **Technical Facilitators**: Platform administration

### Document Conventions

```python
# Code blocks show working examples
def example_function():
    pass
```

**Bold text**: Important concepts or warnings
*Italic text*: File paths or variable names
`inline code`: Commands or code snippets

---

## System Architecture

### High-Level Overview

```
┌─────────────────┐
│   React Frontend│
│   (Port 3000)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Backend│◄───┐
│   (Port 8000)   │    │
└────┬────┬───┬───┘    │
     │    │   │        │
     │    │   │    ┌───┴─────┐
     │    │   │    │ Celery  │
     │    │   │    │ Worker  │
     │    │   │    └───┬─────┘
     │    │   │        │
     ▼    ▼   ▼        ▼
┌────────┐┌──────┐┌────────┐
│Postgres││Redis ││Pinecone│
│  DB    ││Cache ││/Chroma │
└────────┘└──────┘└────────┘
```

### Component Description

**Frontend (React):**
- User interface for patients and facilitators
- State management with Context API/Redux
- Real-time updates
- Responsive design

**Backend (FastAPI):**
- RESTful API server
- Authentication and authorization
- Business logic
- Database operations
- RAG orchestration

**Database (PostgreSQL):**
- User data
- Curriculum content
- Pain logs and assessments
- Discussion forums

**Cache (Redis):**
- Session storage
- API response caching
- Rate limiting
- Celery task queue

**Vector Database (Pinecone/ChromaDB):**
- Document embeddings
- Semantic search
- RAG context retrieval

**Background Workers (Celery):**
- Email notifications
- Report generation
- Document processing
- Scheduled tasks

### Data Flow

**User Authentication Flow:**
```
1. User submits credentials → Frontend
2. Frontend → POST /api/v1/auth/login → Backend
3. Backend verifies credentials → Database
4. Backend generates JWT token
5. Backend → Token → Frontend
6. Frontend stores token
7. Frontend includes token in subsequent requests
```

**RAG Query Flow:**
```
1. User asks question → Frontend
2. Frontend → POST /api/v1/rag/query → Backend
3. Backend → Embedding Generation → OpenAI API
4. Backend → Similarity Search → Vector DB
5. Vector DB → Top K chunks → Backend
6. Backend → LLM with context → OpenAI/Claude API
7. LLM → Generated answer → Backend
8. Backend → Save conversation → Database
9. Backend → Response with sources → Frontend
```

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Programming language |
| FastAPI | 0.109+ | Web framework |
| SQLAlchemy | 2.0+ | ORM |
| Pydantic | 2.5+ | Data validation |
| PostgreSQL | 15+ | Primary database |
| Redis | 7+ | Cache and queue |
| Celery | 5.3+ | Background tasks |
| LangChain | 0.1+ | RAG orchestration |
| OpenAI API | 1.10+ | LLM and embeddings |
| Pinecone | 3.0+ | Vector database (option 1) |
| ChromaDB | 0.4+ | Vector database (option 2) |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18+ | UI framework |
| TypeScript | 5+ | Type safety |
| React Router | 6+ | Routing |
| Axios | 1+ | HTTP client |
| Chart.js | 4+ | Visualizations |
| TailwindCSS | 3+ | Styling |
| Material-UI | 5+ | Component library |

### DevOps

| Technology | Version | Purpose |
|------------|---------|---------|
| Docker | 24+ | Containerization |
| Docker Compose | 2+ | Orchestration (dev) |
| GitHub Actions | - | CI/CD |
| Nginx | 1.25+ | Reverse proxy |

### Analytics

| Technology | Version | Purpose |
|------------|---------|---------|
| Pandas | 2.1+ | Data analysis |
| NumPy | 1.26+ | Numerical computing |
| R | 4.3+ | Statistical analysis |
| ggplot2 | 3.4+ | Visualizations |

---

## Development Environment Setup

### Prerequisites

Before starting, ensure you have:
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 15 or higher
- Redis 7 or higher
- Docker and Docker Compose (recommended)
- Git

### Initial Setup

#### 1. Clone Repository

```bash
git clone https://github.com/your-org/pain-management-support-group.git
cd pain-management-support-group
```

#### 2. Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here
SECRET_KEY=generate-secure-random-key
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pain_management

# Optional (for Pinecone)
PINECONE_API_KEY=your-key
PINECONE_ENVIRONMENT=us-west1-gcp
USE_PINECONE=true
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### 3. Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

**Access Points:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000
- PgAdmin: http://localhost:5050 (dev mode)

#### 4. Manual Setup (Alternative)

**Backend:**

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb pain_management

# Run migrations
alembic upgrade head

# Seed data (optional)
python scripts/seed_data.py

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Redis:**

```bash
# macOS
brew install redis
brew services start redis

# Linux
sudo apt-get install redis-server
sudo systemctl start redis

# Verify
redis-cli ping  # Should return PONG
```

**Celery Worker:**

```bash
cd backend
celery -A backend.tasks worker --loglevel=info
```

### Verify Installation

```bash
# Test backend
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","app":"Pain Management Support Group API","version":"1.0.0"}

# Test database connection
docker-compose exec backend python -c "from backend.models.base import engine; print(engine.connect())"

# Test Redis
docker-compose exec redis redis-cli ping
```

---

## Database Architecture

### Schema Overview

The database consists of 12 main tables organized into logical groups:

**User Management:**
- `users`

**Curriculum:**
- `weeks`
- `sessions`
- `session_content`

**Assessments:**
- `assessments`
- `assessment_questions`
- `assessment_submissions`
- `assessment_answers`

**Pain Tracking:**
- `pain_logs`

**Progress:**
- `progress_tracking`

**Social:**
- `discussion_posts`
- `discussion_replies`

**Resources:**
- `resources`

**AI/RAG:**
- `rag_conversations`
- `rag_messages`

### Entity Relationship Diagram

```
users
  │
  ├─── pain_logs (1:N)
  ├─── assessment_submissions (1:N)
  │    └─── assessment_answers (1:N)
  │         └─── assessment_questions (N:1)
  ├─── progress_tracking (1:N)
  │    └─── sessions (N:1)
  ├─── discussion_posts (1:N)
  │    └─── discussion_replies (1:N)
  └─── rag_conversations (1:N)
       └─── rag_messages (1:N)

weeks
  ├─── sessions (1:N)
  │    └─── session_content (1:N)
  └─── assessments (1:N)
       └─── assessment_questions (1:N)
```

### Key Tables

#### users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'patient',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    primary_pain_condition VARCHAR(200),
    pain_conditions TEXT,
    current_medications TEXT,
    enrollment_date TIMESTAMP WITH TIME ZONE,
    program_start_date TIMESTAMP WITH TIME ZONE,
    current_week INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

#### pain_logs

```sql
CREATE TABLE pain_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    pain_level INTEGER NOT NULL CHECK (pain_level >= 0 AND pain_level <= 10),
    pain_locations TEXT NOT NULL,
    pain_quality TEXT,
    activity_before_pain TEXT,
    medications_taken TEXT,
    non_med_strategies TEXT,
    sleep_quality INTEGER CHECK (sleep_quality >= 0 AND sleep_quality <= 10),
    fatigue_level INTEGER CHECK (fatigue_level >= 0 AND fatigue_level <= 10),
    anxiety_level INTEGER CHECK (anxiety_level >= 0 AND anxiety_level <= 10),
    function_level INTEGER CHECK (function_level >= 0 AND function_level <= 10),
    notes TEXT,
    log_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_pain_logs_user_id ON pain_logs(user_id);
CREATE INDEX idx_pain_logs_log_date ON pain_logs(log_date);
```

### Migrations

We use Alembic for database migrations.

**Create Migration:**

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

**Apply Migrations:**

```bash
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade one revision
alembic downgrade -1

# View history
alembic history

# Current revision
alembic current
```

**Example Migration:**

```python
# migrations/versions/001_initial.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        # ... more columns
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

def downgrade():
    op.drop_table('users')
```

### Database Backup

**Manual Backup:**

```bash
# Backup
pg_dump -U postgres pain_management > backup.sql

# With Docker
docker-compose exec postgres pg_dump -U postgres pain_management > backup.sql

# Restore
psql -U postgres pain_management < backup.sql
```

**Automated Backup (add to cron):**

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
docker-compose exec -T postgres pg_dump -U postgres pain_management | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

---

## Backend API Documentation

### Project Structure

```
backend/
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User management
│   │   ├── curriculum.py    # Curriculum access
│   │   ├── assessments.py   # Tests and quizzes
│   │   ├── pain_tracking.py # Pain logs
│   │   ├── progress.py      # Progress tracking
│   │   ├── discussions.py   # Forums
│   │   ├── resources.py     # Educational materials
│   │   └── rag.py          # AI Q&A
│   └── middleware/
│       └── auth.py          # Auth middleware
├── models/
│   ├── __init__.py
│   ├── base.py             # Base model and DB session
│   ├── user.py
│   ├── curriculum.py
│   ├── assessment.py
│   ├── pain_log.py
│   ├── progress.py
│   ├── discussion.py
│   ├── resource.py
│   └── rag.py
├── controllers/
│   └── ...                 # Business logic (optional layer)
├── services/
│   ├── rag_service.py      # RAG implementation
│   ├── email_service.py    # Email notifications
│   └── assessment_service.py
├── utils/
│   ├── security.py         # Password hashing, tokens
│   └── helpers.py
├── config/
│   └── settings.py         # Configuration
├── tasks/
│   └── celery_tasks.py     # Background tasks
├── main.py                 # FastAPI application
└── requirements.txt
```

### Authentication System

**Implementation:** `backend/api/routes/auth.py`

#### Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

#### JWT Tokens

```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

#### Protected Routes

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

### Creating New Endpoints

**Step 1: Define Pydantic Schemas**

```python
# api/schemas/pain_log.py
from pydantic import BaseModel, Field
from datetime import datetime

class PainLogCreate(BaseModel):
    pain_level: int = Field(..., ge=0, le=10)
    pain_locations: str
    sleep_quality: int | None = Field(None, ge=0, le=10)
    notes: str | None = None

class PainLogResponse(BaseModel):
    id: int
    user_id: int
    pain_level: int
    log_date: datetime

    class Config:
        from_attributes = True
```

**Step 2: Create Route Handler**

```python
# api/routes/pain_tracking.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/log", response_model=PainLogResponse)
def create_pain_log(
    pain_log: PainLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new pain log entry"""
    new_log = PainLog(
        user_id=current_user.id,
        log_date=datetime.utcnow(),
        **pain_log.dict()
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/history", response_model=List[PainLogResponse])
def get_pain_history(
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's pain log history"""
    logs = db.query(PainLog).filter(
        PainLog.user_id == current_user.id
    ).order_by(PainLog.log_date.desc()).limit(limit).all()
    return logs
```

**Step 3: Register Router**

```python
# main.py
from api.routes import pain_tracking

app.include_router(
    pain_tracking.router,
    prefix="/api/v1/pain",
    tags=["Pain Tracking"]
)
```

### Error Handling

**Custom Exception Classes:**

```python
# utils/exceptions.py
from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
```

**Global Exception Handler:**

```python
# main.py
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

### Request Validation

FastAPI uses Pydantic for automatic validation:

```python
from pydantic import BaseModel, validator, Field
from typing import List

class PainLogCreate(BaseModel):
    pain_level: int = Field(..., ge=0, le=10, description="Pain level 0-10")
    pain_locations: List[str]

    @validator('pain_locations')
    def validate_locations(cls, v):
        valid_locations = ['lower_back', 'neck', 'shoulder', 'hip', 'knee']
        if not all(loc in valid_locations for loc in v):
            raise ValueError('Invalid pain location')
        return v
```

### Database Transactions

```python
from sqlalchemy.orm import Session
from contextlib import contextmanager

@contextmanager
def transaction(db: Session):
    """Context manager for database transactions"""
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Usage
with transaction(db) as session:
    user = User(email="test@example.com", username="testuser")
    session.add(user)
    pain_log = PainLog(user_id=user.id, pain_level=5)
    session.add(pain_log)
```

### Pagination

```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

def paginate(query, page: int = 1, page_size: int = 20):
    """Paginate SQLAlchemy query"""
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )

# Usage
@router.get("/pain-logs")
def get_pain_logs(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    query = db.query(PainLog)
    return paginate(query, page, page_size)
```

---

## RAG System Implementation

### Architecture

The RAG (Retrieval-Augmented Generation) system enables AI-powered Q&A by:
1. Embedding medical literature into a vector database
2. Retrieving relevant context based on user queries
3. Generating informed answers with citations

### Implementation: `backend/services/rag_service.py`

#### Key Components

**1. Document Ingestion**

```python
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

async def ingest_document(self, file_content: bytes, filename: str):
    """Ingest a document into the vector store"""

    # Save temporary file
    temp_path = f"/tmp/{filename}"
    with open(temp_path, "wb") as f:
        f.write(file_content)

    # Load document
    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)

    # Add metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "source": filename,
            "chunk_index": i,
            "document_id": hashlib.md5(file_content).hexdigest()
        })

    # Add to vector store
    self.vector_store.add_documents(chunks)

    os.remove(temp_path)
    return {"chunks_created": len(chunks)}
```

**2. Query Processing**

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

async def query(self, query: str, conversation_history: List[Dict] = None):
    """Query the knowledge base"""

    # Create retriever
    retriever = self.vector_store.as_retriever(
        search_kwargs={"k": settings.TOP_K_RESULTS}
    )

    # Create memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Add conversation history
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
        return_source_documents=True
    )

    # Get response
    result = qa_chain({"question": query})

    # Extract sources
    sources = [
        {
            "content": doc.page_content[:200],
            "source": doc.metadata.get("source"),
            "chunk_index": doc.metadata.get("chunk_index")
        }
        for doc in result.get("source_documents", [])
    ]

    return {
        "response": result["answer"],
        "sources": sources
    }
```

**3. Custom Prompts**

```python
from langchain.prompts import PromptTemplate

PAIN_MANAGEMENT_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert pain management educator for a chronic pain support group.

Your role is to provide accurate, evidence-based information about:
- Pain physiology and anatomy
- Medication mechanisms and safety
- Alternative pain management techniques
- Nutrition and lifestyle factors
- Self-advocacy and patient rights

Use the following context to answer the question. If the answer is not in the context,
say so and provide general guidance while recommending they discuss with their healthcare provider.

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
```

### Vector Database Setup

**Option 1: Pinecone (Cloud)**

```python
import pinecone
from langchain.vectorstores import Pinecone as LangchainPinecone

# Initialize
pinecone.init(
    api_key=settings.PINECONE_API_KEY,
    environment=settings.PINECONE_ENVIRONMENT
)

# Create index
if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(
        name=settings.PINECONE_INDEX_NAME,
        dimension=3072,  # text-embedding-3-large
        metric="cosine"
    )

# Create vector store
vector_store = LangchainPinecone.from_existing_index(
    index_name=settings.PINECONE_INDEX_NAME,
    embedding=embeddings
)
```

**Option 2: ChromaDB (Local)**

```python
import chromadb
from langchain.vectorstores import Chroma

# Initialize client
client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)

# Create vector store
vector_store = Chroma(
    client=client,
    collection_name="pain_management_docs",
    embedding_function=embeddings
)
```

### Embedding Generation

```python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY,
    model=settings.OPENAI_EMBEDDING_MODEL  # text-embedding-3-large
)

# Generate embedding
text = "How do NSAIDs reduce inflammation?"
embedding = embeddings.embed_query(text)
# Returns: List[float] with 3072 dimensions
```

### Testing RAG System

```python
# Test document ingestion
with open("test_document.pdf", "rb") as f:
    content = f.read()

result = await rag_service.ingest_document(content, "test_document.pdf")
print(f"Created {result['chunks_created']} chunks")

# Test query
response = await rag_service.query(
    query="What are the side effects of NSAIDs?",
    conversation_history=[]
)

print(f"Answer: {response['response']}")
print(f"Sources: {response['sources']}")
```

### Monitoring RAG Performance

```python
# Track query metrics
import time

start_time = time.time()
response = await rag_service.query(query)
response_time = (time.time() - start_time) * 1000

# Log metrics
logger.info(f"RAG Query: {query[:50]}... | Response time: {response_time}ms | Sources: {len(response['sources'])}")

# Store in database for analysis
metric = RAGMetric(
    query=query,
    response_time_ms=response_time,
    chunks_retrieved=len(response['sources']),
    model_used=settings.OPENAI_MODEL
)
db.add(metric)
db.commit()
```

---

## Assessment and Analytics

### Python Assessment System

**Location:** `assessments/python/assessment_generator.py`

#### Creating Assessments

```python
from assessments.python.assessment_generator import AssessmentGenerator

# Initialize generator
generator = AssessmentGenerator()

# Generate Week 1 pre-test
pretest = generator.generate_assessment(
    week_number=1,
    assessment_type="pre_test",
    num_questions=15
)

# Export to JSON
generator.export_to_json(pretest, "week1_pretest.json")

# Score assessment
user_answers = {
    "w1_q1": "B",
    "w1_q2": "A",
    # ... more answers
}

results = generator.score_assessment(pretest, user_answers)
print(f"Score: {results['percentage']}%")
print(f"Passed: {results['passed']}")
```

#### Adding New Questions

```python
from assessments.python.assessment_generator import Question, QuestionType, QuestionDifficulty

# Add to question bank
new_question = Question(
    id="w2_q5",
    text="What is the maximum daily dose of acetaminophen for adults?",
    type=QuestionType.MULTIPLE_CHOICE,
    options=[
        "A. 1000mg",
        "B. 2000mg",
        "C. 3000-4000mg",
        "D. 6000mg"
    ],
    correct_answer="C",
    explanation="The maximum recommended daily dose is 3000-4000mg to avoid liver toxicity.",
    topic="Medication Safety",
    difficulty=QuestionDifficulty.EASY,
    points=1
)

# Add to question bank
generator.question_bank[2].append(new_question)
```

### Python Analytics System

**Location:** `assessments/python/outcome_analytics.py`

#### Generating Patient Reports

```python
from assessments.python.outcome_analytics import OutcomeAnalytics

analytics = OutcomeAnalytics()

# Generate comprehensive report
report = analytics.generate_patient_report(
    user_id=user_id,
    pain_logs=pain_logs_list,
    assessment_scores={
        1: {"pre_score": 60, "post_score": 85},
        2: {"pre_score": 65, "post_score": 90},
        # ... more weeks
    },
    program_completion=True
)

# Export
analytics.export_report_to_json(report, f"patient_{user_id}_report.json")
analytics.export_report_to_csv(report, f"patient_{user_id}_summary.csv")

# Access results
print(f"Pain reduction: {report['changes']['pain_level']['absolute_change']}")
print(f"Clinically significant: {report['clinically_significant']['pain_level']}")
```

### R Statistical Analysis

**Location:** `assessments/r/statistical_analysis.R`

#### Running Analysis

```bash
cd assessments/r

# Run full analysis
Rscript statistical_analysis.R --input ../data/patient_outcomes.csv

# Or from R console
source("statistical_analysis.R")
results <- main("../data/patient_outcomes.csv")
```

#### Key Functions

**Paired T-Tests:**

```r
# Perform paired t-tests
ttests <- perform_paired_ttests(data)

# Results include:
# - n_pairs: number of complete pairs
# - mean_baseline: average at baseline
# - mean_endpoint: average at week 8
# - t_statistic, p_value
# - cohens_d: effect size
```

**Longitudinal Models:**

```r
# Fit mixed-effects models
models <- fit_longitudinal_models(data)

# Access results
summary(models$models$pain_level)
models$summaries$pain_level$slope  # Change per week
```

**Generate Report:**

```r
# Generate HTML report with plots
results <- generate_statistical_report(
    data,
    output_path = "reports/statistical_report.html"
)
```

### Integrating Analytics with API

```python
# api/routes/analytics.py
from fastapi import APIRouter, Depends
from assessments.python.outcome_analytics import OutcomeAnalytics

router = APIRouter()

@router.get("/patient/{user_id}/report")
async def get_patient_report(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate patient outcome report"""

    # Authorization check
    if current_user.role not in ["admin", "instructor"] and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Get data
    pain_logs = db.query(PainLog).filter(PainLog.user_id == user_id).all()

    # Generate report
    analytics = OutcomeAnalytics()
    report = analytics.generate_patient_report(
        user_id=user_id,
        pain_logs=[log.__dict__ for log in pain_logs],
        assessment_scores={},  # Get from database
        program_completion=True
    )

    return report
```

---

## Frontend Development

### Project Structure (React)

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/          # Reusable components
│   │   ├── auth/            # Login, register
│   │   ├── dashboard/       # Patient dashboard
│   │   ├── curriculum/      # Week/session viewers
│   │   ├── assessments/     # Test interfaces
│   │   ├── pain-tracking/   # Pain log forms
│   │   ├── chat/           # AI chatbot
│   │   └── forums/         # Discussion forums
│   ├── pages/
│   │   ├── HomePage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── WeekPage.tsx
│   │   └── ...
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── usePainLogs.ts
│   │   └── ...
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   └── ThemeContext.tsx
│   ├── services/
│   │   └── api.ts          # API client
│   ├── types/
│   │   └── index.ts        # TypeScript types
│   ├── utils/
│   │   └── helpers.ts
│   ├── styles/
│   │   └── globals.css
│   ├── App.tsx
│   └── index.tsx
├── package.json
└── tsconfig.json
```

### API Client Setup

```typescript
// src/services/api.ts
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/api/v1/auth/login', { username, password }),
  register: (data: RegisterData) =>
    api.post('/api/v1/auth/register', data),
};

export const painAPI = {
  createLog: (data: PainLogData) =>
    api.post('/api/v1/pain/log', data),
  getHistory: (limit: number = 30) =>
    api.get(`/api/v1/pain/history?limit=${limit}`),
};
```

### Authentication Hook

```typescript
// src/hooks/useAuth.ts
import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    // Check for stored token
    const token = localStorage.getItem('access_token');
    if (token) {
      // Fetch user info
      fetchCurrentUser();
    }
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authAPI.login(username, password);
    localStorage.setItem('access_token', response.data.access_token);
    await fetchCurrentUser();
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/api/v1/auth/me');
      setUser(response.data);
    } catch (error) {
      logout();
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

### Component Example: Pain Log Form

```typescript
// src/components/pain-tracking/PainLogForm.tsx
import React, { useState } from 'react';
import { painAPI } from '../../services/api';

export const PainLogForm: React.FC = () => {
  const [painLevel, setPainLevel] = useState(5);
  const [locations, setLocations] = useState<string[]>([]);
  const [notes, setNotes] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await painAPI.createLog({
        pain_level: painLevel,
        pain_locations: JSON.stringify(locations),
        notes,
      });

      alert('Pain log saved!');
      // Reset form or redirect
    } catch (error) {
      console.error('Error saving pain log:', error);
      alert('Failed to save pain log');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="pain-log-form">
      <div className="form-group">
        <label>Pain Level (0-10)</label>
        <input
          type="range"
          min="0"
          max="10"
          value={painLevel}
          onChange={(e) => setPainLevel(Number(e.target.value))}
        />
        <span>{painLevel}</span>
      </div>

      <div className="form-group">
        <label>Pain Locations</label>
        <select
          multiple
          value={locations}
          onChange={(e) => {
            const selected = Array.from(e.target.selectedOptions, option => option.value);
            setLocations(selected);
          }}
        >
          <option value="lower_back">Lower Back</option>
          <option value="neck">Neck</option>
          <option value="shoulder">Shoulder</option>
          <option value="hip">Hip</option>
          <option value="knee">Knee</option>
        </select>
      </div>

      <div className="form-group">
        <label>Notes</label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={4}
        />
      </div>

      <button type="submit">Save Pain Log</button>
    </form>
  );
};
```

---

## Deployment

### Production Deployment Checklist

**Pre-Deployment:**

☐ Environment variables set correctly
☐ Database migrations run
☐ SSL certificate configured
☐ Domain DNS configured
☐ Backup strategy in place
☐ Monitoring tools configured
☐ Security audit completed
☐ Load testing completed

### Docker Production Build

**Backend Dockerfile:**

```dockerfile
# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Production docker-compose.yml:**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
    secrets:
      - postgres_password
    restart: always

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      DATABASE_URL: postgresql://postgres@postgres:5432/pain_management
    depends_on:
      - postgres
    restart: always

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    restart: always

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt

volumes:
  postgres_data:
```

### Nginx Configuration

```nginx
# nginx/nginx.conf
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name painmanagement.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name painmanagement.example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}
```

### CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /app/pain-management
            git pull
            docker-compose -f docker-compose.prod.yml up -d --build
            docker-compose exec backend alembic upgrade head
```

### Environment Variables (Production)

```bash
# Use secrets management (AWS Secrets Manager, Vault, etc.)
# Never commit .env to git

# Generate secure keys
openssl rand -base64 32

# Example .env.prod
SECRET_KEY=your-generated-secure-key
DATABASE_URL=postgresql://user:pass@db-host:5432/pain_management
OPENAI_API_KEY=sk-prod-key
PINECONE_API_KEY=prod-key
ENVIRONMENT=production
DEBUG=false
```

---

## Security and Compliance

### HIPAA Compliance Considerations

**Technical Safeguards:**

1. **Access Control**
   - Unique user authentication
   - Role-based access control
   - Automatic logout after inactivity
   - Emergency access procedures

2. **Audit Controls**
   - Log all PHI access
   - Tamper-proof logs
   - Regular audit reviews

3. **Integrity**
   - Data checksums
   - Digital signatures
   - Version control

4. **Transmission Security**
   - TLS 1.3 for all connections
   - VPN for admin access
   - Encrypted backups

**Implementation Example:**

```python
# Audit logging middleware
from fastapi import Request
import logging

audit_logger = logging.getLogger('audit')

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    # Log PHI access
    if '/api/v1/users/' in request.url.path or '/api/v1/pain/' in request.url.path:
        user = await get_current_user_from_request(request)
        audit_logger.info(
            f"PHI_ACCESS | User: {user.id} | Endpoint: {request.url.path} | IP: {request.client.host}"
        )

    response = await call_next(request)
    return response
```

### Data Encryption

**At Rest:**

```python
from cryptography.fernet import Fernet

# Generate key (store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt sensitive data
def encrypt_field(data: str) -> bytes:
    return cipher.encrypt(data.encode())

def decrypt_field(encrypted_data: bytes) -> str:
    return cipher.decrypt(encrypted_data).decode()

# In model
class User(Base):
    ssn_encrypted = Column(LargeBinary)  # Store encrypted

    @property
    def ssn(self):
        return decrypt_field(self.ssn_encrypted) if self.ssn_encrypted else None

    @ssn.setter
    def ssn(self, value):
        self.ssn_encrypted = encrypt_field(value) if value else None
```

**In Transit:**

- Always use HTTPS (TLS 1.2+)
- Certificate pinning for mobile apps
- Encrypted WebSocket connections

### Input Validation and SQL Injection Prevention

```python
# SAFE - Using ORM
user = db.query(User).filter(User.email == email).first()

# UNSAFE - Raw SQL with string formatting (DON'T DO THIS)
# result = db.execute(f"SELECT * FROM users WHERE email = '{email}'")

# If raw SQL is necessary, use parameterized queries
result = db.execute(
    "SELECT * FROM users WHERE email = :email",
    {"email": email}
)
```

### XSS Prevention

```python
from fastapi.responses import HTMLResponse
from markupsafe import escape

@app.get("/user/{user_id}")
def get_user_profile(user_id: int):
    user = get_user(user_id)

    # Escape user input before displaying
    safe_bio = escape(user.bio)

    return HTMLResponse(f"<div>{safe_bio}</div>")
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/v1/pain/history")
@limiter.limit("10/minute")
def get_pain_history(request: Request):
    # Endpoint limited to 10 requests per minute per IP
    pass
```

### Password Requirements

```python
import re

def validate_password(password: str) -> bool:
    """
    Password must:
    - Be at least 12 characters
    - Contain uppercase and lowercase
    - Contain a number
    - Contain a special character
    """
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True
```

---

## Testing

### Backend Testing

**Test Structure:**

```
backend/tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── test_auth.py
├── test_users.py
├── test_pain_logs.py
├── test_assessments.py
└── test_rag.py
```

**Fixtures (conftest.py):**

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.base import Base
from backend.main import app
from fastapi.testclient import TestClient

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db_session():
    """Create test database session"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def client(db_session):
    """Create test client"""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def auth_token(client):
    """Create authenticated user and return token"""
    # Register user
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePassword123!",
        "first_name": "Test",
        "last_name": "User"
    })

    # Login
    response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "SecurePassword123!"
    })

    return response.json()["access_token"]
```

**Example Tests:**

```python
# tests/test_pain_logs.py
def test_create_pain_log(client, auth_token):
    """Test creating a pain log"""
    response = client.post(
        "/api/v1/pain/log",
        json={
            "pain_level": 5,
            "pain_locations": '["lower_back"]',
            "notes": "Test pain log"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["pain_level"] == 5
    assert "lower_back" in data["pain_locations"]

def test_get_pain_history(client, auth_token):
    """Test retrieving pain history"""
    # Create some logs first
    for i in range(5):
        client.post(
            "/api/v1/pain/log",
            json={"pain_level": i + 1, "pain_locations": '["knee"]'},
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    # Get history
    response = client.get(
        "/api/v1/pain/history?limit=10",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5

def test_unauthorized_access(client):
    """Test that endpoints require authentication"""
    response = client.get("/api/v1/pain/history")
    assert response.status_code == 401
```

**Running Tests:**

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_pain_logs.py

# Run specific test
pytest tests/test_pain_logs.py::test_create_pain_log

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Frontend Testing

```typescript
// src/components/__tests__/PainLogForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PainLogForm } from '../pain-tracking/PainLogForm';
import * as api from '../../services/api';

jest.mock('../../services/api');

describe('PainLogForm', () => {
  it('renders pain level slider', () => {
    render(<PainLogForm />);
    const slider = screen.getByRole('slider');
    expect(slider).toBeInTheDocument();
  });

  it('submits form with correct data', async () => {
    const mockCreate = jest.spyOn(api.painAPI, 'createLog');
    mockCreate.mockResolvedValue({ data: { id: 1 } });

    render(<PainLogForm />);

    const slider = screen.getByRole('slider');
    fireEvent.change(slider, { target: { value: '7' } });

    const submit = screen.getByText('Save Pain Log');
    fireEvent.click(submit);

    await waitFor(() => {
      expect(mockCreate).toHaveBeenCalledWith(
        expect.objectContaining({ pain_level: 7 })
      );
    });
  });
});
```

### Load Testing

```python
# tests/load_test.py
from locust import HttpUser, task, between

class PainManagementUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login before running tasks"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def view_dashboard(self):
        self.client.get("/api/v1/users/dashboard", headers=self.headers)

    @task(2)
    def view_pain_history(self):
        self.client.get("/api/v1/pain/history", headers=self.headers)

    @task(1)
    def create_pain_log(self):
        self.client.post(
            "/api/v1/pain/log",
            json={"pain_level": 5, "pain_locations": '["back"]'},
            headers=self.headers
        )
```

**Run load test:**

```bash
locust -f tests/load_test.py --host=http://localhost:8000
# Open http://localhost:8089 to configure and run
```

---

## Maintenance and Monitoring

### Logging

**Configuration:**

```python
# backend/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logging():
    # Create logger
    logger = logging.getLogger("pain_management")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging()
```

**Usage:**

```python
from backend.config.logging_config import logger

logger.info("User logged in", extra={"user_id": user.id})
logger.warning("High pain level reported", extra={"pain_level": 9, "user_id": user.id})
logger.error("Database connection failed", exc_info=True)
```

### Monitoring

**Health Check Endpoint:**

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }

    # Database check
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = "unhealthy"
        health_status["status"] = "unhealthy"
        logger.error(f"Database health check failed: {e}")

    # Redis check
    try:
        redis_client.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = "unhealthy"
        logger.error(f"Redis health check failed: {e}")

    # Vector DB check
    try:
        vector_store.similarity_search("test", k=1)
        health_status["checks"]["vector_db"] = "healthy"
    except Exception as e:
        health_status["checks"]["vector_db"] = "unhealthy"
        logger.error(f"Vector DB health check failed: {e}")

    return health_status
```

**Metrics Collection:**

```python
from prometheus_client import Counter, Histogram
import time

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    request_duration.observe(duration)

    return response
```

### Backup Strategy

**Automated Backups:**

```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
RETENTION_DAYS=30

# Database backup
docker-compose exec -T postgres pg_dump -U postgres pain_management | \
    gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Vector DB backup (ChromaDB)
tar -czf $BACKUP_DIR/chromadb_backup_$DATE.tar.gz rag/chromadb/

# Uploaded documents backup
tar -czf $BACKUP_DIR/documents_backup_$DATE.tar.gz rag/documents/

# Delete old backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/db_backup_$DATE.sql.gz s3://pain-management-backups/

echo "Backup completed: $DATE"
```

**Add to crontab:**

```bash
# Run daily at 2 AM
0 2 * * * /app/scripts/backup.sh >> /var/log/backup.log 2>&1
```

### Database Maintenance

```sql
-- Vacuum and analyze (run weekly)
VACUUM ANALYZE;

-- Rebuild indexes (run monthly)
REINDEX DATABASE pain_management;

-- Check for bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS external_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
```

---

## Troubleshooting

### Common Issues

#### Issue: Database Connection Errors

**Symptoms:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**

1. Check PostgreSQL is running:
```bash
docker-compose ps postgres
# or
pg_isready -h localhost -p 5432
```

2. Verify connection string:
```python
# Check .env file
DATABASE_URL=postgresql://user:password@host:5432/database
```

3. Check firewall/network:
```bash
telnet localhost 5432
```

4. Check logs:
```bash
docker-compose logs postgres
```

#### Issue: RAG Queries Failing

**Symptoms:**
```
Error: No documents found in vector store
```

**Solutions:**

1. Verify documents ingested:
```python
# Python console
from backend.services.rag_service import RAGService
rag = RAGService()
stats = await rag.get_stats()
print(stats["documents_indexed"])
```

2. Check vector DB connection:
```python
# For Pinecone
import pinecone
pinecone.init(api_key=settings.PINECONE_API_KEY, environment=settings.PINECONE_ENVIRONMENT)
print(pinecone.list_indexes())

# For ChromaDB
import chromadb
client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
print(client.list_collections())
```

3. Re-ingest documents:
```bash
docker-compose exec backend python scripts/ingest_documents.py
```

#### Issue: High Memory Usage

**Symptoms:**
- Slow response times
- Container crashes
- Out of memory errors

**Solutions:**

1. Check resource usage:
```bash
docker stats
```

2. Limit container memory:
```yaml
# docker-compose.yml
services:
  backend:
    mem_limit: 2g
    mem_reservation: 1g
```

3. Optimize database queries:
```python
# Use .options() for eager loading
users = db.query(User).options(
    joinedload(User.pain_logs)
).all()

# Add indexes
CREATE INDEX idx_pain_logs_user_date ON pain_logs(user_id, log_date);
```

4. Implement caching:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_week_content(week_id: int):
    return db.query(Week).filter(Week.id == week_id).first()
```

#### Issue: Slow API Responses

**Diagnostic Steps:**

1. Enable query logging:
```python
# settings.py
DB_ECHO = True  # Prints all SQL queries
```

2. Profile endpoints:
```python
import time
from functools import wraps

def profile(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"{func.__name__} took {duration:.2f}s")
        return result
    return wrapper

@router.get("/slow-endpoint")
@profile
async def slow_endpoint():
    # Your code here
    pass
```

3. Add database indexes:
```sql
-- Find slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Add index
CREATE INDEX idx_name ON table(column);
```

### Debug Mode

```python
# main.py
if settings.DEBUG:
    @app.middleware("http")
    async def debug_middleware(request: Request, call_next):
        logger.debug(f"Request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")

        response = await call_next(request)

        logger.debug(f"Response Status: {response.status_code}")
        return response
```

### Getting Help

1. **Check logs first:**
```bash
# All logs
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

2. **Check GitHub Issues:**
- Search existing issues
- Create new issue with:
  - Error messages
  - Steps to reproduce
  - Environment details
  - Log excerpts

3. **Stack Overflow:**
- Tag: `pain-management-platform`
- Include minimal reproducible example

---

## Contributing Guidelines

### Code Style

**Python (Backend):**

```bash
# Format with black
black backend/

# Lint with flake8
flake8 backend/ --max-line-length=100

# Type checking with mypy
mypy backend/
```

**Style Guide:**
- Follow PEP 8
- Max line length: 100 characters
- Use type hints
- Docstrings for all public functions

```python
def calculate_pain_change(baseline: float, current: float) -> dict:
    """
    Calculate change in pain level from baseline.

    Args:
        baseline: Initial pain level (0-10)
        current: Current pain level (0-10)

    Returns:
        Dictionary with absolute and percent change

    Raises:
        ValueError: If pain levels out of range
    """
    if not (0 <= baseline <= 10 and 0 <= current <= 10):
        raise ValueError("Pain levels must be between 0 and 10")

    absolute_change = current - baseline
    percent_change = (absolute_change / baseline * 100) if baseline != 0 else 0

    return {
        "absolute_change": absolute_change,
        "percent_change": percent_change
    }
```

**TypeScript (Frontend):**

```bash
# Format with prettier
prettier --write src/

# Lint with eslint
eslint src/ --ext .ts,.tsx
```

### Git Workflow

**Branch Naming:**
```
feature/add-user-dashboard
bugfix/fix-login-error
hotfix/critical-security-patch
docs/update-readme
```

**Commit Messages:**
```
feat: add pain tracking analytics endpoint
fix: resolve database connection timeout
docs: update API documentation
test: add unit tests for assessment scoring
refactor: extract RAG service methods
chore: update dependencies
```

**Pull Request Process:**

1. Create feature branch from `main`
2. Make changes with clear commits
3. Write/update tests
4. Update documentation
5. Run tests locally
6. Create PR with description:
   - What changed
   - Why it changed
   - How to test
7. Address review comments
8. Squash and merge

### Adding New Features

**Checklist:**

☐ Create issue describing feature
☐ Design database changes (if needed)
☐ Implement backend logic
☐ Add API endpoints
☐ Write tests (aim for >80% coverage)
☐ Update API documentation
☐ Implement frontend (if needed)
☐ Write user documentation
☐ Create migration (if database changed)
☐ Update CHANGELOG.md

---

## API Reference

### Authentication

#### POST /api/v1/auth/register
Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response: 201 Created**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "role": "patient"
}
```

#### POST /api/v1/auth/login
Login and receive access token.

**Request:**
```json
{
  "username": "username",
  "password": "SecurePassword123!"
}
```

**Response: 200 OK**
```json
{
  "access_token": "eyJhbGci....",
  "token_type": "bearer"
}
```

### Pain Tracking

#### POST /api/v1/pain/log
Create pain log entry.

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "pain_level": 7,
  "pain_locations": "[\"lower_back\", \"hip_right\"]",
  "sleep_quality": 4,
  "fatigue_level": 8,
  "notes": "Pain worse after sitting"
}
```

**Response: 200 OK**
```json
{
  "id": 123,
  "user_id": 1,
  "pain_level": 7,
  "log_date": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### GET /api/v1/pain/history
Get pain log history.

**Query Parameters:**
- `limit` (optional): Number of entries (default: 30)

**Response: 200 OK**
```json
[
  {
    "id": 123,
    "pain_level": 7,
    "log_date": "2024-01-15T10:30:00Z"
  },
  ...
]
```

### RAG / AI Q&A

#### POST /api/v1/rag/query
Ask AI a question.

**Request:**
```json
{
  "query": "What are the side effects of NSAIDs?",
  "conversation_id": null,
  "use_history": true
}
```

**Response: 200 OK**
```json
{
  "response": "NSAIDs can cause several side effects including...",
  "sources": [
    {
      "content": "NSAIDs inhibit COX enzymes...",
      "source": "medication_guide.pdf",
      "chunk_index": 5
    }
  ],
  "conversation_id": 45,
  "message_id": 90,
  "response_time_ms": 1250
}
```

### [Continue with remaining endpoints...]

---

## Appendix

### Glossary

**ADL**: Activities of Daily Living
**API**: Application Programming Interface
**CORS**: Cross-Origin Resource Sharing
**JWT**: JSON Web Token
**LLM**: Large Language Model
**MME**: Morphine Milligram Equivalent
**NSAID**: Nonsteroidal Anti-Inflammatory Drug
**ORM**: Object-Relational Mapping
**PHI**: Protected Health Information
**RAG**: Retrieval-Augmented Generation
**REST**: Representational State Transfer
**VAS**: Visual Analog Scale

### Useful Commands Cheat Sheet

```bash
# Docker
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose ps                 # List services
docker-compose logs -f backend    # Follow logs
docker-compose restart backend    # Restart service
docker-compose exec backend bash  # Shell into container

# Database
alembic upgrade head              # Run migrations
alembic revision -m "message"     # Create migration
pg_dump pain_management > backup.sql  # Backup
psql pain_management < backup.sql     # Restore

# Python
pip install -r requirements.txt   # Install dependencies
pytest                            # Run tests
pytest --cov                      # Run with coverage
black .                           # Format code
flake8 .                          # Lint code

# Git
git checkout -b feature/name      # Create branch
git add .                         # Stage changes
git commit -m "message"           # Commit
git push origin feature/name      # Push branch
git pull origin main              # Pull changes
```

---

**End of Technical Manual**

*Version 1.0 | Last Updated: 2024*

For questions or contributions, please refer to the Contributing Guidelines or open an issue on GitHub.
