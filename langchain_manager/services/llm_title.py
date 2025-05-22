from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage


from models.llm import LLMModel


class TitleLLM:

    async def invoke(prompt: str, answer: str, llm: LLMModel) -> str:

        title_generation_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                You are an AI responsible for generating titles. Your task is to generate a concise, attractive and relevant title for the following given context.

                Please pay attention to the following points:
                    - Conciseness: The title should be as short as possible, no more than 10 words.
                    - Relevance: The title must be highly relevant to the context provided.
                    - Attractiveness: The title should be attractive and arouse the reader's interest.
                    - Clarity: The title should clearly express the main content or theme of the article or paragraph.
                    - No punctuation is allowed. Please check your title for punctuation before you output it. If it does, you need to rethink it. Titles should not contain any punctuation.
                    - The title should be in Chinese.

                Example: If the context is about the application of AI in the medical field, you can generate a title such as "AI Revolutionizes Healthcare".
                
                Finally, please generate a suitable title according to the above detailed requirements.

                When you don't know how to generate a title, please output the title as `未命名标题`。
                

                The following is a contextual dialogue between User and AI:.
                """,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        title_generation_chain = (
            title_generation_prompt
            | llm.model
            | StrOutputParser()
        )

        title = await title_generation_chain.ainvoke({
                "messages": [HumanMessage(content=f"User: {prompt}, AI: {answer}")],
            })
        return title[:30]
