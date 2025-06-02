from fastapi import APIRouter, HTTPException, Request
from app.api.schemas import GPTCommandRequest
from app.services import github_operator
import os

router = APIRouter()


@router.post("/webhook")

async def handle_gpt_command(command: GPTCommandRequest):
    action = command.action
    params = command.params or {}

    if not action:
        raise HTTPException(status_code=400, detail="Missing 'action' in payload.")

    def summarize_file_handler():
        file_data = github_operator.get_file_content(
            repo_name=params["repo_name"],
            file_path=params["file_path"]
        )
        if file_data["status"] != "success":
            return file_data
        return {
            "status": "error",
            "detail": "summarize_file_with_gpt functionality is not available."
        }

    # Dispatch dictionary (GitHub-only)
    action_map = {
        "get_repo_url": lambda params=params: github_operator.get_repo_url(params["repo_name"]),
        "create_repo": lambda params=params: github_operator.create_repo(**params),
        "create_pull_request": lambda params=params: github_operator.create_pull_request(**params),
        "validate_repo_url": lambda params=params: {"valid": github_operator.validate_repo_url(**params)},
        "commit_file_to_repo": lambda params=params: github_operator.commit_file_to_repo(
            repo_name=params["repo_name"],
            file_path=params["file_path"],
            content=params["content"],
            commit_message=params["commit_message"]
        ),
        "summarize_repo": lambda params=params: github_operator.summarize_repo(params["repo_name"]),
        "summarize_file": summarize_file_handler,
        "get_file_content": lambda params=params: github_operator.get_file_content(
            repo_name=params["repo_name"],
            file_path=params["file_path"]
        ),
        "list_repo_files": lambda params=params: github_operator.list_repo_files(
            repo_name=params["repo_name"]
        ),
        "list_repos": lambda: github_operator.list_repos(),
    }
    handler = action_map.get(action)
    if handler:
        return handler(params)

    raise HTTPException(status_code=400, detail=f"Unknown action: {action}")