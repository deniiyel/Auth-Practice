(
echo import os
echo from dotenv import load_dotenv
echo from fastapi import FastAPI, Depends, HTTPException, status
echo from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
echo from pydantic import BaseModel, EmailStr
echo from supabase import create_client, Client
echo.
echo load_dotenv^(^)
echo.
echo SUPABASE_URL = os.getenv^("SUPABASE_URL"^)
echo SUPABASE_KEY = os.getenv^("SUPABASE_KEY"^)
echo.
echo if not SUPABASE_URL or not SUPABASE_KEY:
echo     raise RuntimeError^("SUPABASE_URL and SUPABASE_KEY must be set in .env"^)
echo.
echo supabase: Client = create_client^(SUPABASE_URL, SUPABASE_KEY^)
echo print^("Server running and connected to Supabase"^)
echo.
echo app = FastAPI^(title="Auth Login ^& Protect API", version="1.0.0"^)
echo security_scheme = HTTPBearer^(^)
echo.
echo class AuthCredentials^(BaseModel^):
echo     email: EmailStr
echo     password: str
echo.
echo def get_current_user^(credentials: HTTPAuthorizationCredentials = Depends^(security_scheme^)^):
echo     token = credentials.credentials
echo     try:
echo         user_response = supabase.auth.get_user^(token^)
echo         if not user_response or not user_response.user:
echo             raise HTTPException^(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid or expired token"}^)
echo         return {"user": user_response.user, "token": token}
echo     except Exception:
echo         raise HTTPException^(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid or expired token"}^)
echo.
echo @app.get^("/public/info", status_code=status.HTTP_200_OK^)
echo def public_info^(^):
echo     return {"message": "Welcome stranger! This info is public."}
echo.
echo @app.post^("/auth/signup", status_code=status.HTTP_201_CREATED^)
echo def signup^(credentials: AuthCredentials^):
echo     try:
echo         res = supabase.auth.sign_up^({"email": credentials.email, "password": credentials.password}^)
echo         if not res.user:
echo             raise HTTPException^(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Signup failed"}^)
echo         return res.user
echo     except Exception as e:
echo         raise HTTPException^(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": str^(e^)}^)
echo.
echo @app.post^("/auth/login", status_code=status.HTTP_200_OK^)
echo def login^(credentials: AuthCredentials^):
echo     try:
echo         res = supabase.auth.sign_in_with_password^({"email": credentials.email, "password": credentials.password}^)
echo         return {"access_token": res.session.access_token, "refresh_token": res.session.refresh_token, "token_type": "bearer"}
echo     except Exception:
echo         raise HTTPException^(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": "Invalid login credentials"}^)
echo.
echo @app.post^("/auth/logout", status_code=status.HTTP_204_NO_CONTENT^)
echo def logout^(current_user: dict = Depends^(get_current_user^)^):
echo     try:
echo         supabase.auth.sign_out^(^)
echo         return None
echo     except Exception as e:
echo         raise HTTPException^(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": str^(e^)}^)
echo.
echo @app.get^("/protected/profile", status_code=status.HTTP_200_OK^)
echo def get_profile^(current_user: dict = Depends^(get_current_user^)^):
echo     user = current_user["user"]
echo     return {"id": user.id, "email": user.email, "created_at": user.created_at}
echo.
echo @app.get^("/protected/dashboard", status_code=status.HTTP_200_OK^)
echo def get_dashboard^(current_user: dict = Depends^(get_current_user^)^):
echo     user = current_user["user"]
echo     return {"message": f"Welcome to your private dashboard, {user.email}!", "status": "Authenticated"}
) > main.py