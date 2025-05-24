import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_file(prompt, file_path):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Python backend code assistant."},
                {"role": "user", "content": f"Generate a code file:\n\n{prompt}"}
            ]
        )
        code = response.choices[0].message.content

        with open(file_path, "w") as f:
            f.write(code)

        return {"status": "file_generated", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def update_file_with_prompt(prompt, file_path):
    try:
        with open(file_path, "r") as f:
            original_code = f.read()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a backend code refactorer."},
                {"role": "user", "content": f"Here is the original code:\n{original_code}\n\nUpdate it to:\n{prompt}"}
            ]
        )
        updated_code = response.choices[0].message.content

        with open(file_path, "w") as f:
            f.write(updated_code)

        return {"status": "file_updated", "file_path": file_path}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def summarize_diff(diff_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a git diff summarizer."},
                {"role": "user", "content": f"Summarize this git diff for a commit message:\n{diff_text}"}
            ]
        )
        summary = response.choices[0].message.content
        return {"status": "success", "summary": summary}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
