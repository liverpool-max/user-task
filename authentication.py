from fastapi import APIRouter,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from jwt import authenticate_user,create_access_token
from service import read_user

login_router = APIRouter(tags=["Authorization"])


@login_router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db=read_user()
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}