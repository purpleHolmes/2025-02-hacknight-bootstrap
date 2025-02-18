# 2025-02-hacknight-bootstrap

## Prerequisite

You'll need a GitHub token for this challenge. Create your token by following
GitHub's [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

For a fine-grained token, use these settings:

- Repository access: All repositories
- Issues permission: Read and write

check more detail information in
this [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

For a classic personal access token, make sure to include the repo scope.

check more detail information in
this [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)

## Initial Setup

1. Clone the following repository - https://github.com/vessl-ai/2025-02-hacknight-bootstrap

    ```bash
    git clone https://github.com/vessl-ai/2025-02-hacknight-bootstrap.git
    cd 2025-02-hacknight-bootstrap
    ```

2. Install utilities - we need uv and orbstack
    - [uv](https://github.com/astral-sh/uv): Hyperpocket uses this as package manager.
    - [orbstack](https://docs.orbstack.dev/): Hyperpocket runs tools with this underneath.

    ```bash
    brew install uv # skip if you already have one
    brew install orbstack # to run docker container, skip if you already have simliar one.
    ```

3. Install dependencies - run the following

    ```bash
    cd 01_github_issue_cleanup_agent
    uv sync
    ```

4. Set up environment variables in `.env`
    ```shell
    OPENAI_API_KEY="your-openai-api-key"
    OPENAI_API_BASE="openai-api-base"
    MODEL_NAME="model-name"
    GITHUB_TOKEN="your-github-token"
    ```

   (optional) if you want to use deepseek or some other model, you can use fireworks inference api.
    ```shell
    OPENAI_API_KEY="your-fireworks-api-key"
    OPENAI_API_BASE="https://api.fireworks.ai/inference/v1"
    MODEL_NAME="accounts/fireworks/models/deepseek-v3"
    GITHUB_TOKEN="your-github-token"
    ```
    - more detail information [link](https://docs.fireworks.ai/getting-started/introduction)

5. Test if your agent starts well!

    ```bash
    # on `01_github_issue_agent` dir
    uv run python agent.py
    ```

## Add Tools

Go to [01_github_issue_cleanup_agent/agent.py#L16](/01_github_issue_cleanup_agent/agent.py#L16):

```python
pocket = PocketLangchain(
    tools=[
        # Add your tools here
    ])
```

You can add the following tools:

- issue-cleanup
    - cleanup your issue.
    - tool url: https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/issue-cleanup
- list-issues
    - lists the github issues for a repository
    - tool url: https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/list-issues

```python
pocket = PocketLangchain(
    tools=[
        ("https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/list-issues",
         {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}),
        ("https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/issue-cleanup",
         {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")})
    ])
```

- the dictionary values will be sent into runtime environment.

Run again and play with the agent.

## Add predefined tools to your agent and build some cool stuff

You can see the list of Hyperpocket managed tools in https://github.com/vessl-ai/hyperpocket/tree/main/tools.

1. Create your directory as <TEAMNAME_AGENTNAME> and copy upper example(github_issue_cleanup_agent) into it.

2. Tune system prompt and add tools to the agent.

- [System prompt region](/01_github_issue_cleanup_agent/agent.py#L28)

- Tool region is the same as the previous example.

3. Run the agent and see the magic.

## Create your own tools and add them to the agent

To add a custom tool, follow the docs https://vessl-ai.github.io/hyperpocket/tools/using-function-tools.html

