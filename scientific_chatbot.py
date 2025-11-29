"""
Scientific Chatbot powered by Claude AI
A comprehensive chatbot for answering academic and professional queries across multiple scientific domains.
"""

import streamlit as st
import anthropic
import os
from datetime import datetime

# Scientific categories with descriptions and colors
SCIENTIFIC_CATEGORIES = {
    "Chemistry": {
        "icon": "🧪",
        "color": "#FF6B6B",
        "description": "Organic, inorganic, analytical chemistry, and chemical reactions",
        "resources": [
            {"name": "PubChem", "url": "https://pubchem.ncbi.nlm.nih.gov/"},
            {"name": "ChemSpider", "url": "http://www.chemspider.com/"},
        ]
    },
    "Physics": {
        "icon": "⚛️",
        "color": "#4ECDC4",
        "description": "Classical mechanics, quantum physics, thermodynamics, and relativity",
        "resources": [
            {"name": "Physics arXiv", "url": "https://arxiv.org/archive/physics"},
            {"name": "HyperPhysics", "url": "http://hyperphysics.phy-astr.gsu.edu/"},
        ]
    },
    "Biology": {
        "icon": "🧬",
        "color": "#95E1D3",
        "description": "Cell biology, genetics, ecology, and evolutionary biology",
        "resources": [
            {"name": "NCBI", "url": "https://www.ncbi.nlm.nih.gov/"},
            {"name": "BioRxiv", "url": "https://www.biorxiv.org/"},
        ]
    },
    "Biochemistry": {
        "icon": "🔬",
        "color": "#F38181",
        "description": "Molecular biology, enzymology, metabolism, and protein structures",
        "resources": [
            {"name": "PDB", "url": "https://www.rcsb.org/"},
            {"name": "KEGG", "url": "https://www.genome.jp/kegg/"},
        ]
    },
    "Physiology": {
        "icon": "❤️",
        "color": "#AA96DA",
        "description": "Human and animal physiology, organ systems, and homeostasis",
        "resources": [
            {"name": "Physiology.org", "url": "https://www.physiology.org/"},
            {"name": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
        ]
    },
    "Mathematics": {
        "icon": "📐",
        "color": "#FCBAD3",
        "description": "Algebra, calculus, statistics, and applied mathematics",
        "resources": [
            {"name": "Wolfram MathWorld", "url": "https://mathworld.wolfram.com/"},
            {"name": "arXiv Math", "url": "https://arxiv.org/archive/math"},
        ]
    },
    "Geology": {
        "icon": "🌍",
        "color": "#A8D8EA",
        "description": "Earth science, mineralogy, petrology, and geochemistry",
        "resources": [
            {"name": "USGS", "url": "https://www.usgs.gov/"},
            {"name": "Mindat", "url": "https://www.mindat.org/"},
        ]
    },
    "Electricity & Magnetism": {
        "icon": "⚡",
        "color": "#FFD93D",
        "description": "Electromagnetic theory, circuits, and electrodynamics",
        "resources": [
            {"name": "IEEE", "url": "https://www.ieee.org/"},
            {"name": "All About Circuits", "url": "https://www.allaboutcircuits.com/"},
        ]
    },
}


def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")


def get_claude_response(user_message, category=None):
    """Get response from Claude AI"""
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)

        # Create system prompt based on category
        system_prompt = """You are an expert scientific assistant specializing in providing accurate,
        detailed, and educational responses to academic and professional queries. Your expertise spans
        chemistry, physics, biochemistry, biology, physiology, mathematics, geology, and electricity & magnetism.

        Provide clear, comprehensive answers that are:
        - Scientifically accurate and well-researched
        - Appropriate for both elementary and advanced levels
        - Include relevant equations, formulas, or diagrams when helpful
        - Reference key concepts and principles
        - Educational and engaging
        """

        if category:
            category_info = SCIENTIFIC_CATEGORIES.get(category, {})
            system_prompt += f"\n\nThe user is currently interested in {category}: {category_info.get('description', '')}"

        # Call Claude API
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return message.content[0].text

    except anthropic.AuthenticationError:
        return "❌ Authentication error. Please check your API key."
    except anthropic.APIError as e:
        return f"❌ API error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"


