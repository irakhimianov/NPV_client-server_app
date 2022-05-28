from schemas import NPVSchema
from datetime import datetime


def npv_counter(year: int, discount_rate: float, income: float, expense: float, prev_NPV: float=0) -> float:
    net_cash_flow = income - expense
    return net_cash_flow / ((1 + discount_rate) ** year) + prev_NPV


def get_npv_list(npv: NPVSchema) -> list:
    res = []
    years_amount = npv.year - datetime.now().year + 1
    for i in range(1, years_amount + 1):
        prev_NPV = 0 if i == 1 else res[i - 2]['npv']
        # npv_counter(**npv)
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


def npv_to_change(npv_list: list, col_changed: int, income: int, expense: int):
    res = npv_list[:col_changed]
    prev_NPV = 0 if col_changed == 0 else res[col_changed - 1]['npv']
    new_npv_amount = npv_counter(year=col_changed + 1,
                                 discount_rate=npv_list[col_changed]['discount_rate'],
                                 income=income,
                                 expense=expense,
                                 prev_NPV=prev_NPV)

    res.append({'year': col_changed + 1,
                'discount_rate': npv_list[col_changed]['discount_rate'],
                'income': income,
                'expense': expense,
                'npv': new_npv_amount})

    for i in range(col_changed + 1, len(npv_list)):
        prev_year_npv_amount = new_npv_amount if i == col_changed else res[i - 1]['npv']
        npv_amount = npv_counter(year=i + 1,
                                 discount_rate=npv_list[i]['discount_rate'],
                                 income=npv_list[i]['income'],
                                 expense=npv_list[i]['expense'],
                                 prev_NPV=prev_year_npv_amount)
        res.append({'year': i + 1,
                    'discount_rate': npv_list[i]['discount_rate'],
                    'income': npv_list[i]['income'],
                    'expense': npv_list[i]['expense'],
                    'npv': npv_amount})

    return res



npv = NPVSchema(year=2025,
                discount_rate=0.2,
                income=1000,
                expense=500,
                prev_NPV=0)

npv_list = get_npv_list(npv)
print(npv_list)
x = npv_to_change(npv_list, 0, 1000, 300)
print(npv_to_change(x, 2, 1000, 300))




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