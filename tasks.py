from fastapi import APIRouter,HTTPException,Depends
from jwt import get_current_user
from service import read_user,read_task,write_task


task_router=APIRouter(tags=["Task"])


@task_router.get("/current_task")
def get_current_task(current_user=Depends(get_current_user)):
    db_user=read_user()
    for j in db_user:
        if j['username']==current_user['username']:
            if j['role']=="admin":
                raise HTTPException(status_code=401,detail="This function only for regular users")
    db=read_task()
    for i in db:
        if i['username']==current_user['username'] and i['status']=="in_progress":
            return {"Task_details":{"name":i['name'],"description":i['description'],"status":i['status']}}
    raise HTTPException(status_code=404,detail="For this username not assigned task ")



@task_router.get("/task_by_id")
def get_task_by_id(id:int,current_user=Depends(get_current_user)):
    db_user = read_user()
    for j in db_user:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db=read_task()
    for i in db:
        if i['task_id']==id:
            return  {"Task_details":{"name":i['name'],"description":i['description'],"status":i['status']}}
    raise HTTPException(status_code=404,detail="This task is not found")



@task_router.post("/task")
def create_task(username:str,task_name:str,task_detail,current_user=Depends(get_current_user)):
    db_user = read_user()
    for j in db_user:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db=read_task()
    for i in db:
        if i['username']==username and i['status']=="in_progress" and i['is_deleted']==False:
            raise HTTPException(status_code=401,detail="For one username have to be one task! ")
    n=len(db)
    dict1={
    "task_id": n+1,
    "username": username,
    "name": task_name,
    "description": task_detail,
    "status": "in_progress",
    "is_deleted": False
  }
    db.append(dict1)
    a=write_task(db)
    if a==True:
        return {"Message":"This task is created and added system"}
    


@task_router.put("/task_detail")
def change_task_detail(task_id:int,new_task_detail,current_user=Depends(get_current_user)):
    db_user = read_user()
    for j in db_user:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db=read_task()
    for i in db:
        if i['task_id']==task_id:
            i['description']=new_task_detail
            a = write_task(db)
            if a == True:
                return {"Message": "Detail of this task is changed"}
    raise HTTPException(status_code=404,detail="This task is not found")


@task_router.put("/task")
def change_task_status(current_user=Depends(get_current_user)):
    db=read_task()
    for i in db:
        if i['username']==current_user and  i['status']=="in_progress":
            i['status']="completed"
            a = write_task(db)
            if a == True:
                return {"Message": "Status of this task is changed successfully"} 
    for i in db:
        if i['username']==current_user and  i['status']=="completed":
            raise HTTPException(status_code=402,detail="This task has already been completed")
    raise HTTPException(status_code=402,detail="For this username not assigned task")


            
@task_router.delete("/task")
def delete_task(id:int,current_user=Depends(get_current_user)):
    db_user = read_user()
    for j in db_user:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db = read_task()
    for i in db:
        if i['task_id'] == id and i['is_deleted'] == False:
            i['is_deleted'] = True
            a = write_task(db)
            if a == True:
                return {"Message": "This task is deleted"}
    raise HTTPException(status_code=404,detail="This task is not found")



@task_router.get("/task/user_stats")
def get_all_tasks_by_user(username:str,current_user=Depends(get_current_user)):
    db_user = read_user()
    for j in db_user:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db = read_task()
    ls=[]
    for  i in db:
        if i['username']==username and i['is_deleted'] != True:
            my_dict={"task_name":i['name'],"description":i['description'],"status":i['status']}
            ls.append(my_dict)
    if len(ls)==0:
        raise HTTPException(status_code=404,detail="For this username haven't task")
    else:
        return {"tasks":ls}
    


@task_router.get("/task/general_stats")
def complete_tasks_for_current_user(current_user=Depends(get_current_user)):
    dbuser = read_user()
    for j in dbuser:
        if j['username'] == current_user['username']:
            if j['role'] == "regular":
                raise HTTPException(status_code=401, detail="This function only for admin")
    db = read_task()
    lst=[]
    for i in db:
        if i["status"]=="completed" and i['is_deleted']==False:
            dict1={i['username']:{"task_name":i['name'],"description":i['description'],"status":i['status']}}
            lst.append(dict1)
    if len(lst)==0:
        raise HTTPException(status_code=404,detail="This username haven't complete task")
    else:
        return {"complete_tasks":lst}
    

    
@task_router.get("/task/all")
def get_all_task_for_current_user(current_user=Depends(get_current_user)):
    db = read_task()
    lst=[]
    for i in db:
        if i['username']==current_user['username'] and i['is_deleted']==False:
            dict1={"task_name":i['name'],"description":i['description'],"status":i['status']}
            lst.append(dict1)
    if len(lst)==0:
        raise HTTPException(status_code=404,detail="For this username havent task")
    else:
        return {"all_tasks":lst}