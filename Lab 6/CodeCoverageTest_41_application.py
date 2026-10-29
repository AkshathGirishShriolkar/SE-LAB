import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status,
)


def test_extra_weight_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_extra_weight_regular_standard():
    assert extra_weight_charge("regular", 8, "standard", False) == 90


def test_extra_weight_express():
    assert extra_weight_charge("regular", 8, "express", False) == 150


def test_extra_weight_member():
    assert extra_weight_charge("regular", 8, "standard", True) == 30


def test_extra_weight_bedding():
    assert extra_weight_charge("bedding", 10, "standard", False) == 60


def test_extra_weight_delicate():
    assert extra_weight_charge("delicate", 8, "standard", False) == 150


def test_extra_weight_no_extra():
    assert extra_weight_charge("regular", 5, "standard", False) == 0


def test_extra_weight_invalid_garment():
    with pytest.raises(ValueError):
        extra_weight_charge("unknown", 8, "standard", False)


def test_extra_weight_negative_weight():
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)


def test_order_acceptable_delicate():
    assert order_acceptable(10, 5, True) is True


def test_order_acceptable_weight_limit():
    assert order_acceptable(25, 40, False) is True


def test_dropoff_accepted():
    assert dropoff_status(90, False, False) == "accepted"


def test_dropoff_late():
    assert dropoff_status(45, False, False) == "late"


def test_dropoff_rejected():
    assert dropoff_status(39, False, False) == "rejected"


def test_dropoff_bedding_cutoff():
    assert dropoff_status(90, True, False) == "accepted"
    assert dropoff_status(75, True, False) == "late"


def test_dropoff_express_cutoff():
    assert dropoff_status(60, False, True) == "rejected"
    assert dropoff_status(90, False, True) == "accepted"


def test_dropoff_bedding_express_combination():
    assert dropoff_status(120, True, True) == "accepted"
    assert dropoff_status(89, True, True) == "rejected"


def test_dropoff_express_boundary():
    assert dropoff_status(69, False, True) == "rejected"
    assert dropoff_status(70, False, True) == "late"


def test_extra_weight_above_ten():
    assert extra_weight_charge("regular", 13, "standard", False) == 240


def test_extra_weight_exactly_ten():
    assert extra_weight_charge("regular", 15, "standard", False) == 300


def test_extra_weight_express_rate():
    assert extra_weight_charge("regular", 13, "express", False) == 400

def test_extra_weight_standard_above_ten():
    # Extra weight = 13 - 5 = 8; standard rate = 30
    assert extra_weight_charge("regular", 13, "standard", False) == 240


def test_order_acceptable_overweight():
    assert order_acceptable(26, 10, False) is False


def test_order_acceptable_item_limit():
    assert order_acceptable(20, 41, False) is False
