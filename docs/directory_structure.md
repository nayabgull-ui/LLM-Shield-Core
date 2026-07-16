# Production Project Directory Layout — LLM Shield

The project workspace is organized into discrete, modular sub-projects. Below is the structure, showing where specific application layers are housed:

```text
llm-shield/
│
├── .github/                       # GitHub Platform Configurations
│   └── workflows/                 # CI/CD automated pipeline scripts
│       └── ci-cd.yml              # Bandit security & automated test runner
│
├── backend/                       # FastAPI Server Root Directory
│   ├── app/                       # Core application packages
│   │   ├── api/                   # Route endpoints
│   │   │   ├── v1/                # API version controls
│   │   │   │   ├── auth.py        # Authentication validation handlers
│   │   │   │   └── leads.py       # Lead retrieval logic
│   │   │   └── deps.py            # Shared router dependency functions
│   │   │
│   │   ├── core/                  # Core setting configurations
│   │   │   ├── config.py          # Environment settings parser via Pydantic
│   │   │   └── security.py        # Hashing and encryption configurations
│   │   │
│   │   └── main.py                # Core App application startup file
│   │
│   ├── requirements.txt           # Python dependency file list
│   └── Dockerfile                 # Hardened, non-root build container file
│
├── frontend/                      # React Frontend Client Folder
│   ├── src/                       # Main client source files
│   │   ├── components/            # Isolated reusable UI components
│   │   ├── pages/                 # Main screen views
│   │   └── App.js                 # App routes and views wrapper
│   └── package.json               # Frontend dependencies manifest
│
└── security/                      # Threat modeling, security configurations
    └── api_security_report.md     # Documented secure email API integrations