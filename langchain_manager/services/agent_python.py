from langchain_core.tools import tool

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain_manager.utils.history import get_session_history

from models.llm import LLMModel, LLMMessage, LLMStatus

from config.model import PYTHON_SAVE_DIR, IMAGE_SAVE_DIR

from langchain_manager.utils.jupyter import Jupyter

import os
import uuid
from concurrent.futures import ThreadPoolExecutor
import traceback
import aiofiles
import subprocess
import asyncio
import base64

from models.llm import LLMModel


class PythonLLM:


    operating_system = os.name

    async def python_run(
        prompt: str,
        config: dict,
        llm: LLMModel,
    ):

        code_id = str(uuid.uuid4())

        @tool
        async def execute_code(code: str) -> str:
            """Execute the code asynchronously."""

            os.makedirs(
                PYTHON_SAVE_DIR, exist_ok=True
            ) 
            filename = os.path.join(PYTHON_SAVE_DIR, f"{code_id}.py")
            print(f"Saving code to file: {filename}")
            async with aiofiles.open(filename, "w", encoding="utf-8") as file:
                await file.write(code)

            def run_subprocess():
                try:

                    conda_python_path = os.path.expanduser("~/miniconda3/bin/python") 
                    if os.name == "nt": 
                        conda_python_path = os.path.expanduser("~python.exe")


                    process = subprocess.Popen(
                        [conda_python_path, filename],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                    )
                    try:
                        stdout, stderr = process.communicate(timeout=60)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        stdout, stderr = process.communicate()
                        return "[Tool] Task timeout: process was killed after 60 seconds."

                    if process.returncode == 0:
                        return stdout
                    else:
                        return stderr
                except Exception as e:
                    return str(e)

            try:
                loop = asyncio.get_running_loop()
                with ThreadPoolExecutor() as pool:
                    output_content = await loop.run_in_executor(pool, run_subprocess)

                output_filename = os.path.join(PYTHON_SAVE_DIR, f"{code_id}.txt")
                async with aiofiles.open(
                    output_filename, "w", encoding="utf-8"
                ) as file:
                    if output_content is None:
                        output_content = "无" 

                    await file.write(output_content)
                    fakepath = "./code/" + code_id + ".txt"

                    if len(output_content) > 200:
                        return f"[Tool] Output is too long, Code running result is saving in this txt file, here is the url: {fakepath}, here is the first 100 characters of the output: {output_content[:200]}"
                    return f"[Tool] Output is: {output_content}, Code running result is saving in this txt file, here is the url: {fakepath}"

            except Exception as e:
                print(traceback.print_exc())

        @tool
        async def python(code: str) -> str:
            """Execute the code asynchronously."""

            os.makedirs(
                PYTHON_SAVE_DIR, exist_ok=True
            )  # Ensure the directory exists
            filename = os.path.join(PYTHON_SAVE_DIR, f"{code_id}.py").replace("\\", "/")
            print(f"Saving code to file: {filename}")
            async with aiofiles.open(filename, "w", encoding="utf-8") as file:
                await file.write(code)

            kernel = Jupyter()

            try:
                result = kernel.execute(code)

                output_content = ""
                if result["text"]:
                    output_content = result["text"]
                if result["error"]:
                    output_content = result["error"]

                output_filename = os.path.join(PYTHON_SAVE_DIR, f"{code_id}.txt").replace("\\", "/")
                async with aiofiles.open(
                    output_filename, "w", encoding="utf-8"
                ) as file:
                    await file.write(str(output_content))

                if result["images"]:
                    for idx, image in enumerate(result["images"]):
                        if isinstance(image, bytes):
                            image_bytes = image
                        else:
                            image_bytes = image.encode('utf-8')
                        
                        # 解码 base64 字符串为二进制数据
                        image_data = base64.b64decode(image_bytes)
                        
                        image_filename = os.path.join(IMAGE_SAVE_DIR, f"{code_id}_{idx}.jpg").replace("\\", "/")
                        # 使用二进制模式写入解码后的图片数据
                        async with aiofiles.open(image_filename, "wb") as img_file:
                            await img_file.write(image_data)

                print("toolreturning")
                if len(output_content) > 200:
                    return f"[Tool] Output is too long, here is the first 200 characters of the output: {output_content[:200]}"
                
                return f"[Tool] Output is: {output_content}"

            finally:
                # 确保正确关闭kernel
                print("Shutting down kernel...")
                kernel.shutdown()


        tools = [python]

        template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""

                    You are a Python code execution agent. You can send Python code to `python` tool , it will be executed in a stateful Jupyter kernel environment.

                    `python` tool will respond with the output of the code execution or timeout after 60.0 seconds.

                    Internet access for this agent is disabled, so do not make external API calls or web requests as they will fail.

                    System will show the image output to user automatically, you don't need to show the image output to user, i mean you don't output the sandbox image path to user, because it not work.

                    When you use matplotlib to draw a charts, do not use chinese to name your charts, otherwise the picture will be garbled.
                    
                    Use katex to render math formulas.
                    Use Chinese to answer the user, and use markdown format your answer.
                    禁止输出任何与图片URL.
            
                OS: {PythonLLM.operating_system}

                questions:
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
                if tool_data:
                    yield LLMStatus("python", code_id)
