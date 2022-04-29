from fastapi import FastAPI
from . import schemas, services

app = FastAPI()


@app.post('/')
def root(npv_schema: schemas.NPVSchema):
    return services.npv_counter(npv_schema)
