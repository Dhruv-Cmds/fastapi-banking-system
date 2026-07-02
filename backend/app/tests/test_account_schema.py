from pydantic import ValidationError

from app.schemas.account import MoneyRequest


def test_money_request_rejects_negative_amount():
    try:
        MoneyRequest(amount=-1)
    except ValidationError:
        pass
    else:
        raise AssertionError("negative amounts must be rejected")


def test_money_request_rejects_zero_amount():
    try:
        MoneyRequest(amount=0)
    except ValidationError:
        pass
    else:
        raise AssertionError("zero amounts must be rejected")

