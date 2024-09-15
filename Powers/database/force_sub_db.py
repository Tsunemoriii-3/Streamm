from Powers.database import DB_BASE


class FSUBS():
    """
    class to store fsub channels in database
    request, direct
    """

    def __init__(self) -> None:
        self.db = DB_BASE["fsub_channel"]

    def inser_fsub(self, channel_id, type_=None):
        """
        channeld_id: Int type id of the channel
        type: request, direct. request if you want request to join type fsub and direct if you want normal fsub.
        """
        curr = self.db.find_one({"c_id": channel_id})
        if curr:
            return curr["type"]
        else:
            if type_:
                self.db.insert_one({"c_id": channel_id, "type": type_})
                return False
            else:
                return True

    def update_fsub_type(self, channel_id, type_):
        self.db.find_one_and_update({"c_id": channel_id}, {"type": type_})

    def remove_fsub(self, channel_id):
        self.db.find_one_and_delete({"c_id": channel_id})

    def get_fsubs(self, type_="all"):
        """
        type: Type you want to fetch default to all.

        Types:
            direct: Fetch fsub channel which will directly accept the users.
            request: Fetch fsub channel with request to join attribute.
            all: Fetch bot type of channels

        all will return the list of dictionary of containing info of the channels insted of channel ids
        """
        if type_ == "request":
            all_ = self.db.find({"type": type})
            curr = [int(i["c_id"]) for i in all_]

        elif type_ == "direct":
            all_ = self.db.find({"type": type})
            curr = [int(i["c_id"]) for i in all_]

        else:
            curr = self.db.find({})

        return curr
