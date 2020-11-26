import json
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ikea_backend import domain, model
from ikea_backend.database import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/available_products")
def available_products():
    products_available_quantities = domain.get_all_products_availabilities()
    return products_available_quantities


@app.put("/sell_product/{prod_id}")
def sell_product(prod_id: int):
    if domain.does_product_exist(prod_id):
        if domain.get_product_availability(prod_id) >= 1:
            product_component = domain.get_product_components(prod_id)
            domain.update_inventory(product_component)
            return {'message': "product was sold successfully"}
        return{'error': 'product out of stock'}
    return {'error': 'product does not exist'}


@app.post("/uploadfile/inventory")
def upload_inventory(file: UploadFile = File(...)):
    json_file = domain.from_byte_to_json(file.file)
    try:
        domain.write_inventory_to_database(json_file['inventory'])
    except Exception:
        return {"error": "an error happend, please contact your admin."}
    return {"message": f"{file.filename} was uploaded successfully"}



@app.post("/uploadfile/products")
def upload_products(file: UploadFile = File(...)):
    json_file = domain.from_byte_to_json(file.file)
    try:
        domain.write_products_to_database(json_file['products'])
    except Exception as e:

        return {"error": f"an error happend, please contact your admin. {e}"}
    return {"message": f"{file.filename} was uploaded successfully"}
