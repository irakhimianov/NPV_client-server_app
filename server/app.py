from fastapi import FastAPI
from . import services
from models import NPVSchema


app = FastAPI()


@app.post('/npv')
def npv(npv: NPVSchema):
    return services.get_npv_list(npv)


@app.post('/npv_on_change')
def npv_on_change(npv_list: list, col_changed: int, income: float, expense: float):
    return services.npv_list_on_change(npv_list=npv_list,
                                       col_changed=col_changed,
                                       income=income,
                                       expense=expense)
    return 'hi'
