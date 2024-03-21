from typing import Union

from fastapi import FastAPI
import os
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(f"\n\n {os.environ['appname']} \n\n")
    return {"item_id": item_id, "q": q}

