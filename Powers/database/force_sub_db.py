from Powers.database import DB_BASE


class FSUBS():
    """
    class to store fsub channels in database
    request, direct
    """

    def __init__(self) -> None:
        self.db = DB_BASE["fsub_channel"]

    def inser_fsub(self, channel_id, type_=None, btn_name = None):
        """
        channeld_id: Int type id of the channel
        type: request, direct. request if you want request to join type fsub and direct if you want normal fsub.
        btn_name: Name of the button you want to set
        """
        curr = self.db.find_one({"c_id": channel_id})
        if curr:
            return curr
        else:
            if type_:
                self.db.insert_one({"c_id": channel_id, "type": type_, "btn_name": btn_name})
                return False
            else:
                return True

    def update_fsub_type(self, channel_id, type_):
        return self.db.find_one_and_update({"c_id": channel_id}, {"type": type_})

    def update_fsub_btn(self, channel_id, name):
        return self.db.find_one_and_replace({"c_id": channel_id}, {"$set": {"btn_name": name}})

    def remove_fsub(self, channel_id):
        return self.db.find_one_and_delete({"c_id": channel_id})

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
            all_ = self.db.find({"type": type_})
            curr = list(all_)

        elif type_ == "direct":
            all_ = self.db.find({"type": type_})
            curr = list(all_)

        else:
            curr = list(self.db.find({}))

        return curr


class FSUB_LINK():
    """
    class to store link based fsub channels or anything
    """

    def __init__(self) -> None:
        self.db = DB_BASE["linksub"]

    def insert_link(self, link: str, btn_name = None):
        curr = self.db.find_one({"link": link})
        if not curr:
            self.db.insert_one({"link": link, "btn_name": btn_name})
            return True
        return

    def delete_link(self, link):
        return self.db.find_one_and_delete({"link": link})

    def get_all(self):
        return list(self.db.find({}))

    def update_btn(self, link, name):
        return self.db.find_one_and_update({"link": link}, {"btn_name": name})