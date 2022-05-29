from pydantic import BaseModel


class NPVSchema(BaseModel):
    # Год
    year: int = 0
    # Ставка дисконтирования
    discount_rate: float = 0.0
    # Доход
    income: float = 0.0
    # Расход
    expense: float = 0.0
    # Чистый денежный поток
    # Предыдущий показатель NPV
    prev_NPV: float = 0.0