def display_category_buttons():
    """Display category selection buttons"""
    st.markdown("### 🔬 Select a Scientific Domain")

    # Create 4 columns for category buttons
    cols = st.columns(4)

    for idx, (category, info) in enumerate(SCIENTIFIC_CATEGORIES.items()):
        with cols[idx % 4]:
            # Create a styled button using markdown and button
            if st.button(
                f"{info['icon']} {category}",
                key=f"cat_{category}",
                use_container_width=True
            ):
                st.session_state.selected_category = category
                st.rerun()

    # Display current category if selected
    if st.session_state.selected_category:
        category_info = SCIENTIFIC_CATEGORIES[st.session_state.selected_category]
        st.markdown(f"""
        <div style="background-color: {category_info['color']}22; padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4 style="color: {category_info['color']}; margin: 0;">
                {category_info['icon']} {st.session_state.selected_category}
            </h4>
            <p style="margin: 5px 0 0 0;">{category_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)


def display_resources_sidebar():
    """Display helpful resources in sidebar"""
    with st.sidebar:
        st.markdown("### 📚 Helpful Resources")

        if st.session_state.selected_category:
            category_info = SCIENTIFIC_CATEGORIES[st.session_state.selected_category]
            st.markdown(f"**{category_info['icon']} {st.session_state.selected_category}**")

            for resource in category_info['resources']:
                st.markdown(f"- [{resource['name']}]({resource['url']})")
        else:
            st.markdown("Select a category to see relevant resources")

        st.markdown("---")
        st.markdown("### 🌐 General Resources")
        st.markdown("""
        - [Google Scholar](https://scholar.google.com/)
        - [Wikipedia](https://www.wikipedia.org/)
        - [Khan Academy](https://www.khanacademy.org/)
        - [MIT OpenCourseWare](https://ocw.mit.edu/)
        """)

        st.markdown("---")

        # Clear category button
        if st.button("🔄 Clear Category", use_container_width=True):
            st.session_state.selected_category = None
            st.rerun()

        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def main():
    """Main application function"""

    # Page configuration
    st.set_page_config(
        page_title="Scientific Chatbot | Claude AI",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .chat-message {
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #e3f2fd;
            border-left: 5px solid #2196f3;
        }
        .assistant-message {
            background-color: #f3e5f5;
            border-left: 5px solid #9c27b0;
        }
        h1 {
            color: #1a237e;
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .stButton>button {
            border-radius: 20px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    init_session_state()

    # Header
    st.markdown("# 🔬 Scientific Chatbot powered by Claude AI")
    st.markdown("### *Your intelligent assistant for academic and professional scientific queries*")

    # API Key input in sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your Anthropic API key to use Claude AI"
        )
        if api_key_input:
            st.session_state.api_key = api_key_input

        if not st.session_state.api_key:
            st.warning("⚠️ Please enter your API key to start chatting")
        else:
            st.success("✅ API key configured")

        st.markdown("---")

    # Display resources sidebar
    display_resources_sidebar()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col2:
        # Category selection
        display_category_buttons()

    with col1:
        st.markdown("### 💬 Chat Interface")

        # Chat container
        chat_container = st.container()

        # Display chat messages
        with chat_container:
            for message in st.session_state.messages:
                role = message["role"]
                content = message["content"]
                timestamp = message.get("timestamp", "")

                if role == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>👤 You</strong> <small style="color: #666;">{timestamp}</small>
                        <p style="margin-top: 8px;">{content}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-message">
                        <strong>🤖 Claude AI</strong> <small style="color: #666;">{timestamp}</small>
                        <div style="margin-top: 8px;">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Chat input
        user_input = st.chat_input(
            "Ask your scientific question here...",
            disabled=not st.session_state.api_key
        )

        if user_input:
            # Add user message
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp
            })

            # Get Claude response
            with st.spinner("🤔 Claude is thinking..."):
                response = get_claude_response(
                    user_input,
                    st.session_state.selected_category
                )

            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🔬 Scientific Chatbot | Powered by Claude AI (Sonnet 4.5) | Built with Streamlit</p>
        <p><small>Covering: Chemistry, Physics, Biology, Biochemistry, Physiology, Mathematics, Geology, and Electricity & Magnetism</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
