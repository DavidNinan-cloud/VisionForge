from fastapi import APIRouter, HTTPException,Request
from app.api.schemas import GPTCommandRequest
from app.services import github_operator, git_operator, code_generator
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

    # GitHub operations
    if action == "create_repo":
        return github_operator.create_repo(**params)

    if action == "create_pull_request":
        return github_operator.create_pull_request(**params)

    if action == "validate_repo_url":
        return {"valid": github_operator.validate_repo_url(**params)}

    # Git operations
    if action == "use_repo":
        return git_operator.use_existing_repo(
            repo_url=params["repo_url"],
            local_path=os.path.join(BASE_PATH, params["folder_name"])
        )

    if action == "create_branch":
        return git_operator.create_branch(
            local_path=params["repo_path"],
            branch_name=params["branch_name"]
        )

    if action == "checkout_branch":
        return git_operator.checkout_branch(
            local_path=params["repo_path"],
            branch_name=params["branch_name"]
        )

    if action == "commit_and_push":
        return git_operator.add_all_and_commit(
            local_path=params["repo_path"],
            message=params["message"]
        ) or git_operator.push_changes(params["repo_path"])

    if action == "get_status":
        return git_operator.get_git_status(params["repo_path"])

    # Code generation
    if action == "generate_file":
        return code_generator.generate_file(
            prompt=params["prompt"],
            file_path=params["file_path"]
        )

    if action == "update_file":
        return code_generator.update_file_with_prompt(
            prompt=params["prompt"],
            file_path=params["file_path"]
        )

    if action == "summarize_diff":
        return code_generator.summarize_diff(params["diff"])
    
    if action == "commit_file_to_repo":
        return github_operator.commit_file_to_repo(
            repo_name=params["repo_name"],
            file_path=params["file_path"],
            content=params["content"],
            commit_message=params["commit_message"]
        )
    
    if action == "summarize_repo":
        return github_operator.summarize_repo(params["repo_name"])

    if action == "summarize_file":
        file_data = github_operator.get_file_content(
            repo_name=params["repo_name"],
            file_path=params["file_path"]
        )
        if file_data["status"] != "success":
            return file_data
        return code_generator.summarize_file_with_gpt(
            content=file_data["content"],
            filename=params["file_path"]
        )


    raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
