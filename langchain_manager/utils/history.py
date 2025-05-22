
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


store = {}

@staticmethod
def get_session_history(
    topic_id: str, history_list: dict = None, is_new_chat: bool = False
) -> BaseChatMessageHistory:
    if is_new_chat or history_list is not None:
        store[topic_id] = ChatMessageHistory()

    if history_list:
        store[topic_id] = ChatMessageHistory()
        for history in history_list:

            prompt = history.get("prompt")
            prompt_message = HumanMessage(content=prompt)
            store[topic_id].add_message(prompt_message)

            answer = history.get("answer")
            if not answer:
                answer = "Empty answer"
            answer_message = AIMessage(content=answer)
            store[topic_id].add_message(answer_message)

    return store[topic_id]
