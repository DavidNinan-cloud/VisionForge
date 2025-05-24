from fastapi import FastAPI
from app.api import webhook

app = FastAPI(
    title="Application Developer AI",
    description="Backend API to bridge GPT prompts with Git and GitHub operations",
    version="1.0.0"
)

# Include the webhook router for GPT
app.include_router(webhook.router, prefix="/api")
