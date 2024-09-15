from Powers.database import DB_BASE


class PEERS():

    def __init__(self) -> None:
        self.db = DB_BASE["PEERS"]

    def insert_peer(self, peer_type, peer_id):
        curr = self.db.find_one({"peer": peer_id})
        if curr:
            return
        self.db.insert_one({"peer": peer_id, "type": peer_type.lower()})
        return True

    def remove_peer(self, peer_id):
        self.db.find_one_and_delete({"peer": peer_id})

    def get_peers(self, peer_type: str = "all"):
        """
        peer_type: `all`, `chat`, `user`
        """
        peer_type = peer_type.lower()
        if peer_type == "all":
            peer = self.db.find({})
        elif peer_type == "chat":
            peer = self.db.find({"type": peer_type})
        elif peer_type == "user":
            peer = self.db.find({"type": peer_type})
        else:
            return []

        return list(peer)

    def count_peers(self):
        """
        return a tuple of total numbers of users and chats in order users first followed by chats in tuple
        """
        users = self.db.count_documents({"type": "user"})
        chats = self.db.count_documents({"type": "chat"})

        return (users, chats)
