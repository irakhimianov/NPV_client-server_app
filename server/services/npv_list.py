from datetime import datetime
from models import NPVSchema
from .npv_counter import npv_counter


def get_npv_list(npv: NPVSchema) -> list:
    res = []
    years_amount = npv.year - datetime.now().year + 1
    for i in range(years_amount + 1):
        prev_NPV = 0 if i == 0 else res[i - 1]['npv']
        npv_amount = npv_counter(year=i + 1,
                                 discount_rate=npv.discount_rate,
                                 income=npv.income,
                                 expense=npv.expense,
                                 prev_NPV=prev_NPV)
        res.append({'year': i + 1,
                    'discount_rate': npv.discount_rate,
                    'income': npv.income,
                    'expense': npv.expense,
                    'npv': npv_amount})
    return res
