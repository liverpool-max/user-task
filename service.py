import json

def read_user():
    with open("users.json","r") as f:
        db=json.load(f)
    return db

def write_user(db):
    with open("users.json","w") as f:
        json.dump(db,f,indent=4)
    return  True

def read_task():
    with open("tasks.json","r") as f:
        db=json.load(f)
    return db

def write_task(db):
    with open("tasks.json","w") as f:
        json.dump(db, f, indent=4)
    return True