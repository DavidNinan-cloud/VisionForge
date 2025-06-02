from fastapi import APIRouter, HTTPException,Request
from app.api.schemas import GPTCommandRequest
from app.services import github_operator, git_operator
import os

router = APIRouter()

BASE_PATH = os.getenv("BASE_REPO_PATH", "/tmp/projects")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@router.post("/webhook")

async def handle_gpt_command(command: GPTCommandRequest):
    action = command.action
    params = command.params or {}

    if not action:
        raise HTTPException(status_code=400, detail="Missing 'action' in payload.")

    def use_repo_handler():
        return git_operator.use_existing_repo(
            repo_url=params["repo_url"],
            local_path=os.path.join(BASE_PATH, params["folder_name"])
        )

    def create_branch_handler():
        return git_operator.create_branch(
            local_path=params["repo_path"],
            branch_name=params["branch_name"]
        )

    def checkout_branch_handler():
        return git_operator.checkout_branch(
            local_path=params["repo_path"],
            branch_name=params["branch_name"]
        )

    def commit_and_push_handler():
        commit_result = git_operator.add_all_and_commit(
            local_path=params["repo_path"],
            message=params["message"]
        )
        if commit_result.get("status") != "committed":
            return commit_result
        return git_operator.push_changes(params["repo_path"])

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

    # Dispatch dictionary
    action_map = {
        "create_repo": lambda: github_operator.create_repo(**params),
        "create_pull_request": lambda: github_operator.create_pull_request(**params),
        "validate_repo_url": lambda: {"valid": github_operator.validate_repo_url(**params)},
        "use_repo": use_repo_handler,
        "create_branch": create_branch_handler,
        "checkout_branch": checkout_branch_handler,
        "commit_and_push": commit_and_push_handler,
        "get_status": lambda: git_operator.get_git_status(params["repo_path"]),
        "commit_file_to_repo": lambda: github_operator.commit_file_to_repo(
            repo_name=params["repo_name"],
            file_path=params["file_path"],
            content=params["content"],
            commit_message=params["commit_message"]
        ),
        "summarize_repo": lambda: github_operator.summarize_repo(params["repo_name"]),
        "summarize_file": summarize_file_handler,
    }

    handler = action_map.get(action)
    if handler:
        return handler()

    raise HTTPException(status_code=400, detail=f"Unknown action: {action}")