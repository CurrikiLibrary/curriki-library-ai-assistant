from langchain_core.tools import tool

class UserInfo:

    @tool
    def get_user_info(self):
        column_names = ["id", "name", "age"]
        rows = [(1, "Bob", 25)]
        return [dict(zip(column_names, row)) for row in rows]