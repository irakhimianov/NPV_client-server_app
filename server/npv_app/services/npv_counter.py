from datetime import datetime
from npv_app.schemas import NPVSchema


def npv_counter(year: int, discount_rate: float, income: float, expense: float, prev_NPV: float=0) -> float:
    net_cash_flow = income - expense
    return net_cash_flow / ((1 + discount_rate) ** year) + prev_NPV


def get_npv_list(npv: NPVSchema) -> list[float]:
    res = []
    years_amount = npv.year - datetime.now().year + 1
    for i in range(1, years_amount + 1):
        prev_NPV = 0 if i == 1 else res[i - 2]
        # print(f"{prev_NPV=}\n{res=}")
        res.append(npv_counter(year=i,
                               discount_rate=npv.discount_rate,
                               income=npv.income,
                               expense=npv.expense,
                               prev_NPV=prev_NPV))
    return res
