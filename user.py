from fastapi import APIRouter, HTTPException, Depends
from jwt import get_current_user
from service import read_user, write_user

user_router = APIRouter(tags=["User"])


@user_router.get("/user")
def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@user_router.post("/user")
def create_user(username: str, password: str, fullname: str, current_user=Depends(get_current_user)):
    db = read_user()
    for j in db:
        if current_user['username'] == j['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    for i in db:
        if i['username'] == username:
            raise HTTPException(status_code=401, detail="This user has exists")
    dict1 = {
        "username": username,
        "password": password,
        "full_name": fullname,
        "role": "regular",
        "is_active": True
    }
    db.append(dict1)
    result = write_user(db)
    if result==True:
        return {"Message":"This user is created and added system"}

@user_router.put("/user")
def change_user_fullname(username:str,new_fullname:str, current_user=Depends(get_current_user)):
    db = read_user()
    for j in db:
        if current_user['username'] == j['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    for i in db:
        if i['username']==username and i['is_active']==True:
            i['full_name']=new_fullname
            result = write_user(db)
            if result == True:
                return {"Message": "This user has changed and update to system"}
    raise HTTPException(status_code=404,detail="This username haven't in base")

@user_router.delete("/user")
def delete_user(username,current_user=Depends(get_current_user)):
    db = read_user()
    for j in db:
        if current_user['username'] == j['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    for i in db:
        if i['username']==username and i['is_active']==True:
            i['is_active']=False
            result = write_user(db)
            if result == True:
                return {"msg": "this user is deleted"}
    raise HTTPException(status_code=404,detail="This username haven't in base")

@user_router.get("/user/all")
def get_all_user(current_user=Depends(get_current_user)):
    db = read_user()
    for j in db:
        if current_user['username'] == j['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    all_user_lst=[]
    for i in db:
        if i['role']=="regular" and i['is_active']==True:
            dict1={i['username']:{"full_name":i['full_name'],"role":i['role']}}
            all_user_lst.append((dict1))
    return  {"All_users":all_user_lst}
