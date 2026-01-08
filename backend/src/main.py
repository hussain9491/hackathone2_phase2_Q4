
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
from .database import init_db

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is not required

# Context manager for application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await init_db()
    yield
    # Cleanup on shutdown if needed
    pass

# Create FastAPI app
app = FastAPI(
    title="Multi-User Todo API",
    description="API for multi-user todo application",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Multi-User Todo API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# -------------------------------
# Swagger / OpenAPI Security Setup
# -------------------------------
bearer_scheme = HTTPBearer(scheme_name="Bearer")

# Import routers
from .routers import auth, tasks
app.include_router(auth.router)
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

# Optional: Add global security requirement in OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    import json
    from fastapi.openapi.utils import get_openapi

    # Use the original get_openapi function to avoid recursion
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        servers=app.servers,
    )

    # Add Bearer token globally (Swagger UI will show Authorize)
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # Apply BearerAuth to task routes (not to auth routes, root, or health check)
    for path_pattern, path_item in openapi_schema["paths"].items():
        for operation in path_item.values():
            if isinstance(operation, dict):
                # Check if this is an auth route by looking at tags
                if "tags" in operation and "auth" in operation["tags"]:
                    # Auth routes don't need additional security schemes
                    continue
                # Root and health endpoints don't need auth
                elif path_pattern in ["/", "/health"]:
                    continue
                else:
                    # Apply security to all other routes (like task routes)
                    operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
