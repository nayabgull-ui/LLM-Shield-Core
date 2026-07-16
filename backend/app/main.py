import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from app.core.config import settings
from app.core.security import scan_prompt, create_access_token

# Initialize FastAPI App
app = FastAPI(title=settings.PROJECT_NAME)

# --- CORS MIDDLEWARE SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your local frontend to talk to the backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SUPABASE CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Initialize the Supabase client if keys are present
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Successfully connected to Supabase!")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")


# --- API SCHEMAS ---
class ScanRequest(BaseModel):
    prompt: str

class ScanResponse(BaseModel):
    safe: bool
    risk_score: float
    matched_patterns: list[str]

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_email: str


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "message": "Welcome to the LLM Shield API"
    }


# --- EMAIL NOTIFICATION TRIGGER (RESEND API) ---
def send_security_alert(prompt: str, risk_score: float):
    api_key = os.getenv("EMAIL_API_KEY")
    if not api_key:
        print("Skipping email alert: EMAIL_API_KEY not set in environment variables.")
        return

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Customize the recipient to your email
    payload = {
        "from": "LLM Shield Security <onboarding@resend.dev>",
        "to": "nayabgull@gmail.com",  # Replace with your actual destination email address
        "subject": "⚠️ CRITICAL SECURITY ALERT: LLM Shield Threat Blocked",
        "html": f"""
        <div style="font-family: monospace; background-color: #060913; color: #d1d5db; padding: 20px; border-radius: 8px; border: 1px solid #ef4444;">
            <h2 style="color: #ef4444; margin-top: 0;">[CRITICAL SECURITY ALERT]</h2>
            <p>The <strong>LLM Shield</strong> gateway has intercepted and blocked an injection threat.</p>
            <hr style="border-color: #1e293b; margin: 15px 0;" />
            <p><strong>Calculated Risk Score:</strong> <span style="color: #f87171; font-weight: bold;">{risk_score}</span></p>
            <p><strong>Intercepted Prompt Payload:</strong></p>
            <blockquote style="background-color: #000; padding: 10px; border-left: 3px solid #ef4444; color: #f3f4f6; margin: 10px 0;">
                {prompt}
            </blockquote>
            <p style="font-size: 11px; color: #4b5563; margin-top: 20px;">LLM SHIELD GATEWAY SENSOR // SECURE OPERATIONS CENTER</p>
        </div>
        """
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print("Security alert email dispatched successfully via Resend API!")
        else:
            print(f"Failed to send email alert. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Email dispatch error: {e}")


# --- AUTHENTICATION ENDPOINT ---
@app.post("/api/v1/auth/login", response_model=LoginResponse)
def login_endpoint(request: LoginRequest):
    if not supabase:
        raise HTTPException(
            status_code=503, 
            detail="Authentication service unavailable (Supabase not configured)"
        )
    
    try:
        # Authenticate user directly against Supabase Auth service
        auth_response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        # Extract user details
        user = auth_response.user
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
            
        # Create a local JWT access token
        access_token = create_access_token(data={"sub": user.email, "id": user.id})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_email": user.email
        }
        
    except Exception as e:
        # Return a clean error if Supabase auth fails (e.g., incorrect password)
        raise HTTPException(
            status_code=401, 
            detail=f"Authentication failed: {str(e)}"
        )


# --- THE CORE ENDPOINT (WITH DATABASE LOGGING & ALERTS!) ---
@app.post("/api/v1/shield/scan", response_model=ScanResponse)
def scan_endpoint(request: ScanRequest):
    try:
        # 1. Perform the security scan
        result = scan_prompt(request.prompt)
        
        # 2. Log the scan details into Supabase if connected
        if supabase:
            try:
                log_data = {
                    "prompt": request.prompt,
                    "safe": result["safe"],
                    "risk_score": result["risk_score"],
                    "matched_patterns": result["matched_patterns"]
                }
                # Insert row into the 'scan_logs' table
                supabase.table("scan_logs").insert(log_data).execute()
                print("Scan logged successfully to Supabase.")
            except Exception as db_err:
                # Log error locally so the API call doesn't crash if the database is down
                print(f"Database logging failed: {db_err}")
        
        # 3. Trigger Real Email Alert if threat is critical (Risk Score = 1.0)
        if result["risk_score"] >= 1.0:
            send_security_alert(request.prompt, result["risk_score"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))