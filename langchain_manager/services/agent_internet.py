from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool


from models.llm import LLMModel, LLMMessage, LLMStatus

from langchain_manager.utils.history import get_session_history

from datetime import datetime
import json
import uuid


class InternetLLM:
    async def invoke(
        prompt: str,
        config: dict,
        llm: LLMModel,
        search_model: LLMModel,
    ):

        @tool
        def internet_tool(query: str):
            """Tool to search the internet"""

            tool_call = {
                "args": {"query": f"{query}"},
                "id": f"{uuid.uuid4()}",
                "name": f"{search_model.model_name}",
                "type": "tool_call",
            }

            print(tool_call)

            return search_model.model.invoke(tool_call).artifact

        tools = [internet_tool]

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""
                        Today's date is: {datetime.now().strftime("%Y-%m-%d")}

                        You are an intelligent assistant that can help users answer questions by searching the Internet. Your task is to identify the key points in the user's question and generate queries that can verify these key points to ensure that the information is accurate. To do this, you need to:

                         - Understand the user's needs: clarify the user's core question and think deeply about the details they may want to know, covering implicit assumptions.
                        
                         - If it is about real-time information, make sure you include the current date when searching. If it is historical information, please be sure to tell the user
                        
                         - Refine the search: you can use tool multiple times to get more accurate search results if the first search does not provide enough information.
                                                
                         - Add additional information: While answering the question, provide relevant additional context or suggestions to help users fully understand all aspects of the problem.
                        
                        Remember, your task is to ensure that users can quickly get useful information without directly seeing the query process or citing the source you generated.

                        There is no need to output the reference source of the search results to users because the system has already displayed it.

                        Use Markdown to format your response and use tables whenever possible make sure the format is clear and easy to read.

                    """,
                ),
                MessagesPlaceholder(variable_name="messages"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

        agent = create_tool_calling_agent(llm.model, tools, template)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        with_message_history = RunnableWithMessageHistory(
            agent_executor,
            get_session_history,
            input_messages_key="messages",
        )

        events_stream = with_message_history.astream_events(
            {
                "messages": [HumanMessage(content=prompt)],
            },
            config=config,
            version="v2",
        )

        async for event in events_stream:
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield LLMMessage("answer", content)

            elif kind == "on_tool_start":
                yield LLMStatus("status", "[Start]")

            elif kind == "on_tool_error":
                yield LLMStatus("error", "[Error]")

            elif kind == "on_tool_end":
                tool_data = event["data"].get("output")

                if type(tool_data) == str:

                    tool_data = tool_data.replace("'", '"')
                    tool_data = json.loads(tool_data)

                if search_model.results_path is not None:
                    tool_data = tool_data[search_model.results_path]

                for entry in tool_data:

                    url = entry[search_model.url_keyword]
                    title = entry[search_model.title_keyword]
                    content = entry[search_model.content_keyword]

                    print(title)
                    yield LLMStatus(
                        "internet",
                        json.dumps(
                            {
                                "url": url,
                                "title": title,
                                "content": content,
                            },
                        ),
                    )
