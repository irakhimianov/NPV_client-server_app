def npv_counter(year: int, discount_rate: float, income: float, expense: float, prev_NPV: float = 0) -> float:
    net_cash_flow = income - expense
    return net_cash_flow / ((1 + discount_rate) ** year) + prev_NPV
