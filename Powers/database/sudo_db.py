from Powers.database import DB_BASE


class SUPPORTS():
    """
    class to store support users in database
    sudo
    """

    def __init__(self) -> None:
        self.db = DB_BASE["SUDO"]

    def insert_support_user(self, user_id):
        if not self.is_support_user(user_id):
            self.db.insert_one({"_id": user_id})
        return

    def is_support_user(self, user_id):
        curr = self.db.find_one({"_id": user_id})
        if curr:
            return True
        return False

    def delete_support_user(self, user):
        self.db.find_one_and_delete({"_id": user})

    def get_support(self):
        curr = self.db.find({})
        if curr:
            return [int(i["_id"]) for i in curr]
        else:
            return []
