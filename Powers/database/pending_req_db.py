from Powers.database import DB_BASE


class REQUESTED_USERS():
    """
    class to store join requested users in database
    """

    def __init__(self, channel: int) -> None:
        self.db = DB_BASE["pending_request"]
        self.channel = channel

    def insert_pending_user(self, user: int):
        self.db.insert_one({"c_id": self.channel, "user": user})

    def remove_pending_user(self, user: int):
        self.db.find_one_and_delete({"c_id": self.channel, "user": user})

    def get_pending_users(self, user=None):
        """
        if user id is not given it will return list of all pending requests in the channel
        """
        if not user:
            curr = self.db.find({"c_id": self.channel})
            user = [i["user"] for i in curr]

        else:
            curr = self.db.find_one({"c_id": self.channel, "user": user})
            if not curr:
                return False
            user = True

        return user
