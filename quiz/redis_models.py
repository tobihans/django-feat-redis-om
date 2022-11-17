import datetime
from enum import Enum

from redis_om import HashModel


class CorrectOption(Enum):
    OP1 = "op1"
    OP2 = "op2"
    ALL = "all"
    NONE = "none"


class SimpleQuiz(HashModel):
    title: str
    option1: str
    option2: str
    correct_option: CorrectOption
