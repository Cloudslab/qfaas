from qfaas.utils.logger import logger
from fastapi.openapi.utils import get_openapi
from qfaas.routes.functionRoute import router as FunctionRouter
from qfaas.dependency.auth import get_current_active_user
from qfaas.routes.authRoute import router as AuthRouter
from qfaas.routes.userRoute import router as UserRouter
from functools import lru_cache
from fastapi import Depends, FastAPI, Request

from qfaas.routes.providerRoute import router as ProviderRouter
from qfaas.routes.backendRoute import router as BackendRouter
from qfaas.routes.jobRoute import router as JobRouter

# CORs
from fastapi.middleware.cors import CORSMiddleware


# Import logger

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

origins = [
    "http://localhost.qfaas.cloud",
    "http://localhost:3000",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Router and set path operations
app.include_router(
    ProviderRouter,
    tags=["Provider"],
    prefix="/api/provider",
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    BackendRouter,
    tags=["Backend"],
    prefix="/api/backend",
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    JobRouter,
    tags=["Job"],
    prefix="/api/job",
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    UserRouter,
    tags=["User"],
    prefix="/api/user",
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    AuthRouter,
    tags=["Auth"],
    prefix="/api/auth",
)
# Root
app.include_router(
    FunctionRouter,
    tags=["Function"],
    prefix="/api/function",
    dependencies=[Depends(get_current_active_user)],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to QFaaS Core API"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="QFaaS Core API",
        version="1.0.0",
        description="OpenAPI schema for QFaaS - Quantum Function-as-a-Service framework",
        routes=app.routes,
        openapi_version="3.0.2",
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.title = "QFaaS Core API"
# Logger Test
logger.info("QFaaS Core Started!")
