from fastapi import FastAPI

# FastAPI app
app = FastAPI()

# User Crud - EDIT, DELETE, GET (no create we create only via register, all other values like images are via update only)

@app.get("/helloworld")
def read_root():
    return {"Hello": "World"}