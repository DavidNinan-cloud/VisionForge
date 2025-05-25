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

def commit_file_to_repo(repo_name, file_path, content, commit_message):
    try:
        repo = user.get_repo(repo_name)
        existing = None
        try:
            existing = repo.get_contents(file_path)
        except:
            pass  # File doesn't exist yet

        if existing:
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=existing.sha
            )
        else:
            repo.create_file(
                path=file_path,
                message=commit_message,
                content=content
            )
        return {"status": "success", "file": file_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def summarize_repo(repo_name):
    try:
        repo = user.get_repo(repo_name)
        files = repo.get_contents("")

        summary = []
        for file in files:
            if file.type == "file":
                summary.append(f"📄 {file.name}")
            elif file.type == "dir":
                summary.append(f"📁 {file.name}/ (folder)")

        return {
            "status": "success",
            "repo": repo.full_name,
            "summary": summary
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def get_file_content(repo_name, file_path):
    try:
        repo = user.get_repo(repo_name)
        file = repo.get_contents(file_path)
        content = file.decoded_content.decode("utf-8")
        return {"status": "success", "filename": file_path, "content": content}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def list_repo_files(repo_name, path="", extension_filter=""):
    try:
        repo = user.get_repo(repo_name)
        contents = repo.get_contents(path)
        result = []

        for item in contents:
            if item.type == "file":
                if extension_filter == "" or item.name.endswith(extension_filter):
                    result.append({"path": item.path, "type": "file"})
            elif item.type == "dir":
                result.extend(list_repo_files(repo_name, path=item.path, extension_filter=extension_filter))

        return result
    except Exception as e:
        return [{"error": str(e)}]
