import jwt

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
from fastapi import File, UploadFile, Path
import boto3
from botocore.exceptions import NoCredentialsError
import os


from app.models.User import UserOut, UserUpdate
from app.UserService import UserService

app = FastAPI()
us = UserService()

@app.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    return await us.get_user_by_id(user_id)

@app.get("/", response_model=UserOut)
async def search_user(username: str):
    return await us.get_user_by_username(username)

@app.patch("/", response_model=UserUpdate)
async def update_user(request: Request, updated_user: UserUpdate):
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload["sub"]
    return await us.update_user_by_id(user_id, updated_user)

@app.delete("/")
async def delete_user(request: Request):
    bearer = request.headers.get("Authorization")
    token = bearer.split(" ")[1]
    payload = jwt.decode(token, options={"verify_signature": False})
    user_id = payload["sub"]
    return await us.delete_user_by_id(user_id)

@app.get("/users/{user_id}/following", response_model=None)
async def get_following_users():
    raise NotImplementedError

@app.post("/users/{user_id}/image", response_model=None)
async def upload_user_image(user_id: str = Path(...), file: UploadFile = File(...)):

    bucket_name = "ms-user" #must be also defined in localstack-setup under support  
    s3_folder = "user-images/"  # This acts as a "folder" in S3
    
    # get data from env (doesn't matter if localstack or true aws )
    s3_client = boto3.client(
        's3',
        endpoint_url= os.getenv("S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )

    try:
        # Read file content
        file_content = await file.read()

        # The object key simulates a path structure
        object_key = f"{s3_folder}{user_id}/{file.filename}"

        # Upload file to S3 (LocalStack in this case)
        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)

        return {"message": "File uploaded successfully", "file_name": object_key}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})



