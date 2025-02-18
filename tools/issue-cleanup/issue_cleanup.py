import json
import os
import sys
from github import Github, Auth
from pydantic import Field, BaseModel

class GithubIssueCleaningRequest(BaseModel):
    owner: str = Field(..., description="The owner of the repository")
    repo: str = Field(..., description="The name of the repository")
    number: int = Field(..., description="The number of the issue")

def cleaning(req: GithubIssueCleaningRequest):
    token = os.environ.get("GITHUB_TOKEN")
    github = Github(auth=Auth.Token(token))

    client = github.get_repo(f"{req.owner}/{req.repo}")
    issue = client.get_issue(req.number)
    issue.edit(state="closed")
    issue.create_comment("closed by github issue cleanup agent.")
    return issue.raw_data

def main():
    req = json.load(sys.stdin.buffer)
    req_typed = GithubIssueCleaningRequest.model_validate(req)
    issue = cleaning(req_typed)

    print(json.dumps(issue))

if __name__ == "__main__":
    main() 