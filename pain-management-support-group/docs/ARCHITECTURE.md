# Pain Management Support Group - System Architecture

## Overview
This is a comprehensive web-based platform for an 8-week Pain Management Support Group program. The system integrates educational content delivery, assessment tools, progress tracking, and AI-powered document Q&A capabilities.

## System Components

### 1. Frontend (React + TypeScript)
**Purpose:** User interface for patients, instructors, and administrators

**Key Features:**
- Patient dashboard with progress tracking
- Interactive curriculum viewer
- Pre/post assessment interface
- Pain tracking journal
- Discussion forums
- Visual learning aids viewer
- Exercise video player (Tai Chi, Qi Gong, Yoga)
- Nutrition planner
- AI-powered Q&A chatbot

**Tech Stack:**
- React 18+ with TypeScript
- React Router for navigation
- Context API + Redux for state management
- Axios for API calls
- Chart.js for data visualization
- TailwindCSS for styling (warm, soothing color palette)
- Material-UI components

### 2. Backend API (FastAPI + Python)
**Purpose:** RESTful API server handling all business logic

**Tech Stack:**
- FastAPI (Python 3.11+)
- Pydantic for data validation
- SQLAlchemy ORM
- PostgreSQL database
- JWT authentication
- Celery for background tasks

**API Endpoints:**

#### Authentication & Users
- POST `/api/auth/register` - Register new patient
- POST `/api/auth/login` - User login
- GET `/api/users/profile` - Get user profile
- PUT `/api/users/profile` - Update profile

#### Curriculum
- GET `/api/curriculum/weeks` - List all weeks
- GET `/api/curriculum/week/{id}` - Get week details
- GET `/api/curriculum/week/{id}/sessions` - Get sessions for week
- GET `/api/curriculum/session/{id}` - Get session content

#### Assessments
- GET `/api/assessments/week/{week_num}/pre` - Get pre-test
- POST `/api/assessments/week/{week_num}/pre/submit` - Submit pre-test
- GET `/api/assessments/week/{week_num}/post` - Get post-test
- POST `/api/assessments/week/{week_num}/post/submit` - Submit post-test
- GET `/api/assessments/results` - Get user's assessment history

#### Pain Tracking
- POST `/api/pain/log` - Log pain entry
- GET `/api/pain/history` - Get pain history
- GET `/api/pain/analytics` - Get pain analytics

#### Progress Tracking
- GET `/api/progress/overview` - Overall progress
- GET `/api/progress/week/{week_num}` - Week-specific progress
- POST `/api/progress/activity` - Log activity completion

#### RAG/AI Q&A
- POST `/api/rag/query` - Ask question to AI
- GET `/api/rag/conversations` - Get conversation history

#### Resources
- GET `/api/resources/visual-aids` - Get visual aids
- GET `/api/resources/slides/{week_num}` - Get slides for week
- GET `/api/resources/materials` - Get supplementary materials

### 3. Database (PostgreSQL)
**Purpose:** Persistent storage for all application data

**Main Tables:**
- `users` - User accounts and profiles
- `curriculum_weeks` - 8-week structure
- `curriculum_sessions` - 32 session details
- `assessments` - Pre/post test questions
- `assessment_submissions` - User responses
- `pain_logs` - Daily pain tracking entries
- `progress_tracking` - Activity completion status
- `discussion_posts` - Forum posts
- `resources` - Educational materials metadata
- `rag_conversations` - AI chat history

### 4. RAG System (LangChain + Vector DB)
**Purpose:** AI-powered document Q&A using embedded medical literature

**Components:**
- **Document Ingestion Pipeline:**
  - PDF parsers for medical journals
  - Text chunking with semantic awareness
  - Metadata extraction (source, date, topic)

- **Embedding Generation:**
  - Model: OpenAI text-embedding-3-large
  - Chunk size: 512 tokens with 50-token overlap

- **Vector Database Options:**
  - **Primary:** Pinecone (cloud-based, production)
  - **Alternative:** ChromaDB (local development)

- **Query Pipeline:**
  - User query → Embedding → Similarity search
  - Context retrieval (top 5 chunks)
  - LLM generation (Claude 3.5 Sonnet) with citations
  - Response validation for medical accuracy

**Document Categories:**
- AAFP journal articles (20 years)
- Anatomy textbooks (12th-grade level)
- Pharmacology references
- Alternative therapy research
- Nutrition and metabolism guides
- Exercise instruction manuals

### 5. Assessment Engine (Python + R)
**Purpose:** Statistical analysis of patient outcomes

**Python Components:**
- Pre/post test generation
- Scoring algorithms
- Progress metrics calculation
- Data export to R

**R Components:**
- Statistical analysis (paired t-tests, ANOVA)
- Longitudinal outcome modeling
- Visualization generation
- Report generation (PDF reports)

**Metrics Tracked:**
- Pain levels (VAS scale)
- Sleep quality
- Fatigue scores
- Anxiety levels (GAD-7)
- Physical function (ROM, strength)
- ADL completion rates
- Medication usage

