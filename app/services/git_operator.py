from git import Repo
import os
import shutil


def init_repo(local_path):
    try:
        repo = Repo.init(local_path)
        return {"status": "initialized", "path": local_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def clone_repo(repo_url, local_path):
    try:
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        Repo.clone_from(repo_url, local_path)
        return {"status": "cloned", "path": local_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def use_existing_repo(repo_url, local_path):
    if os.path.exists(local_path):
        try:
            repo = Repo(local_path)
            if repo.is_dirty(untracked_files=True):
                return {"status": "exists_dirty", "path": local_path}
            return {"status": "exists_clean", "path": local_path}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
    else:
        return clone_repo(repo_url, local_path)


def get_git_status(local_path):
    try:
        repo = Repo(local_path)
        return {
            "is_dirty": repo.is_dirty(untracked_files=True),
            "untracked_files": repo.untracked_files,
            "changed_files": [item.a_path for item in repo.index.diff(None)]
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def add_all_and_commit(local_path, message):
    try:
        repo = Repo(local_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        return {"status": "committed", "message": message}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def push_changes(local_path):
    try:
        repo = Repo(local_path)
        origin = repo.remote(name='origin')
        origin.push()
        return {"status": "pushed"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def pull_changes(local_path):
    try:
        repo = Repo(local_path)
        origin = repo.remote(name='origin')
        origin.pull()
        return {"status": "pulled"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def create_branch(local_path, branch_name):
    try:
        repo = Repo(local_path)
        new_branch = repo.create_head(branch_name)
        return {"status": "branch_created", "branch": new_branch.name}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def checkout_branch(local_path, branch_name):
    try:
        repo = Repo(local_path)
        repo.git.checkout(branch_name)
        return {"status": "branch_checked_out", "branch": branch_name}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def get_diff(local_path):
    try:
        repo = Repo(local_path)
        return repo.git.diff()
    except Exception as e:
        return {"status": "error", "detail": str(e)}
