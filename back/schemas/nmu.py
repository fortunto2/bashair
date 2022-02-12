from typing import Optional

from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, validator, AnyUrl


class NmuBase(BaseModel):
    mode: int
    datetime: datetime
    time: time
    date: date
