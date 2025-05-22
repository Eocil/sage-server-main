from enums.message_enum import ServicesStatusEnum


class ManagersStatusEnum(ServicesStatusEnum):

    INVOKE_LLM_FAILED = (10001, "Invoke LLM failed")
    INVOKE_SORT_FAILED = (10002, "Invoke Sort failed")
    INVOKE_CHAT_FAILED = (10003, "Invoke Chat failed")
    INVOKE_PYTHON_FAILED = (10004, "Invoke Python failed")
    INVOKE_IMAGE_FAILED = (10005, "Invoke Image failed")
    INVOKE_INTERNET_FAILED = (10006, "Invoke Internet failed")
    INVOKE_RETRIEVAL_FAILED = (10007, "Invoke Retrieval failed")
    INVOKE_TITLE_FAILED = (10008, "Invoke Title failed")