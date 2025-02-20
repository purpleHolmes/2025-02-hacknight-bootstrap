import os

from dotenv import load_dotenv
from hyperpocket_langchain import PocketLangchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from custom_tools import get_current_datetime, get_comment_on_issue_for_impact, comment_on_issue_for_infra_impact


load_dotenv()


def agent():
    pocket = PocketLangchain(
        tools=[
            # Add your tools here
            get_current_datetime,
            get_comment_on_issue_for_impact,
            comment_on_issue_for_infra_impact,
            ("https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/issue-cleanup", {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}),
            ("https://github.com/vessl-ai/2025-02-hacknight-bootstrap/tree/main/tools/list-issues", {"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}),
           
        ])
    tools = pocket.get_tools()
    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            (
                "system",
                "You are a tool calling assistant. You can help the user by calling proper tools",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )

    print("\n\n\n")
    print("Hello, this is github cleaning agent.")
    while True:
        print("user(q to quit) : ", end="")
        user_input = input()
        if user_input == "q":
            print("Good bye!")
            break
        elif user_input == "":
            continue

        response = agent_executor.invoke({"input": user_input})
        print("agent : ", response["output"])
        print()


if __name__ == "__main__":
    agent()
