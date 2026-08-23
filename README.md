(

echo # Auth Login ^\& Protect API

echo.

echo A secure REST API built with FastAPI and Supabase Auth featuring JWT verification and Swagger UI bearer token support.

echo.

echo ## API Reference

echo.

echo ^| Method ^| Endpoint ^| Auth Required ^| Description ^|

echo ^| --- ^| --- ^| --- ^| --- ^|

echo ^| POST ^| /auth/signup ^| No ^| Register a new user ^|

echo ^| POST ^| /auth/login ^| No ^| Authenticate user ^\& return JWT ^|

echo ^| POST ^| /auth/logout ^| Yes ^| Terminate session ^|

echo ^| GET ^| /public/info ^| No ^| Access public data ^|

echo ^| GET ^| /protected/profile ^| Yes ^| Read authenticated user profile ^|

echo ^| GET ^| /protected/dashboard ^| Yes ^| Read protected dashboard details ^|

echo.

echo ## How to Run

echo.

echo 1. Clone repository and create a `.env` file with `SUPABASE\_URL` and `SUPABASE\_KEY`.

echo 2. Run `pip install -r requirements.txt`

echo 3. Start server: `uvicorn main:app --reload --port 8000`

echo 4. Access Interactive Docs: `http://localhost:8000/docs`

) > README.md

