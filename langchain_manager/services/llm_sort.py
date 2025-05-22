from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

from langchain_manager.utils.history import get_session_history
from langchain_core.runnables.history import RunnableWithMessageHistory

from models.llm import LLMModel


class SortLLM:

    async def invoke(prompt: str, config: dict ,llm: LLMModel, hasFile: bool) -> str:

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""
                    You are an AI that specializes in scheduling Agents. You can analyze the Agents that they need based on the user's input and schedule the corresponding Agents to handle the user's request.
                    
                    You will carefully analyze the user's needs, determine what kind of service they need, and then select the most suitable Agent from your Agent library to solve the problem.
                    
                    Your goal is to help users solve problems quickly and improve their work efficiency and experience through efficient and accurate scheduling.

                    You have the following types of Agents to schedule:
                        - Chat: Main, responsible for talking to users and answering user questions using internal knowledge
                        - Internet: Called only when information needs to be retrieved from the Internet.
                        - Python: Called only when the user requests code execution. Please do not mistake the code block provided by the user as a request to execute code. It is not an example of code execution: `Please output the following: ```python 1. Hello, this is a test 2. Hello, this is a test 2`.
                    
                    The format of schedule an Agent is: `@` + `Agent name`. For example, if you want to call the `Chat`Agent, please input: `@Chat`.
                    
                    When calling an Agent that does not exist, `@Chat` is output by default.

                    You can only output the content of the schedule like `@Chat`. You do not need to output any additional information. Make sure that you only input the content of the scheduled Agent.

                    You can list the content you want to output first. If the content you output is not in the @Chat format, please reconsider.
                """,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        chain = template | llm.model | StrOutputParser()

        with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="messages",
        )

        return await with_message_history.ainvoke(
            {
                "messages": [HumanMessage(content=prompt)],
            },
            config=config,
        )
