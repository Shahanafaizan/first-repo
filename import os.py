import os
import requests
import openai

openai.api_key = os.getenv("3416730d0b2e084a1fa918f4123b2f98b6360904724fe84fd2d93fac0da9e06c")

def get_pr_diff(owner, repo, pr_number):
    url = f"https://patch-diff.githubusercontent.com/raw/{owner}/{repo}/pull/{pr_number}.diff"
    headers = {"Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def review_code(diff_text):
    prompt = f"Review the following code diff and suggest improvements:\n\n{diff_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior code reviewer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    owner = "your-github-username"
    repo = "your-repo-name"
    pr_number = 1  # Replace with actual PR number

    diff = get_pr_diff(owner, repo, pr_number)
    feedback = review_code(diff)
    print("\n🧠 AI Code Review Feedback:\n")
    print(feedback)
