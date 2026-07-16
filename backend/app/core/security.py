import re
import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Setup password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Heuristics for detecting Prompt Injections
SUSPICIOUS_PATTERNS = [
    # Captures: ignore/disregard/forget + all/your/system/previous + instructions/rules/guidelines/prompt
    r"(ignore|disregard|forget|bypass)\s+(all\s+|your\s+|system\s+|previous\s+)*(instructions|rules|guidelines|prompt|safety)",
    
    # Captures: override system, system override, override prompt
    r"(system\s+)?prompt\s+override",
    r"override\s+(the\s+)?(system|prompt|rules)",
    
    # Classic Jailbreaks / Persona adoption
    r"you\s+are\s+now\s+a",
    r"act\s+as",
    r"do\s+anything\s+now",
    r"dan\s+mode",
    r"jailbreak",
    
    # Developer/System mode access attempts
    r"developer\s+mode",
    r"system\s+instructions",
    r"print\s+'?system\s+hacked'?"
]
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def scan_prompt(prompt: str) -> dict:
    """
    Scans an incoming prompt for potential injection or system override attacks.
    """
    if not prompt or not prompt.strip():
        return {"safe": True, "risk_score": 0.0, "matched_patterns": []}

    matched_patterns = []
    normalized_prompt = prompt.lower()

    # Apply heuristic regex patterns
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, normalized_prompt):
            matched_patterns.append(pattern)

    num_matches = len(matched_patterns)
    if num_matches == 0:
        risk_score = 0.0
        safe = True
    elif num_matches == 1:
        risk_score = 0.4  # Medium risk
        safe = True       # Flagged but technically allowed
    else:
        risk_score = min(0.1 + (num_matches * 0.3), 1.0) # High/Critical risk
        safe = False

    return {
        "safe": safe,
        "risk_score": round(risk_score, 2),
        "matched_patterns": matched_patterns
    }