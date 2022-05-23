from fastapi import FastAPI, Request
from . import schemas, services


app = FastAPI()


@app.post('/npv')
def npv(npv_schema: schemas.NPVSchema):
    return services.get_npv_list(npv_schema)

# @app.post('/npv')
# def root(data: str):
#     print(data)
#     return 'hi'
#
# # @app.post('/npv')
# # def get_npv(request: Request):
# #     req_info = request.json()
# #     return {'status': 'ok',
# #             'data': req_info}