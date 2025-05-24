import os
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Define default host and port
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
