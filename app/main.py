from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
import uvicorn
from hello import hello
import json
from pydantic import BaseModel
from settings import settings_as_dict
from tasks import add

app = FastAPI()

class Job(BaseModel):
   file_name: str
   id: int

   def get(self):
        return f'message {self.file_name}'


@app.get('/')
def hello_world():
    r = add.delay(1, 1)
    return {'greet': hello(), 'url': settings_as_dict['redis_host'], 'r': str(r)}


@app.post("/files/")
async def image(params:  UploadFile = File(...), image: UploadFile = File(...)):
    data = await params.read()
    params = json.loads(data)
    return {"filename": image.filename, 'info': params['message']}


@app.post("/job/")
async def params(params: Job):

    return {'file_name': params.file_name, 'id': params.id}


@app.post("/uploadfile/")
async def upload(image: UploadFile = File(...), id: int = Form(...)):
    return {"filename": image.filename, 'id': id}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