### 6. Controllers
**Purpose:** Business logic layer between API and services

**Key Controllers:**
- `AuthController` - Authentication and authorization
- `CurriculumController` - Content delivery logic
- `AssessmentController` - Test administration
- `ProgressController` - Progress calculations
- `RAGController` - AI query orchestration
- `AnalyticsController` - Data aggregation

### 7. Services Layer
**Purpose:** Reusable business services

**Key Services:**
- `UserService` - User management
- `AssessmentService` - Test generation and scoring
- `PainTrackingService` - Pain data processing
- `EmbeddingService` - Vector operations
- `NotificationService` - Email/SMS alerts
- `ReportService` - PDF report generation

## Data Flow

### Typical User Journey:
1. User registers/logs in (Frontend → Auth API)
2. Dashboard loads progress data (Frontend → Progress API → Database)
3. User views week content (Frontend → Curriculum API → Database)
4. User takes pre-test (Frontend → Assessment API → Database)
5. User attends session (content from Database)
6. User logs pain daily (Frontend → Pain API → Database)
7. User asks AI question (Frontend → RAG API → Vector DB → LLM → Frontend)
8. User takes post-test (Frontend → Assessment API → Database → R Analysis)
9. User views progress report (Frontend → Analytics API → R Engine → Frontend)

## Security & Compliance

### Authentication:
- JWT tokens with refresh mechanism
- Password hashing (bcrypt)
- Role-based access control (Patient, Instructor, Admin)

### Data Privacy:
- HIPAA compliance considerations
- PHI encryption at rest and in transit
- Audit logging for data access
- Data anonymization for research

### API Security:
- Rate limiting
- CORS configuration
- Input validation
- SQL injection prevention
- XSS protection

## Deployment Architecture

### Development:
- Local PostgreSQL database
- ChromaDB for vector storage
- Docker Compose for services
- Hot reload for frontend/backend

### Production:
- **Cloud Provider:** AWS/Azure/GCP
- **Frontend:** Vercel or S3 + CloudFront
- **Backend:** ECS/Kubernetes pods
- **Database:** RDS PostgreSQL (Multi-AZ)
- **Vector DB:** Pinecone (managed)
- **Cache:** Redis
- **CDN:** CloudFront for static assets
- **Monitoring:** DataDog/New Relic
- **Logging:** ELK stack

### Scaling Strategy:
- Horizontal scaling for API servers
- Database read replicas
- CDN for static content
- Background job queues (Celery + Redis)

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + TypeScript | User interface |
| API | FastAPI | REST endpoints |
| Database | PostgreSQL | Relational data |
| Vector DB | Pinecone/ChromaDB | Embeddings |
| Cache | Redis | Session/query cache |
| Background Jobs | Celery | Async tasks |
| LLM | Claude 3.5 Sonnet | AI responses |
| Embeddings | OpenAI API | Vector generation |
| Analytics | Python + R | Statistical analysis |
| Containerization | Docker | Deployment |
| Orchestration | Docker Compose/K8s | Service management |
| Version Control | Git/GitHub | Code management |
| CI/CD | GitHub Actions | Automation |

## Development Workflow

1. **Local Development:**
   ```bash
   docker-compose up  # Start all services
   cd frontend && npm run dev  # Frontend dev server
   cd backend && uvicorn main:app --reload  # Backend dev server
   ```

2. **Testing:**
   - Unit tests: pytest (backend), Jest (frontend)
   - Integration tests: API test suite
   - E2E tests: Playwright

3. **Deployment:**
   - Push to GitHub → Actions run tests
   - Merge to main → Auto-deploy to staging
   - Manual promotion to production

## Future Enhancements

1. **Mobile App:** React Native version
2. **Telehealth Integration:** Video conferencing for remote sessions
3. **Wearables Integration:** Apple Health, Fitbit data import
4. **Multilingual Support:** Spanish, Chinese translations
5. **Gamification:** Achievement badges, progress milestones
6. **Social Features:** Patient-to-patient support groups
7. **Provider Dashboard:** For physicians to monitor patients
8. **Research Portal:** Anonymized data for pain management research

## File Structure

```
pain-management-support-group/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   ├── middleware/
│   │   └── dependencies.py
│   ├── models/
│   ├── controllers/
│   ├── services/
│   ├── utils/
│   └── config/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── context/
│   │   ├── services/
│   │   └── styles/
│   └── public/
├── curriculum/
│   └── week-{01-08}/
├── assessments/
│   ├── python/
│   └── r/
├── rag/
│   ├── documents/
│   ├── embeddings/
│   └── prompts/
├── docker/
├── docs/
└── tests/
```

## Conclusion

This architecture provides a scalable, secure, and user-friendly platform for delivering comprehensive pain management education and support. The modular design allows for independent development and testing of components while maintaining clear interfaces between layers.
