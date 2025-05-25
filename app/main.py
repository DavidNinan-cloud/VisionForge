from fastapi import FastAPI
from app.api import webhook
from app.api import code_api

app = FastAPI(
    title="Application Developer AI",
    description="Backend API to bridge GPT prompts with Git and GitHub operations",
    version="1.0.0"
)

# Include the webhook router for GPT
app.include_router(webhook.router, prefix="/api")
app.include_router(code_api.router, prefix="/api")
