from git import Repo


def has_changes(local_path):
    try:
        repo = Repo(local_path)
        return repo.is_dirty(untracked_files=True)
    except Exception:
        return False


def get_file_diff(local_path):
    try:
        repo = Repo(local_path)
        return repo.git.diff()
    except Exception as e:
        return f"Error generating diff: {str(e)}"


def get_changed_files(local_path):
    try:
        repo = Repo(local_path)
        changed = [item.a_path for item in repo.index.diff(None)]
        untracked = repo.untracked_files
        return {"changed": changed, "untracked": untracked}
    except Exception as e:
        return {"error": str(e)}
