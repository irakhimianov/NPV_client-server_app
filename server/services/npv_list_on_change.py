from .npv_list import get_npv_list
from .npv_counter import npv_counter


def npv_list_on_change(npv_list: list, col_changed: int, income: float, expense: float) -> list:
    res = npv_list[:col_changed]
    prev_NPV = 0 if col_changed == 0 else float(res[col_changed - 1]['npv'])
    new_npv_amount = round(npv_counter(year=col_changed + 1,
                                       discount_rate=float(npv_list[col_changed]['discount_rate']),
                                       income=income,
                                       expense=expense,
                                       prev_NPV=prev_NPV), 3)

    res.append({'year': col_changed + 1,
                'discount_rate': float(npv_list[col_changed]['discount_rate']),
                'income': income,
                'expense': expense,
                'npv': new_npv_amount})

    for i in range(col_changed + 1, len(npv_list)):
        prev_year_npv_amount = new_npv_amount if i == col_changed else float(res[i - 1]['npv'])
        npv_amount = npv_counter(year=i + 1,
                                 discount_rate=float(npv_list[i]['discount_rate']),
                                 income=float(npv_list[i]['income']),
                                 expense=float(npv_list[i]['expense']),
                                 prev_NPV=float(prev_year_npv_amount))
        res.append({'year': i + 1,
                    'discount_rate': npv_list[i]['discount_rate'],
                    'income': npv_list[i]['income'],
                    'expense': npv_list[i]['expense'],
                    'npv': round(npv_amount, 3)})
    return res
