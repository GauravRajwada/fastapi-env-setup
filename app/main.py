from typing import Union

from fastapi import FastAPI
import os
from . import message
from .domain import invoice

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    print(f"\n\n {os.environ['appname']} \n\n")
    return {"item_id": item_id, "q": q}


@app.post("/invoice/")
def create_invoice(msg: message.CreateInvoice):
    msg = msg.dict()
    print(f"\n\n msg: {msg}")
    result = invoice.create_invoice(**msg)
    return result

@app.get("/invoice/{id}")
def get_invoice_by_id(id: str):
    result = invoice.get_invoice_by_id(id)
    return result

@app.delete("/invoice/{id}")
def delete_invoice_by_id(id: str):
    return invoice.delete_invoice_by_id(id)

@app.put("invoice/{id}")
def update_invoice(msg: message.CreateInvoice):
    msg = msg.dict()
    return invoice.update_invoice_by_id(id=id, **msg)
