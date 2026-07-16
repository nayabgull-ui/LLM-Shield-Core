# Technology Stack Rationale — LLM Shield

## 1. Core Stack Selection

| Layer | Technology | Key Rationale for Selection |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js | Provides an extremely fast client-side rendering architecture. Can be easily compiled to static files and served globally over Vercel Edge Networks. |
| **Backend** | Python / FastAPI | Extremely high throughput utilizing asynchronous programming natively. Auto-generates interactive Swagger API docs, and features built-in validation via Pydantic. |
| **Database** | Supabase (PostgreSQL) | Fully-managed PostgreSQL with enterprise-grade Row Level Security (RLS) policies. Greatly reduces backend data validation logic. |
| **API Design** | RESTful JSON API | Universally understood, easy to secure via typical reverse proxies, and strictly defined through standard OpenAPI specs. |
| **Security SAST**| Bandit | Open-source Python analyzer that automatically checks for vulnerabilities (like use of unsafe pseudo-random generators, SQL-injections, or subprocess execution). |

## 2. Why this Supports Scalability
By separating the heavy computational API processing (FastAPI) from the static assets (React), each layer can scale independently. The backend container images run statelessly on Vercel Functions, meaning they auto-scale from zero when traffic spikes without needing a managed load balancer setup.