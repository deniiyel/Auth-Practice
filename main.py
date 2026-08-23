import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in the .env file.")

# Stage 0: Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("Server running and connected to Supabase")

# Stage 5: Configure FastAPI app with Swagger UI documentation
app = FastAPI(
    title="Auth Login & Protect API",
    description="Secure API handling authentication and route protection using Supabase.",
    version="1.0.0"
)

# Stage 5: Security scheme to enable the "Authorize" padlock in Swagger UI (/docs)
security_scheme = HTTPBearer()


# --- Pydantic Request Schemas ---
class AuthCredentials(BaseModel):
    email: EmailStr
    password: str


# --- Stage 4: Reusable Dependency (Middleware) for Token Verification ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Extracts the Bearer token from the Authorization header,
    verifies it with Supabase, and returns user details.
    """
    token = credentials.credentials
    try:
        # Stage 3: Verify token with Supabase
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"}
            )
        return {"user": user_response.user, "token": token}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )


# --- Stage 2: Public Endpoint ---
@app.get("/public/info", status_code=status.HTTP_200_OK)
def public_info():
    return {"message": "Welcome stranger! This info is public."}


# --- Stage 1: Auth Endpoints ---

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthCredentials):
    """Register a new user with email and password."""
    try:
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        if not res.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Signup failed"}
            )
        return res.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )


@app.post("/auth/login", status_code=status.HTTP_200_OK)
def login(credentials: AuthCredentials):
    """Authenticate user and return JWT Access Token and Refresh Token."""
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials"}
        )


# --- Stage 4: Protected Logout Endpoint ---
@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: dict = Depends(get_current_user)):
    """Terminate the user session."""
    try:
        supabase.auth.sign_out()
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(e)}
        )


# --- Stage 3 & 4: Protected Endpoints ---

@app.get("/protected/profile", status_code=status.HTTP_200_OK)
def get_profile(current_user: dict = Depends(get_current_user)):
    """Read authenticated user profile data."""
    user = current_user["user"]
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


@app.get("/protected/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(current_user: dict = Depends(get_current_user)):
    """Check point protected route to verify reusable middleware."""
    user = current_user["user"]
    return {
        "message": f"Welcome to your private dashboard, {user.email}!",
        "status": "Authenticated"
    }