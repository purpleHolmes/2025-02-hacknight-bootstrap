from hyperpocket.tool.function import function_tool
from datetime import datetime

@function_tool
def get_current_datetime():
    """function to get current datetime"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def comment_on_pr_for_infra_impact(pr_number: int, comment: str):
    """function to comment on a pull request for infra impact"""
    print(f"Commenting on PR {pr_number} with comment: {comment}")
    return "Commented on PR for infra impact"
