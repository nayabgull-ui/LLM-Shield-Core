```markdown
# Built-In Security Practices — LLM Shield

## 1. Input Validation & Type Enforcement
All request payloads entering the FastAPI backend must match a pre-defined Pydantic model class. This prevents **Over-posting/Mass Assignment** vulnerabilities.

## 2. Dynamic Secret Management
* **Never commit configurations:** All keys are injected during environment creation.
* **Local development:** Loaded strictly via a git-ignored `.env` file.
* **CI/CD pipeline:** Injected via GitHub repository secrets during action steps.

## 3. Strict CORS Isolation
The FastAPI backend uses middlewares to explicitly limit allowed origins:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["[https://yourdomain.vercel.app](https://yourdomain.vercel.app)"], # Strict Allowed Origin List
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)