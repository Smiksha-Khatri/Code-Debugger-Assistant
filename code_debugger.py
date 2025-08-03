import openai
import subprocess
import os
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------- 1. Run a Python script and capture errors ----------- #
def run_python_script(file_path):
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "Error: Script execution timed out."


# ----------- 2. Use OpenAI to analyze and suggest fix ----------- #
def debug_with_openai(code, error_message):
    print("\n🧠 Sending error to GPT for analysis...")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a code debugging assistant. Your job is to fix the code based on errors."},
            {"role": "user", "content": f"The following Python code caused an error:\n\n{code}\n\nThe error was:\n\n{error_message}\n\nPlease explain the error and suggest a corrected version of the code."}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# ----------- 3. Main function ----------- #
def main():
    file_path = input("Enter path to Python script (e.g., test_script.py): ")

    if not os.path.isfile(file_path):
        print("❌ File not found.")
        return

    with open(file_path, 'r') as f:
        code = f.read()

    print("\n🚀 Running script...\n")
    stdout, stderr = run_python_script(file_path)

    if stderr:
        print("❌ Error detected:\n", stderr)
        gpt_response = debug_with_openai(code, stderr)
        print("\n✅ GPT Suggestion:\n", gpt_response)
    else:
        print("✅ Script ran successfully!\nOutput:\n", stdout)


if __name__ == "__main__":
    main()
