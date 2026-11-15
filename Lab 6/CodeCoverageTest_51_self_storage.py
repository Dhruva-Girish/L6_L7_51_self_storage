
import pytest

from self_storage import rent_due, access_allowed, payment_status


# ---------------- RENT DUE TESTS ----------------

def test_invalid_unit_size():
    with pytest.raises(ValueError):
        rent_due("extra_large", 5, False, False)


def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_normal_rent():
    assert rent_due("small", 3, False, False) == 160


def test_member_discount():
    assert rent_due("small", 3, True, True) == 120


def test_large_member():
    assert rent_due("large", 4, False, True) == 80


def test_long_term_non_climate():
    assert rent_due("large", 10, False, False) == 490


def test_long_term_climate():
    assert rent_due("large", 10, True, False) == 735


# ---------------- ACCESS ALLOWED TESTS ----------------

def test_owner_allowed():
    assert access_allowed(23, 4, True) is True


def test_owner_exceeds_limit():
    assert access_allowed(12, 5, True) is False


def test_visitor_before_hours():
    assert access_allowed(5, 1, False) is False


def test_visitor_after_hours():
    assert access_allowed(23, 1, False) is False


def test_visitor_allowed():
    assert access_allowed(12, 2, False) is True


def test_visitor_exceeds_limit():
    assert access_allowed(12, 3, False) is False


# ---------------- PAYMENT STATUS TESTS ----------------

def test_autopay_current():
    assert payment_status(5, True, False) == "current"


def test_manual_payment_current():
    assert payment_status(5, False, False) == "current"


def test_payment_grace():
    assert payment_status(0, False, False) == "grace"


def test_payment_lien():
    assert payment_status(-11, False, False) == "lien"


def test_prior_late_current():
    assert payment_status(15, False, True) == "current"


def test_prior_late_grace():
    assert payment_status(0, False, True) == "grace"


def test_prior_late_lien():
    assert payment_status(-1, False, True) == "lien"
