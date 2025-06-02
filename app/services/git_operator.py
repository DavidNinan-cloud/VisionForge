from git import Repo
import os
import shutil

def format_success(data):
    return {"status": "success", "data": data}

def format_error(e):
    return {"status": "error", "error": str(e)}


def init_repo(local_path):
    try:
        Repo.init(local_path)
        return format_success({"path": local_path})
    except Exception as e:
        return format_error(e)


def clone_repo(repo_url, local_path):
    try:
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        Repo.clone_from(repo_url, local_path)
        return format_success({"path": local_path})
    except Exception as e:
        return format_error(e)


def use_existing_repo(repo_url, local_path):
    if os.path.exists(local_path):
        try:
            repo = Repo(local_path)
            status = "dirty" if repo.is_dirty(untracked_files=True) else "clean"
            return format_success({"path": local_path, "status": status})
        except Exception as e:
            return format_error(e)
    else:
        return clone_repo(repo_url, local_path)


def get_git_status(local_path):
    try:
        repo = Repo(local_path)
        return format_success({
            "is_dirty": repo.is_dirty(untracked_files=True),
            "untracked_files": repo.untracked_files,
            "changed_files": [item.a_path for item in repo.index.diff(None)]
        })
    except Exception as e:
        return format_error(e)


def add_all_and_commit(local_path, message):
    try:
        repo = Repo(local_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        return format_success({"message": message})
    except Exception as e:
        return format_error(e)


def push_changes(local_path):
    try:
        repo = Repo(local_path)
        origin = repo.remote(name='origin')
        origin.push()
        return format_success({"pushed": True})
    except Exception as e:
        return format_error(e)


def pull_changes(local_path):
    try:
        repo = Repo(local_path)
        origin = repo.remote(name='origin')
        origin.pull()
        return format_success({"pulled": True})
    except Exception as e:
        return format_error(e)


def create_branch(local_path, branch_name):
    try:
        repo = Repo(local_path)
        new_branch = repo.create_head(branch_name)
        return format_success({"branch": new_branch.name})
    except Exception as e:
        return format_error(e)


def checkout_branch(local_path, branch_name):
    try:
        repo = Repo(local_path)
        repo.git.checkout(branch_name)
        return format_success({"branch": branch_name})
    except Exception as e:
        return format_error(e)


def get_diff(local_path):
    try:
        repo = Repo(local_path)
        diff_text = repo.git.diff()
        return format_success({"diff": diff_text})
    except Exception as e:
        return format_error(e)


