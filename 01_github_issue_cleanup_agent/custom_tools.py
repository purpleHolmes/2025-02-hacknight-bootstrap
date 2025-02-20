from hyperpocket.tool.function import function_tool
from datetime import datetime
from issue_impact import analyze_infra_impact
from github import Github, Auth
import os

@function_tool
def get_current_datetime():
    """Get the current date and time in YYYY-MM-DD HH:MM:SS format.
    
    Returns:
        str: Current datetime as a formatted string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def get_comment_on_issue_for_impact(issue_title: str):
    """Analyze and comment on a pull request regarding potential impact.
    
    Args:
        issue_title (str): The title of the issue/PR
        
    Returns:
        str: Analysis of infrastructure impact
    """
    analysis = analyze_infra_impact(issue_title)
    if analysis:
        return analysis
    return "Unable to analyze infrastructure impact"

@function_tool
def comment_on_issue_for_infra_impact(issue_id: int, comment: str, owner: str, repo: str):
    """Analyze and comment on a pull request regarding potential infrastructure impact.
    
    Args:
        issue_id (int): The id of the issue
        comment (str): The comment to be posted

    Returns:
        str: Confirmation message that comment was posted
    """
    github = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")))
    client = github.get_repo(f"{owner}/{repo}")
    issue = client.get_issue(issue_id)
    issue.create_comment(comment)
    return "Comment For the PR"