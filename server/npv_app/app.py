from fastapi import FastAPI
from . import schemas, services

app = FastAPI()


@app.get('/')
def root():
    return {"message": "hello"}


@app.post('/npv')
def npv(npv_schema: schemas.NPVSchema):
    return services.npv_counter(npv_schema)