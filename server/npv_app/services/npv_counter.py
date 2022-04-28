from npv_app.schemas import NPVSchema


def npv_counter(npv: NPVSchema) -> float:
    year = npv.year
    discount_rate = npv.discount_rate
    income = npv.income
    expense = npv.expense
    net_cash_flow = npv.net_cash_flow
    prev_NPV = npv.prev_NPV

    return net_cash_flow / ((1 + discount_rate) ** year) + prev_NPV