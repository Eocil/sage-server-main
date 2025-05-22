from enums.message_enum import ServicesStatusEnum


class ServicesStatusEnum(ServicesStatusEnum):

    

    INVALID_PASSWORD = (1001, "账号或密码错误")
    USER_NOT_FOUND = (1002, "用户不存在")
    EMAIL_EXIST = (1003, "邮箱已存在")
    INVALID_INVITE_CODE = (1004, "无效的邀请码")

    INVALID_ACCESS_TOKEN = (2001, "无效的访问令牌")

    INVALID_TOPIC_ID = (3001, "无效的话题ID")
    TOPIC_NOT_FOUND = (3002, "话题不存在")
    HISTORY_NOT_FOUND = (3003, "该话题的历史记录不存在")

    GET_CHAT_MODEL_FAILED = (4001, "获取Chat模型失败")
    GET_SEARCH_MODEL_FAILED = (4002, "获取Internet模型失败")
    GET_IMAGE_MODEL_FAILED = (4003, "获取Image模型失败")
    GET_EMBEDDING_MODEL_FAILED = (4004, "获取Embedding模型失败")
    MODEL_PERMISSION_DENIED = (4005, "没有该模型的权限")

    FILE_NOT_FOUND = (5001, "文件不存在")
    CODE_NOT_FOUND = (5002, "代码不存在")
    IMAGE_NOT_FOUND = (5003, "图片不存在")
    FILE_UPLOAD_FAILED = (5004, "文件上传失败")

    PERMISSION_DENIED = (9001, "没有权限")