import msgpack
import unqlite
from threading import Lock

db = unqlite.UnQLite('DBs/master.db')
db_lock = Lock()


#   store a decoded JSON dictionary  in the database to be accessed by the key which is UNIX datetime (which is specified in the record)
def StoreJSON( decoded_json ):
    record_bin = msgpack.packb( decoded_json )
    
    with db_lock:
        db[ decoded_json["date"] ] = record_bin
        db.commit()


