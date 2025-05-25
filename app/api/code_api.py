from fastapi import APIRouter
from app.services import github_operator

router = APIRouter()

@router.get("/code/files")
async def list_repo_files(repo_name: str, filter: str = ""):
    return github_operator.list_repo_files(repo_name=repo_name, extension_filter=filter)


@router.get("/code/file")
async def get_single_file(repo_name: str, file_path: str):
    return github_operator.get_file_content(repo_name, file_path)

@router.get("/code/all")
async def get_all_code(repo_name: str, filter: str = ""):
    files = github_operator.list_repo_files(repo_name, extension_filter=filter)
    result = []

    MAX_FILE_SIZE = 50 * 1024      # 50 KB
    MAX_TOTAL_SIZE = 500 * 1024    # 500 KB

    total_size = 0

    for file in files:
        if file.get("type") == "file" and "path" in file:
            content_result = github_operator.get_file_content(repo_name, file["path"])
            
            if content_result.get("status") != "success":
                continue

            content = content_result["content"]
            content_size = len(content.encode("utf-8"))

            if content_size > MAX_FILE_SIZE:
                result.append({
                    "path": file["path"],
                    "skipped": True,
                    "reason": f"File exceeds {MAX_FILE_SIZE // 1024}KB limit"
                })
                continue

            if total_size + content_size > MAX_TOTAL_SIZE:
                result.append({
                    "path": file["path"],
                    "skipped": True,
                    "reason": "Total size limit exceeded"
                })
                break

            result.append({
                "path": file["path"],
                "content": content
            })

            total_size += content_size

    return {
        "status": "success",
        "total_files": len(result),
        "total_bytes": total_size,
        "files": result
    }
