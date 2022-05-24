from fastapi import FastAPI
from . import schemas, services


app = FastAPI()


@app.post('/npv')
def npv(npv_schema: schemas.NPVSchema):
    return services.get_npv_list(npv_schema)


@app.post('npv_on_change')
def npv(npv_schema: schemas.NPVSchema):
    return services.npv_on_change()