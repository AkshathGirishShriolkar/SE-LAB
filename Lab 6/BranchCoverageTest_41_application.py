import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status,
)


def test_extra_weight_branches():
    assert extra_weight_charge("regular", 4, "standard", False) == 0
    assert extra_weight_charge("regular", 8, "standard", False) == 90
    assert extra_weight_charge("regular", 8, "express", False) == 150
    assert extra_weight_charge("regular", 13, "standard", False) == 240
    assert extra_weight_charge("regular", 13, "express", False) == 400


def test_extra_weight_errors():
    with pytest.raises(ValueError):
        extra_weight_charge("unknown", 8, "standard", False)

    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)


def test_extra_weight_membership():
    assert extra_weight_charge("regular", 8, "standard", True) == 30
    assert extra_weight_charge("bedding", 10, "standard", True) == 60


def test_order_acceptable_branches():
    assert order_acceptable(10, 5, True) is True
    assert order_acceptable(10, 6, True) is False
    assert order_acceptable(26, 10, False) is False
    assert order_acceptable(20, 40, False) is True
    assert order_acceptable(20, 41, False) is False


def test_dropoff_status_branches():
    assert dropoff_status(90, False, False) == "accepted"
    assert dropoff_status(50, False, False) == "late"
    assert dropoff_status(39, False, False) == "rejected"

    assert dropoff_status(120, True, False) == "accepted"
    assert dropoff_status(75, True, False) == "late"
    assert dropoff_status(69, False, True) == "rejected"
    assert dropoff_status(70, False, True) == "late"
    assert dropoff_status(120, True, True) == "accepted"

