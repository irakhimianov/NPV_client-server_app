from ..schemas import NPVSchema
from datetime import datetime


def npv_counter(year: int, discount_rate: float, income: float, expense: float, prev_NPV: float=0) -> float:
    net_cash_flow = income - expense
    return net_cash_flow / ((1 + discount_rate) ** year) + prev_NPV


def get_npv_list(npv: NPVSchema) -> list:
    res = []
    years_amount = npv.year - datetime.now().year + 1
    for i in range(1, years_amount + 1):
        prev_NPV = 0 if i == 1 else res[i - 2]['npv']
        npv_amount = npv_counter(year=i,
                                 discount_rate=npv.discount_rate,
                                 income=npv.income,
                                 expense=npv.expense,
                                 prev_NPV=prev_NPV)
        res.append({'year': i,
                    'discount_rate': npv.discount_rate,
                    'income': npv.income,
                    'expense': npv.expense,
                    'npv': npv_amount})

    return res


def npv_on_change(prev_info: list, year: int, income: float, expense: float, prev_NPV: float):
    pass


# npv = NPVSchema(year=2024,
#                 discount_rate=0.2,
#                 income=1000,
#                 expense=500,
#                 prev_NPV=0)

# x = get_npv_list(npv)
# print(x)
# n = 1
# x[n]['expense'] = 400
# for i in range(n, len(x)):
#     x[i]['npv'] = npv_counter(year=x[i]['year'],
#                               discount_rate=x[i]['discount_rate'],
#                               income=x[i]['income'],
#                               expense=x[i]['expense'],
#                               prev_NPV=x[i - 1]['npv'])

# for i in x:
#     for j in i:
#         print(i[j])
#     print('---')