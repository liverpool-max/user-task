from fastapi import FastAPI
from authentication import login_router
from user import user_router
from tasks import task_router


app = FastAPI(title="Orxan's program",description="This program has created by Orxan Tehmezli and program for user of task",version="1.9.2")


@app.get("/")
def health_check():
    return {"Message":"Hi,Welcome to Orxan's program"}


app.include_router(login_router)

app.include_router(user_router)

app.include_router(task_router)
