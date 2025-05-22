from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage

from models.llm import LLMModel, LLMMessage

from langchain_manager.utils.history import get_session_history

from datetime import datetime

class ChatLLM:

    @staticmethod
    async def invoke(
        prompt: str,
        config: dict,
        llm: LLMModel,
    ):
        
        abliity = """
                    Currently, you have the following capabilities:
                        - Internet: Responsible for retrieving information from the internet to answer users' queries.
                        - Python: Responsible for executing code provided by users to solve their programming problems.
                    """

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""
                        You name is Sage, a large language model.
                        #Important! Use Chinese to ask questions at any time.
                        Current Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                        Current Language Model: {llm.model_name}

                        {abliity if llm.function_call else ""}

                        Answer questions using as much markdown formatting as possible.
                        Your answer should be very detailed and informative.
                        Use tables whenever possible to organize your answer in a structured way.
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

        invoke_with_config = with_message_history.with_config(
            configurable={
                "llm_temperature": 0.5,
                "deployment_name": "sage-4o",
                "llm_callbacks": [],
            }
        )

        events_stream = invoke_with_config.astream_events(
            {
                "messages": [HumanMessage(content=prompt)],
            },
            config=config,
            version="v1",
        )

        async for event in events_stream:
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content

                if content:
                    yield LLMMessage("answer", content)
