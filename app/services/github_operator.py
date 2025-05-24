from github import Github
import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
github = Github(GITHUB_TOKEN)
user = github.get_user()


def create_repo(name, description="", private=True):
    try:
        repo = user.create_repo(name=name, description=description, private=private)
        return {"status": "success", "repo_url": repo.clone_url}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def create_pull_request(repo_name, head, base, title, body=""):
    try:
        repo = user.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return {"status": "success", "pr_url": pr.html_url}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def list_repos():
    try:
        return [repo.full_name for repo in user.get_repos()]
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def delete_repo(repo_name):
    try:
        repo = user.get_repo(repo_name)
        repo.delete()
        return {"status": "success", "message": f"Deleted {repo_name}"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def get_repo_url(repo_name):
    try:
        repo = user.get_repo(repo_name)
        return {"url": repo.clone_url}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def validate_repo_url(repo_url, token=GITHUB_TOKEN):
    if "github.com" not in repo_url:
        return False

    try:
        parts = repo_url.replace("https://github.com/", "").rstrip("/").split("/")
        if len(parts) != 2:
            return False
        owner, repo = parts
        api_url = f"https://api.github.com/repos/{owner}/{repo}"

        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(api_url, headers=headers)
        return response.status_code == 200
    except Exception:
        return False
