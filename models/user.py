
class User:
    """
    User模型
    """

    uuid: str
    username: str
    email: str
    hashed_password: str
    group: str

    def __init__(
        self, uuid: str, username: str, email: str, hashed_password: str, group: str
    ) -> None:
        self.uuid = uuid
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.group = group

    def is_admin(self):
        return self.group == "admin"
