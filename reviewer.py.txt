import os
import requests
import openai

# 🔐 Load OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_pr_diff(owner, repo, pr_number):
    """
    Fetches the .diff file for a given PR from GitHub.
    """
    url = f"https://patch-diff.githubusercontent.com/raw/{owner}/{repo}/pull/{pr_number}.diff"
    headers = {"Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def review_code(diff_text, guidelines_text=None):
    """
    Sends the code diff to OpenAI and gets review feedback.
    Optionally includes team guidelines for contextual improvement.
    """
    prompt = f"""
You are a senior code reviewer. Review the following code diff and suggest specific, constructive improvements.
Go beyond static analysis—focus on logic, readability, maintainability, and context.

{f'Team Guidelines:\n{guidelines_text}\n' if guidelines_text else ''}
Code Diff:
{diff_text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert software engineer and reviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    owner = "your-github-username"       # 🔄 Replace with actual GitHub username
    repo = "your-repo-name"              # 🔄 Replace with actual repository name
    pr_number = 1                        # 🔄 Replace with actual PR number

    try:
        diff = get_pr_diff(owner, repo, pr_number)
        # Optionally add guidelines (e.g., from guidelines.md file)
        guidelines = None
        feedback = review_code(diff, guidelines)
        print("\n🧠 AI Code Review Feedback:\n")
        print(feedback)
    except Exception as e:
        print(f"🚨 Error fetching or reviewing code: {e}")
