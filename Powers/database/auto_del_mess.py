from Powers.database import DB_BASE

mycol = DB_BASE['AUTODEL']

def auto_del_insert(date, chat_id:int, message_id:int):
    query = mycol.find_one({"chat_id":chat_id,"mess_id":message_id,"datee":date})
    if not query:
        mycol.insert_one({"chat_id":chat_id,"mess_id":message_id,"datee":date})
        
    return

def auto_del_get():
    query = list(mycol.find({}))
    return query

def auto_del_delete(chat_id:int, message_id:int):
    query = mycol.find_one({"chat_id":chat_id,"mess_id":message_id})
    if query:
        mycol.delete_one({"chat_id":chat_id,"mess_id":message_id})
    return
