# Pain Management Support Group Platform

A comprehensive web-based platform for delivering an 8-week Pain Management Support Group program. This system integrates educational content delivery, AI-powered Q&A, pain tracking, assessment tools, and outcome analytics.

## 🎯 Project Overview

This platform was designed to address a critical gap in pain management care: empowering patients with knowledge, reducing power differentials between patients and providers, and providing evidence-based alternatives to traditional pain management approaches.

### Key Features

- **8-Week Structured Curriculum**: 32 sessions covering pain science, pharmacology, alternative therapies, nutrition, and self-advocacy
- **AI-Powered Q&A**: RAG-based chatbot using LangChain and vector databases for answering patient questions
- **Comprehensive Tracking**: Daily pain logs, sleep quality, fatigue, anxiety, and functional assessments
- **Assessment Tools**: Pre/post tests with Python-based generation and R-based statistical analysis
- **Discussion Forums**: Safe space for patients to share experiences without fear of reprisal
- **Visual Learning Aids**: Anatomical diagrams, nerve pathways, and educational infographics
- **Multi-modal Approach**: Integration of Tai Chi, Qi Gong, Yoga, and nutrition education

### Target Audience

Middle-aged adults dealing with chronic pain from multiple conditions including:
- Orthopedic injuries (back, neck, shoulders, hips, knees)
- Rheumatic diseases (Rheumatoid Arthritis, SLE, Scleroderma, Sjögren's)
- Fibromyalgia
- Post-surgical pain syndromes

## 🏗️ Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI (Python 3.11+) |
| **Database** | PostgreSQL 15 |
| **Vector DB** | Pinecone / ChromaDB |
| **Cache** | Redis |
| **Frontend** | React 18+ with TypeScript |
| **AI/LLM** | OpenAI GPT-4 / Claude 3.5 Sonnet |
| **Embeddings** | OpenAI text-embedding-3-large |
| **RAG Framework** | LangChain |
| **Analytics** | Python (Pandas, NumPy) + R |
| **Containerization** | Docker & Docker Compose |
| **ORM** | SQLAlchemy |
| **Authentication** | JWT with OAuth2 |

### System Components

```
pain-management-support-group/
├── backend/              # FastAPI backend application
│   ├── api/             # API routes
│   ├── models/          # Database models
│   ├── controllers/     # Business logic controllers
│   ├── services/        # Service layer (RAG, email, etc.)
│   ├── utils/           # Utility functions
│   └── config/          # Configuration management
├── frontend/            # React frontend application
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom React hooks
│   │   ├── context/     # React context providers
│   │   └── services/    # API client services
│   └── public/          # Static assets
├── curriculum/          # 8-week curriculum content
│   ├── week-01/         # Week 1 materials
│   │   ├── sessions/    # Individual session content
│   │   ├── materials/   # Handouts and resources
│   │   ├── slides/      # PowerPoint/Keynote slides
│   │   └── assessments/ # Pre/post tests
│   └── ...             # Weeks 2-8
├── assessments/         # Assessment tools and analytics
│   ├── python/          # Python assessment generators
│   └── r/               # R statistical analysis scripts
├── research/            # Research and reference materials
│   ├── medications/     # Drug safety data
│   ├── support-groups/  # Global support group comparison
│   └── literature/      # AAFP journal references
├── rag/                 # RAG system components
│   ├── documents/       # Source documents for knowledge base
│   ├── embeddings/      # Vector embeddings storage
│   └── prompts/         # LLM prompt templates
├── visual-aids/         # Educational visual materials
│   ├── anatomy/         # Anatomical diagrams
│   ├── diagrams/        # Process diagrams
│   └── infographics/    # Educational infographics
├── database/            # Database schemas and migrations
├── docker/              # Docker configuration files
├── docs/                # Documentation
└── tests/               # Test suites
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+
  - Redis 7+

### Installation

#### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/pain-management-support-group.git
   cd pain-management-support-group
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database**
   ```bash
   docker-compose exec backend python -m backend.scripts.init_db
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - PgAdmin: http://localhost:5050 (dev mode)

#### Option 2: Manual Setup

**Backend Setup**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
createdb pain_management
alembic upgrade head

# Run backend
uvicorn main:app --reload
```

**Frontend Setup**

```bash
cd frontend
npm install
npm start
```

### Configuration

#### Essential Environment Variables

Edit `.env` file with the following required settings:

```bash
# OpenAI API (for LLM and embeddings)
OPENAI_API_KEY="your-key-here"

# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/pain_management"

# Security
SECRET_KEY="generate-a-secure-random-key"

# Vector Database (choose one)
USE_PINECONE=false  # Set to true for Pinecone, false for ChromaDB
PINECONE_API_KEY="your-pinecone-key"  # If using Pinecone
```

## 📚 Core Features

### 1. Curriculum Delivery

**8-Week Program Structure**
- **Week 1**: Understanding Pain - Biology and Neuroscience
- **Week 2**: Pharmacology - Medications and Mechanisms
- **Week 3**: Musculoskeletal System and Common Conditions
- **Week 4**: Rheumatic and Autoimmune Diseases
- **Week 5**: Alternative and Complementary Therapies
- **Week 6**: Nutrition, Metabolism, and Pain
- **Week 7**: Movement, Function, and Activities of Daily Living
- **Week 8**: Self-Advocacy and Moving Forward

Each week includes:
- 4 sessions (2.5 hours each)
- Lectures with visual aids
- Movement practice (Tai Chi, Qi Gong, Yoga)
- Nutrition education
- Pre/post assessments

### 2. AI-Powered Q&A System

**RAG (Retrieval-Augmented Generation) Chatbot**

```python
from backend.services.rag_service import RAGService

rag = RAGService()

# Query the knowledge base
result = await rag.query(
    query="How do NSAIDs reduce inflammation?",
    conversation_history=[]
)

print(result["response"])
# Response includes citations from medical literature
```

**Features:**
- Natural language queries about pain, medications, anatomy
- Cited responses from embedded medical literature
- Conversation history for context-aware answers
- Document upload for expanding knowledge base

### 3. Pain Tracking and Analytics

**Daily Pain Logging**
- Pain levels (VAS 0-10 scale)
- Location mapping
- Sleep quality, fatigue, anxiety tracking
- Functional assessments
- Medication tracking

**Outcome Analytics**
```python
from assessments.python.outcome_analytics import OutcomeAnalytics

analytics = OutcomeAnalytics()
report = analytics.generate_patient_report(
    user_id=123,
    pain_logs=patient_logs,
    assessment_scores=scores,
    program_completion=True
)

print(f"Pain reduction: {report['changes']['pain_level']['absolute_change']}")
print(f"Clinically significant: {report['clinically_significant']['pain_level']}")
```

### 4. Statistical Analysis (R)

```r
source("assessments/r/statistical_analysis.R")

# Load patient data
data <- load_patient_data("data/outcomes.csv")

# Perform paired t-tests
ttests <- perform_paired_ttests(data)

# Generate comprehensive report
results <- generate_statistical_report(data)
```

**Analyses Included:**
- Paired t-tests (pre-post comparison)
- Repeated measures ANOVA
- Longitudinal mixed-effects modeling
- Clinical significance calculations
- Effect size computations
- Comprehensive visualizations

## 📊 API Documentation

### Authentication

```bash
# Register
POST /api/v1/auth/register
{
  "email": "patient@example.com",
  "username": "patient123",
  "password": "securepass",
  "first_name": "John",
  "last_name": "Doe"
}

# Login
POST /api/v1/auth/login
{
  "username": "patient123",
  "password": "securepass"
}

# Response
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Curriculum

```bash
# Get all weeks
GET /api/v1/curriculum/weeks

# Get specific week
GET /api/v1/curriculum/week/1

# Get week sessions
GET /api/v1/curriculum/week/1/sessions
```

### Pain Tracking

```bash
# Log pain entry
POST /api/v1/pain/log
{
  "pain_level": 6,
  "pain_locations": "[\"lower_back\", \"hip_right\"]",
  "sleep_quality": 5,
  "fatigue_level": 7,
  "medications_taken": "[\"ibuprofen 400mg\"]"
}

# Get pain history
GET /api/v1/pain/history?limit=30

# Get analytics
GET /api/v1/pain/analytics
```

### AI Q&A

```bash
# Query AI
POST /api/v1/rag/query
{
  "query": "What are the side effects of long-term NSAID use?",
  "conversation_id": 123,
  "use_history": true
}

# Response
{
  "response": "Long-term NSAID use can lead to several side effects...",
  "sources": [
    {"source": "AAFP_journal_2020.pdf", "content": "..."}
  ],
  "conversation_id": 123,
  "message_id": 456
}
```

### Assessments

```bash
# Get pre-test
GET /api/v1/assessments/week/1/pre

# Submit answers
POST /api/v1/assessments/week/1/pre/submit
{
  "answers": {
    "q1": "B",
    "q2": "A",
    ...
  }
}
```

Full API documentation available at: `http://localhost:8000/docs`

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📈 Data Privacy & Security

### HIPAA Compliance Considerations

- **Encryption**: All PHI encrypted at rest and in transit (TLS 1.3)
- **Authentication**: JWT-based auth with secure token expiration
- **Access Control**: Role-based access (Patient, Instructor, Admin)
- **Audit Logging**: All data access logged with timestamps
- **Data Minimization**: Only collect necessary health information
- **User Consent**: Clear consent forms for data collection and use

**Note**: This system includes security features but would require full HIPAA audit and BAA agreements before handling real patient data in production.

## 🌍 Global Pain Support Groups - Research

See `research/support-groups/global_comparison.md` for comprehensive analysis of pain support programs worldwide:

- UK NHS Pain Management Programmes
- Australian National Pain Strategy
- Canadian Chronic Pain Networks
- European pain patient advocacy
- Comparison with US programs
- Best practices and recommendations

## 🔬 Research Data Included

### Pain Medication Statistics

- Acetaminophen hepatotoxicity rates (AAFP data 2004-2024)
- NSAID-related hospitalizations (GI bleeding, cardiovascular events)
- Opioid prescribing trends and overdose statistics
- Efficacy data for various pain management approaches

See `research/medications/` for detailed compilations.

## 🎨 Visual Aids & Educational Materials

The `visual-aids/` directory includes templates and examples for:

- **Anatomy Diagrams**:
  - Spinal cord cross-sections with nerve pathways
  - Dermatome maps (anterior and posterior)
  - Joint anatomy (ball-socket, hinge, pivot)
  - Muscle and tendon structures

- **Pain Pathways**:
  - Nociceptor activation sequence
  - Spinothalamic tract visualization
  - Gate control theory diagrams
  - Autonomic nervous system effects

- **Pharmacology**:
  - Drug mechanism diagrams
  - COX pathway and NSAID inhibition
  - Opioid receptor locations
  - Metabolism flowcharts

## 🤝 Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for guidelines.

Areas where contributions are especially valuable:
- Additional curriculum content and exercises
- Translations (Spanish, Chinese, etc.)
- Alternative therapy research
- Outcome measurement tools
- UI/UX improvements
- Mobile app development

## 📝 License

[Choose appropriate license - MIT, GPL, etc.]

## 🙏 Acknowledgments

This project was inspired by the lived experience of patients navigating chronic pain management in a healthcare system that often dismisses or under-treats pain due to fear of regulatory scrutiny.

Special thanks to:
- Pain patients who shared their stories
- Healthcare providers committed to compassionate pain care
- Researchers advancing pain science
- Open-source community for excellent tools

## 📧 Contact & Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@painmanagement.com

## 🗺️ Roadmap

### Phase 1 (Current): Core Platform
- [x] Backend API with authentication
- [x] Database models and migrations
- [x] RAG system with LangChain
- [x] Assessment generation tools
- [x] Statistical analysis scripts
- [x] 8-week curriculum outline
- [ ] Frontend UI components
- [ ] Visual aids library

### Phase 2: Enhanced Features
- [ ] Mobile app (React Native)
- [ ] Video conferencing integration
- [ ] Wearable device integration (Apple Health, Fitbit)
- [ ] Multilingual support
- [ ] Provider dashboard for monitoring

### Phase 3: Research & Scale
- [ ] Research portal for aggregated analytics
- [ ] Multi-site deployment capability
- [ ] EMR/EHR integration
- [ ] Insurance billing integration
- [ ] Outcome publication pipeline

## 💡 Usage Tips

### For Program Facilitators

1. **Pre-Program Setup**:
   - Upload all curriculum materials
   - Ingest medical literature into RAG system
   - Create discussion forum categories
   - Set up user accounts

2. **During Program**:
   - Monitor participant progress dashboards
   - Review AI chatbot conversations for common questions
   - Facilitate weekly discussions
   - Track attendance and engagement

3. **Post-Program**:
   - Generate outcome reports
   - Export data for R analysis
   - Survey participants for feedback
   - Plan follow-up sessions

### For Patients

1. **Getting Started**:
   - Complete enrollment and baseline assessments
   - Set up daily pain logging reminders
   - Explore curriculum materials
   - Join discussion forums

2. **Weekly Routine**:
   - Attend 2-4 sessions per week
   - Complete pre/post tests
   - Log pain daily
   - Ask questions via AI chatbot
   - Practice movement exercises

3. **Tracking Progress**:
   - Review personal dashboard
   - Monitor pain trends
   - Track functional improvements
   - Celebrate milestones

## 🔧 Troubleshooting

### Common Issues

**Issue**: Docker containers won't start
```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose down
docker-compose up -d
```

**Issue**: Database connection errors
```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Check connection
docker-compose exec postgres psql -U postgres -d pain_management -c "SELECT 1;"
```

**Issue**: RAG queries returning no results
```bash
# Verify documents are ingested
docker-compose exec backend python -m backend.scripts.check_vector_db

# Re-ingest documents
docker-compose exec backend python -m backend.scripts.ingest_docs
```

**Issue**: Frontend can't reach backend
```bash
# Check REACT_APP_API_URL in frontend .env
# Ensure backend is running on expected port
curl http://localhost:8000/health
```

## 📚 Additional Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [Database Schema](docs/DATABASE_SCHEMA.md)
- [API Reference](docs/API_REFERENCE.md)
- [Curriculum Guide](docs/CURRICULUM_GUIDE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Security Best Practices](docs/SECURITY.md)

---

**Built with ❤️ for pain patients seeking knowledge, community, and better care.**
