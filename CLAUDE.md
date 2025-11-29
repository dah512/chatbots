# CLAUDE.md - AI Assistant Guide

**Repository**: Scientific Chatbot powered by Claude AI
**Last Updated**: 2025-11-29
**Purpose**: Comprehensive guide for AI assistants working with this codebase

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Codebase Structure](#codebase-structure)
3. [Architecture & Design](#architecture--design)
4. [Development Workflows](#development-workflows)
5. [Key Conventions](#key-conventions)
6. [Code Modification Guidelines](#code-modification-guidelines)
7. [Testing & Deployment](#testing--deployment)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Repository Overview

### Purpose
A Streamlit-based scientific chatbot powered by Claude AI (Sonnet 4.5) that provides expert answers across 8 scientific domains: Chemistry, Physics, Biology, Biochemistry, Physiology, Mathematics, Geology, and Electricity & Magnetism.

### Tech Stack
- **Frontend Framework**: Streamlit 1.29+
- **AI Backend**: Anthropic Claude API (claude-sonnet-4-5-20250929)
- **Language**: Python 3.8+
- **Configuration**: python-dotenv for environment variables
- **Optional**: pandas, plotly (included but not actively used)

### Repository Status
- **Production State**: Functional single-file application
- **Complexity**: Low - Single main file with ~370 lines
- **Deployment**: Local development server (Streamlit)

---

## Codebase Structure

```
chatbots/
├── scientific_chatbot.py    # Main application (370 lines)
│   ├── SCIENTIFIC_CATEGORIES # Dictionary of 8 scientific domains
│   ├── init_session_state()  # Session state initialization
│   ├── get_claude_response() # Claude API integration
│   ├── display_category_buttons() # Category UI
│   ├── display_resources_sidebar() # Sidebar resources
│   └── main()                # Application entry point
│
├── requirements.txt          # Python dependencies
│   ├── streamlit>=1.29.0
│   ├── anthropic>=0.34.0
│   ├── python-dotenv>=1.0.0
│   ├── pandas>=2.0.0 (optional)
│   └── plotly>=5.17.0 (optional)
│
├── .env.example             # API key template
├── .gitignore               # Git ignore rules
├── run_chatbot.sh           # Linux/Mac launcher script
├── run_chatbot.bat          # Windows launcher script
└── README.md                # User-facing documentation
```

### File Descriptions

#### scientific_chatbot.py (370 lines)
**Main application file** - Contains all functionality:
- **Lines 1-85**: Configuration and constants (SCIENTIFIC_CATEGORIES dict)
- **Lines 88-96**: Session state initialization
- **Lines 98-138**: Claude API integration with error handling
- **Lines 140-169**: Category selection UI
- **Lines 171-205**: Sidebar resources display
- **Lines 207-369**: Main application logic and UI rendering

**Key Imports**:
```python
import streamlit as st
import anthropic
import os
from datetime import datetime
```

---

## Architecture & Design

### Application Flow

```
1. User launches app (via run_chatbot.sh or streamlit run)
   ↓
2. main() initializes Streamlit page config
   ↓
3. init_session_state() sets up session variables
   ↓
4. User enters API key in sidebar
   ↓
5. User selects scientific category (optional)
   ↓
6. User asks question via chat input
   ↓
7. get_claude_response() sends request to Claude API
   ↓
8. Response displayed in chat interface
   ↓
9. Repeat steps 5-8
```

### Session State Management

**Session Variables** (`st.session_state`):
- `messages`: List of chat messages (role, content, timestamp)
- `selected_category`: Currently selected scientific domain (or None)
- `api_key`: Anthropic API key (from env or user input)

**Initialization** (scientific_chatbot.py:88-96):
```python
def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")
```

### Claude API Integration

**Model**: claude-sonnet-4-5-20250929
**Max Tokens**: 2048
**System Prompt**: Dynamic based on selected category

**Implementation** (scientific_chatbot.py:98-138):
- Authentication via API key
- Error handling for AuthenticationError, APIError, general exceptions
- Category-aware system prompts
- Single-turn conversation (no message history sent to API)

**Key Detail**: The app does NOT send full conversation history to Claude API, only the current user message. This is a design choice that could be modified if needed.

### UI/UX Design

**Layout**:
- Wide layout with sidebar
- 2-column main area: Chat (left) + Categories (right)
- Custom CSS with gradient backgrounds
- Color-coded categories

**Styling**:
- User messages: Blue theme (#e3f2fd background, #2196f3 border)
- Assistant messages: Purple theme (#f3e5f5 background, #9c27b0 border)
- Category buttons: Each domain has unique color (defined in SCIENTIFIC_CATEGORIES)

**Category Colors**:
```python
"Chemistry": "#FF6B6B"      # Warm Red
"Physics": "#4ECDC4"        # Teal
"Biology": "#95E1D3"        # Mint Green
"Biochemistry": "#F38181"   # Coral
"Physiology": "#AA96DA"     # Purple
"Mathematics": "#FCBAD3"    # Pink
"Geology": "#A8D8EA"        # Sky Blue
"Electricity & Magnetism": "#FFD93D"  # Golden Yellow
```

### External Resources

Each category has 2 curated external resources (scientific databases, research tools).
General resources are always visible in sidebar:
- Google Scholar
- Wikipedia
- Khan Academy
- MIT OpenCourseWare

---

## Development Workflows

### Initial Setup

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd chatbots
   ```

2. **Create Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # OR
   venv\Scripts\activate.bat  # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key** (choose one):
   - Create `.env` file: `cp .env.example .env` and add key
   - OR enter key in app sidebar on launch

### Running the Application

**Method 1: Using launcher scripts**
```bash
# Linux/Mac
./run_chatbot.sh

# Windows
run_chatbot.bat
```

**Method 2: Direct Streamlit command**
```bash
streamlit run scientific_chatbot.py
```

**Method 3: With custom port**
```bash
streamlit run scientific_chatbot.py --server.port 8502
```

### Making Code Changes

1. **Edit scientific_chatbot.py**
2. Streamlit auto-reloads on file save (if running)
3. Test changes in browser
4. Commit changes to git

### Adding New Scientific Categories

**Steps**:
1. Add new entry to `SCIENTIFIC_CATEGORIES` dict (scientific_chatbot.py:12-85)
2. Include: icon (emoji), color (hex), description, and 2 resources
3. No other code changes needed - UI auto-adjusts

**Example**:
```python
"Astronomy": {
    "icon": "🌌",
    "color": "#1E3A5F",
    "description": "Stellar physics, cosmology, and planetary science",
    "resources": [
        {"name": "NASA ADS", "url": "https://ui.adsabs.harvard.edu/"},
        {"name": "arXiv Astro", "url": "https://arxiv.org/archive/astro-ph"},
    ]
}
```

### Git Workflow

**Branch Strategy**:
- Main/master branch for stable releases
- Feature branches for development (e.g., `claude/claude-md-...`)

**Current Branch**: `claude/claude-md-mijvjf7rz1001x1k-01AXgMQPqChQcNPvsxdaFeW8`

**Commit Guidelines**:
- Clear, descriptive commit messages
- Focus on "why" rather than "what"
- Example: "Add Astronomy category for celestial physics questions"

**Push Command**:
```bash
git push -u origin <branch-name>
```

**Important**: Branch names should start with 'claude/' and end with matching session ID for push to succeed.

---

## Key Conventions

### Code Style

1. **Docstrings**: Every function has a docstring explaining purpose
2. **Comments**: Minimal inline comments - code is self-documenting
3. **Function Names**: Snake_case (e.g., `init_session_state`)
4. **Constants**: UPPER_CASE (e.g., `SCIENTIFIC_CATEGORIES`)
5. **Imports**: Standard library → Third-party → Local (none in this project)

### Naming Conventions

- **Session state keys**: Lowercase with underscores (`selected_category`, `api_key`)
- **Streamlit button keys**: Prefix pattern (e.g., `cat_Chemistry`, `cat_Physics`)
- **CSS classes**: Kebab-case (`.chat-message`, `.user-message`)

### Error Handling

**Pattern** (scientific_chatbot.py:132-137):
```python
try:
    # API call
except anthropic.AuthenticationError:
    return "❌ Authentication error. Please check your API key."
except anthropic.APIError as e:
    return f"❌ API error: {str(e)}"
except Exception as e:
    return f"❌ Error: {str(e)}"
```

**User-Facing**: All errors return user-friendly messages with emoji indicators.

### Security Best Practices

1. **API Key Storage**:
   - Never commit `.env` to git (in `.gitignore`)
   - Use `type="password"` for API key input
   - Session-only storage (not persisted)

2. **Dependencies**:
   - Pin major versions in `requirements.txt`
   - Regular updates for security patches

3. **Input Validation**:
   - User input is passed directly to Claude API (API handles validation)
   - No SQL injection risk (no database)
   - No XSS risk (Streamlit handles sanitization)

---

## Code Modification Guidelines

### DO

✅ **Test locally before committing**
✅ **Preserve existing code structure** (single-file design is intentional)
✅ **Maintain backward compatibility** with existing session state
✅ **Update README.md** if adding user-facing features
✅ **Follow existing color/styling patterns**
✅ **Add error handling** for new external integrations
✅ **Keep dependencies minimal** (only add if essential)

### DON'T

❌ **Split into multiple files** without discussion (violates design principle)
❌ **Change Claude model** without testing (token limits may differ)
❌ **Remove pandas/plotly** from requirements (may be used in future)
❌ **Modify .gitignore** to commit `.env` files
❌ **Hard-code API keys** in source code
❌ **Remove existing scientific categories** (only add new ones)
❌ **Change color scheme** drastically (maintain visual consistency)

### When Adding Features

1. **Check session state**: Will new feature need session variables?
2. **Consider UI placement**: Sidebar vs main area vs modal
3. **Test error cases**: API failures, invalid input, etc.
4. **Update documentation**: README.md and this file
5. **Verify mobile responsiveness**: Streamlit's responsive design

### When Fixing Bugs

1. **Identify root cause**: Check Streamlit console logs
2. **Reproduce locally**: Run app and test scenario
3. **Fix minimal code**: Don't over-engineer
4. **Test edge cases**: Empty input, API failures, etc.
5. **Document fix**: In commit message

---

## Testing & Deployment

### Local Testing

**Manual Testing Checklist**:
- [ ] App launches without errors
- [ ] API key validation works (valid/invalid keys)
- [ ] All 8 category buttons functional
- [ ] Category selection persists until cleared
- [ ] Chat input sends messages
- [ ] Claude responses display correctly
- [ ] Sidebar resources render
- [ ] Clear chat button works
- [ ] Clear category button works
- [ ] Timestamps display in chat
- [ ] Error messages display for API failures

**Test Commands**:
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Verify dependencies
pip list | grep -E "(streamlit|anthropic|dotenv)"

# Run app
streamlit run scientific_chatbot.py

# Check for errors in console
# Look for Streamlit logs in terminal
```

### Deployment

**Current Deployment**: Local development only (no production deployment)

**Potential Deployment Options** (for future):
1. **Streamlit Cloud**: Free hosting for public repos
2. **Docker**: Container-based deployment
3. **Heroku/Railway**: Platform-as-a-Service
4. **Self-hosted**: VPS with nginx reverse proxy

**Deployment Considerations**:
- API key management (use secrets management, not .env)
- Rate limiting (Anthropic API has usage limits)
- Concurrent users (session state is per-user)
- HTTPS required for production

### Performance Considerations

**Current State**:
- Single-file app: Fast initial load
- No database: No query overhead
- No file uploads: No storage concerns
- Streamlit caching: Not currently used (could optimize API calls)

**Potential Optimizations**:
1. Cache Claude responses for identical questions
2. Add conversation history to API calls (more context)
3. Implement streaming responses (better UX for long answers)
4. Add session timeout for API key security

---

## Common Tasks

### Task 1: Add a New Scientific Category

**File**: `scientific_chatbot.py`
**Location**: Lines 12-85 (SCIENTIFIC_CATEGORIES dict)

```python
# Add this entry to SCIENTIFIC_CATEGORIES
"Your Category": {
    "icon": "🔭",  # Choose appropriate emoji
    "color": "#HEX_COLOR",  # Choose unique color
    "description": "Brief description of the domain",
    "resources": [
        {"name": "Resource 1", "url": "https://example.com"},
        {"name": "Resource 2", "url": "https://example.com"},
    ]
}
```

**Testing**: Launch app, verify button appears, test category selection.

### Task 2: Modify System Prompt

**File**: `scientific_chatbot.py`
**Location**: Lines 104-114 (get_claude_response function)

```python
# Current system prompt
system_prompt = """You are an expert scientific assistant..."""

# Modify as needed, test responses
```

**Testing**: Ask questions in different categories, verify prompt affects responses.

### Task 3: Change Claude Model

**File**: `scientific_chatbot.py`
**Location**: Line 122 (client.messages.create call)

```python
# Current model
model="claude-sonnet-4-5-20250929",

# Change to different model (e.g., Haiku for faster/cheaper responses)
model="claude-3-haiku-20240307",
```

**Testing**: Verify API calls succeed, check response quality.

### Task 4: Add Conversation History to API Calls

**File**: `scientific_chatbot.py`
**Location**: Lines 125-128 (messages parameter in API call)

**Current** (single message):
```python
messages=[
    {"role": "user", "content": user_message}
]
```

**Modified** (full history):
```python
messages=[
    {"role": msg["role"], "content": msg["content"]}
    for msg in st.session_state.messages
] + [{"role": "user", "content": user_message}]
```

**Testing**: Have multi-turn conversation, verify Claude remembers context.

### Task 5: Customize UI Colors

**File**: `scientific_chatbot.py`
**Location**: Lines 219-261 (CSS in st.markdown)

**User Message Color**:
```python
.user-message {
    background-color: #e3f2fd;  # Change this
    border-left: 5px solid #2196f3;  # And this
}
```

**Testing**: Send messages, verify colors display correctly.

### Task 6: Add New External Resource

**File**: `scientific_chatbot.py`
**Location**: Lines 186-192 (General Resources in sidebar)

```python
st.markdown("""
- [Google Scholar](https://scholar.google.com/)
- [Wikipedia](https://www.wikipedia.org/)
- [Khan Academy](https://www.khanacademy.org/)
- [MIT OpenCourseWare](https://ocw.mit.edu/)
- [Your New Resource](https://example.com/)  # Add here
""")
```

**Testing**: Check sidebar, verify link works.

### Task 7: Modify Max Token Limit

**File**: `scientific_chatbot.py`
**Location**: Line 123 (max_tokens parameter)

```python
# Current limit
max_tokens=2048,

# Increase for longer responses
max_tokens=4096,
```

**Testing**: Ask complex questions, verify responses aren't cut off.

---

## Troubleshooting

### Issue: "Authentication error. Please check your API key."

**Cause**: Invalid or missing API key
**Solution**:
1. Verify API key in Anthropic console
2. Check `.env` file format: `ANTHROPIC_API_KEY=sk-ant-...`
3. Re-enter key in app sidebar
4. Ensure no extra spaces in key

### Issue: App doesn't launch

**Cause**: Missing dependencies or Python version
**Solution**:
```bash
# Check Python version
python3 --version  # Must be 3.8+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Streamlit installation
streamlit --version
```

### Issue: Category buttons not working

**Cause**: Session state issue or Streamlit caching
**Solution**:
1. Clear browser cache
2. Restart Streamlit server
3. Check browser console for JavaScript errors
4. Try different browser

### Issue: Chat messages not displaying

**Cause**: Custom CSS conflict or HTML rendering issue
**Solution**:
1. Check scientific_chatbot.py:313-325 for HTML syntax
2. Disable custom CSS temporarily (comment out lines 219-261)
3. Check Streamlit version compatibility

### Issue: "ModuleNotFoundError: No module named 'anthropic'"

**Cause**: Dependencies not installed or wrong Python environment
**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip show anthropic
```

### Issue: API rate limit errors

**Cause**: Anthropic API rate limits exceeded
**Solution**:
1. Check Anthropic console for usage limits
2. Implement request throttling
3. Add caching for repeated questions
4. Upgrade API plan if needed

### Issue: Slow response times

**Cause**: Network latency or model selection
**Solution**:
1. Check internet connection
2. Try smaller model (e.g., Haiku instead of Sonnet)
3. Reduce max_tokens if appropriate
4. Implement streaming responses

### Issue: Git push fails with 403 error

**Cause**: Branch name doesn't match required pattern
**Solution**:
```bash
# Branch must start with 'claude/' and end with session ID
git branch  # Check current branch name

# If needed, rename branch
git branch -m claude/new-session-id

# Ensure branch name matches session ID
git push -u origin claude/claude-md-mijvjf7rz1001x1k-01AXgMQPqChQcNPvsxdaFeW8
```

---

## Additional Context for AI Assistants

### Understanding User Intent

**Common Request Types**:
1. **Add feature**: New category, UI enhancement, API modification
2. **Fix bug**: Error handling, UI glitches, API failures
3. **Refactor**: Code organization, performance optimization
4. **Document**: Update README, add comments, create guides
5. **Deploy**: Setup for production, containerization

### Decision-Making Guidelines

**When to suggest major changes**:
- User explicitly requests architectural changes
- Current design clearly doesn't scale for new requirements
- Security vulnerability requires structural fix

**When to maintain current structure**:
- Minor feature additions
- Bug fixes
- UI tweaks
- Configuration changes

### Code Reading Tips

1. **Start with main()**: Entry point at line 207
2. **Check session state**: Understand data flow via st.session_state
3. **Follow user interaction**: Button clicks → st.rerun() → re-render
4. **Trace API calls**: User input → get_claude_response() → display
5. **Review CSS**: Lines 219-261 for all styling

### Files That Should Never Be Modified

- `.git/` directory
- `.gitignore` (unless adding new ignore patterns)
- `venv/` or `ENV/` (virtual environment)
- `.env` (user-specific, not in repo)

### Files That Should Be Kept in Sync

- `README.md` ↔ User-facing documentation
- `CLAUDE.md` ↔ Developer/AI documentation
- `.env.example` ↔ Required environment variables
- `requirements.txt` ↔ Actual dependencies used

---

## Conclusion

This codebase is intentionally simple and focused. The single-file design makes it easy to understand and modify, while Streamlit handles the complexity of web development. When making changes:

1. Preserve simplicity
2. Test thoroughly
3. Document user-facing changes
4. Follow existing patterns
5. Ask user if unclear about requirements

**Happy coding! 🔬**
