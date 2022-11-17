from datetime import datetime
from enum import Enum

from pydantic import Field
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
    nb_of_successful_attempts: int = 0
    nb_of_failed_attempts: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    @property
    def total_attempts(self):
        return self.nb_of_successful_attempts + self.nb_of_failed_attempts

    @property
    def date(self):
        return self.created_at.strftime("created on %m/%d/%Y, at %H:%M:%S %Z")
