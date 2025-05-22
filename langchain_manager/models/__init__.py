
import importlib
import os

from models.llm import LLMModel

__all__ = ['llms']
llms: list[LLMModel] = []

def init_llms() -> list[LLMModel]:
    """
    初始化LLM模型
    """
    models_dir = os.path.join(os.path.dirname(__file__))
    
    for filename in os.listdir(models_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"langchain_manager.models.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'init'):
                print(f'[Server]  - {module_name}')
                init_method = getattr(module, 'init')
                llm_object = init_method()
                if llm_object is not None and isinstance(llm_object, LLMModel):
                    llms.append(llm_object)

    return llms
    
if not llms:
    init_llms()




