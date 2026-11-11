import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout

# ---------------------------------------------------------------------------
# annual_premium
# ---------------------------------------------------------------------------

def test_sedan_no_claims():
    # Base: sedan, age 30 (no age loading), 0 claims → 20% discount, no anti-theft
    # 12000 - 12000//5 = 12000 - 2400 = 9600
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_hatchback_young_driver_no_claims_anti_theft():
    # hatchback=8000, age<25 +4000=12000, 0 claims -2400=9600, anti_theft -500=9100
    assert annual_premium("hatchback", 20, 0, True) == 9100


def test_suv_senior_driver_many_claims():
    # suv=15000, age>=60 +2000=17000, claims>2 *2=34000, no anti-theft
    assert annual_premium("suv", 65, 3, False) == 34000


def test_sedan_middle_claims_no_anti_theft():
    # sedan=12000, age 40 (no age loading), 1<=claims<=2 (no change), no anti-theft
    assert annual_premium("sedan", 40, 1, False) == 12000


def test_sedan_anti_theft_with_claims():
    # sedan=12000, age 40, 2 claims (no multiplier, no discount), anti_theft -500
    assert annual_premium("sedan", 40, 2, True) == 11500


def test_young_driver_many_claims_anti_theft():
    # hatchback=8000, age<25 +4000=12000, claims>2 *2=24000, anti_theft -500=23500
    assert annual_premium("hatchback", 22, 4, True) == 23500


def test_senior_driver_no_claims_anti_theft():
    # suv=15000, age>=60 +2000=17000, 0 claims -3400=13600, anti_theft -500=13100
    assert annual_premium("suv", 70, 0, True) == 13100


def test_unknown_car_type_raises():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young_raises():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_exactly_age_18():
    # Boundary: age exactly 18 is allowed, also < 25 so +4000 loading
    # sedan=12000+4000=16000, 0 claims -3200=12800
    assert annual_premium("sedan", 18, 0, False) == 12800


def test_exactly_age_25():
    # age=25 is NOT < 25 and NOT >= 60 → no age loading
    # sedan=12000, 0 claims -2400=9600
    assert annual_premium("sedan", 25, 0, False) == 9600


def test_exactly_age_60():
    # age=60 → senior loading +2000
    # sedan=12000+2000=14000, 0 claims -2800=11200
    assert annual_premium("sedan", 60, 0, False) == 11200


def test_exactly_3_claims():
    # claims_last_3_years == 3 → premium * 2
    assert annual_premium("hatchback", 30, 3, False) == 16000


# ---------------------------------------------------------------------------
# no_claim_bonus
# ---------------------------------------------------------------------------

def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_bonus_one_year():
    assert no_claim_bonus(1) == 20


def test_bonus_two_years():
    assert no_claim_bonus(2) == 20


def test_bonus_three_years():
    assert no_claim_bonus(3) == 35


def test_bonus_four_years():
    assert no_claim_bonus(4) == 35


def test_bonus_five_years():
    assert no_claim_bonus(5) == 50


def test_bonus_many_years():
    assert no_claim_bonus(10) == 50


def test_negative_years_raises():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


# ---------------------------------------------------------------------------
# claim_payout
# ---------------------------------------------------------------------------

def test_total_loss_returns_insured_value():
    assert claim_payout(50000, 100000, 5000, True) == 100000


def test_damage_below_deductible():
    assert claim_payout(3000, 100000, 5000, False) == 0


def test_damage_equals_deductible():
    assert claim_payout(5000, 100000, 5000, False) == 0


def test_normal_payout():
    # damage 20000, deductible 5000, insured 100000 → payout 15000
    assert claim_payout(20000, 100000, 5000, False) == 15000


def test_payout_capped_at_insured_value():
    # damage 200000, deductible 5000, insured 100000 → capped at 100000
    assert claim_payout(200000, 100000, 5000, False) == 100000


def test_payout_exactly_insured_value():
    # damage 105000, deductible 5000, insured 100000 → payout = insured = 100000
    assert claim_payout(105000, 100000, 5000, False) == 100000


def test_negative_damage_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 100000, 5000, False)


def test_negative_deductible_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(10000, 100000, -500, False)


def test_zero_deductible():
    assert claim_payout(10000, 100000, 0, False) == 10000
