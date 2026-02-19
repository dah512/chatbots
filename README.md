# 🤖 AI Applications Portfolio

Welcome to the AI Applications Portfolio! This repository contains multiple AI-powered applications designed to enhance learning, healthcare, and productivity.

## 🌐 Landing Page

Visit [index.html](./index.html) for an interactive showcase of all applications with animated previews and descriptions.

---

# 🔬 Scientific Chatbot - Claude AI Powered

A comprehensive, interactive scientific chatbot that provides expert answers to academic and professional queries across multiple scientific domains. Built with Python, Streamlit, and powered by Claude AI (Sonnet 4.5).

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![Claude AI](https://img.shields.io/badge/Claude-Sonnet%204.5-purple.svg)

## 🌟 Features

### 📚 Scientific Domains Covered
- **Chemistry** 🧪 - Organic, inorganic, analytical chemistry, and chemical reactions
- **Physics** ⚛️ - Classical mechanics, quantum physics, thermodynamics, and relativity
- **Biology** 🧬 - Cell biology, genetics, ecology, and evolutionary biology
- **Biochemistry** 🔬 - Molecular biology, enzymology, metabolism, and protein structures
- **Physiology** ❤️ - Human and animal physiology, organ systems, and homeostasis
- **Mathematics** 📐 - Algebra, calculus, statistics, and applied mathematics
- **Geology** 🌍 - Earth science, mineralogy, petrology, and geochemistry
- **Electricity & Magnetism** ⚡ - Electromagnetic theory, circuits, and electrodynamics

### ✨ Key Capabilities
- 🎨 **Beautiful, Colorful UI** - Warm and inviting interface with gradient backgrounds
- 🎯 **Category-Based Navigation** - Easy-to-use push-button interface for topic selection
- 💬 **Interactive Chat** - Real-time conversation with Claude AI
- 📖 **Resource Links** - Curated external resources for each scientific domain
- 🕒 **Chat History** - Track your conversation with timestamps
- 🔐 **Secure API Integration** - Safe handling of API credentials
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd chatbots
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key** (Choose one method)

   **Method 1: Environment Variable**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your API key
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

   **Method 2: Direct Input**
   - Enter your API key directly in the app's sidebar when it launches

### Running the Application

```bash
streamlit run scientific_chatbot.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter Your API Key**
   - On first launch, enter your Anthropic API key in the sidebar
   - The key is stored only for your current session

2. **Select a Scientific Domain**
   - Click on any of the 8 category buttons (Chemistry, Physics, etc.)
   - The chatbot will contextualize its responses to your selected domain
   - You can change categories at any time

3. **Ask Questions**
   - Type your question in the chat input at the bottom
   - Questions can range from elementary to advanced levels
   - The AI will provide detailed, accurate responses

4. **Explore Resources**
   - Check the sidebar for curated external resources
   - Each category has domain-specific research databases and tools
   - General resources are always available

5. **Manage Your Session**
   - Clear category selection to ask general questions
   - Clear chat history to start fresh
   - All controls are in the sidebar

## 🎨 UI Features

### Color-Coded Categories
Each scientific domain has its own color theme:
- Chemistry: Warm Red `#FF6B6B`
- Physics: Teal `#4ECDC4`
- Biology: Mint Green `#95E1D3`
- Biochemistry: Coral `#F38181`
- Physiology: Purple `#AA96DA`
- Mathematics: Pink `#FCBAD3`
- Geology: Sky Blue `#A8D8EA`
- Electricity & Magnetism: Golden Yellow `#FFD93D`

### Interactive Elements
- Gradient background for modern aesthetic
- Hover effects on buttons
- Distinct chat bubbles for user and AI messages
- Timestamped messages
- Responsive layout

## 🔗 External Resources

The chatbot includes links to authoritative sources:

### General Resources
- Google Scholar
- Wikipedia
- Khan Academy
- MIT OpenCourseWare

### Domain-Specific (examples)
- **Chemistry**: PubChem, ChemSpider
- **Physics**: Physics arXiv, HyperPhysics
- **Biology**: NCBI, BioRxiv
- **Mathematics**: Wolfram MathWorld
- And many more...

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit (Python web framework)
- **AI Backend**: Anthropic Claude API (Sonnet 4.5)
- **Language**: Python 3.8+

### File Structure
```
chatbots/
├── scientific_chatbot.py    # Main application
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Key Dependencies
- `streamlit` - Web UI framework
- `anthropic` - Claude AI API client
- `python-dotenv` - Environment variable management

## 💡 Example Questions

**Chemistry**
- "Explain the mechanism of SN2 reactions"
- "What is the difference between ionic and covalent bonds?"

**Physics**
- "Derive the Schrödinger equation"
- "Explain Einstein's theory of general relativity"

**Biology**
- "How does CRISPR-Cas9 gene editing work?"
- "What is the process of photosynthesis?"

**Mathematics**
- "Prove the Pythagorean theorem"
- "Explain the concept of limits in calculus"

**And many more across all domains!**

## 🔒 Security

- API keys are never stored permanently
- Environment variables are gitignored
- Session-based key storage only
- No data is logged or transmitted except to Anthropic's API

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest new features
- Add more scientific categories
- Improve the UI/UX
- Add more resource links

## 📝 License

This project is open source and available for educational and professional use.

## 🙏 Acknowledgments

- **Anthropic** - For the powerful Claude AI API
- **Streamlit** - For the excellent web framework
- **Scientific Community** - For the open-access resources linked in the app

## 📞 Support

For issues or questions:
1. Check the documentation above
2. Review the code comments in `scientific_chatbot.py`
3. Ensure your API key is valid
4. Check that all dependencies are installed

---

**Built with ❤️ for the scientific community**

🔬 Happy exploring! 🚀
