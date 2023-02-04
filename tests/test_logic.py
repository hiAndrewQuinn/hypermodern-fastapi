"""Test cases for the __main__ module."""
from wolt_summer_eng_assignment import logic


###############################################################

# Happy path tests.
# Where everything is normal.

test_payload = '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'

delivery_info = logic.DeliveryInfo.parse_raw(test_payload)


def test_pydantic_delivery_info():
    """Test that the pydantic model works."""
    assert delivery_info.cart_value == 790
    assert delivery_info.delivery_distance == 2235
    assert delivery_info.number_of_items == 4
    assert delivery_info.time == "2021-10-12T13:00:00Z" ""


def test_delivery_fee():
    """Test that the delivery fee is calculated correctly."""
    assert delivery_info.calculate_delivery_fee() == 710


def test_small_order_surcharge():
    """Test that the small order surcharge is calculated correctly."""
    assert delivery_info.calculate_small_order_surcharge() == 210


def test_distance_surcharge():
    """Test that the distance surcharge is calculated correctly."""
    assert delivery_info.calculate_distance_surcharge() == 500


def test_friday_rush_surcharge():
    """Test that the Friday rush surcharge is calculated correctly.

    (According to Google, October 12, 2021 was a Tuesday.)
    """
    assert delivery_info.calculate_friday_rush_surcharge() == 1.0


###############################################################

# Value variations. Here we generate some random values and
# verify we get the right delivery fees by hand.

# Random payload: Big cart, Friday at 5 pm, 10 km away.
# Big carts get free delivery!


def test_random_payload_charges():
    """Logic test that the delivery fee is calculated correctly.

    This is for a random payload that should be free,
    but would otherwise be quite expensive.
    """
    # Quite a large payload, but it's free!
    payload = logic.DeliveryInfo.parse_raw(
        '{"cart_value": 100000, "delivery_distance": 10000, "number_of_items": 100, "time": "2021-10-15T17:00:00Z"}'
    )

    assert payload.calculate_small_order_surcharge() == 0
    assert payload.calculate_distance_surcharge() == (10 * 200)
    assert payload.calculate_item_number_surcharge() == ((100 - 4) * 50) + 120
    assert payload.calculate_friday_rush_surcharge() == 1.2
    assert payload.calculate_delivery_fee() == 0


def test_random_payload2_charges():
    """Logic test that the delivery fee is calculated correctly.

    This is for a random payload that is just under the
    free delivery threshold, and hits the max delivery fee
    as a result.
    """
    payload2 = logic.DeliveryInfo.parse_raw(
        '{"cart_value": 999, "delivery_distance": 10000, "number_of_items": 100, "time": "2021-10-15T17:00:00Z"}'
    )

    assert payload2.calculate_small_order_surcharge() == 1
    assert payload2.calculate_distance_surcharge() == (10 * 200)
    assert payload2.calculate_item_number_surcharge() == ((100 - 4) * 50) + 120
    assert payload2.calculate_friday_rush_surcharge() == 1.2
    assert payload2.calculate_delivery_fee() == 1500


def test_random_payload3_charges():
    """Logic test that the delivery fee is calculated correctly.

    This is for a random payload with no special cases.
    """
    payload3 = logic.DeliveryInfo.parse_raw(
        '{"cart_value": 3124, "delivery_distance": 1718, "number_of_items": 6, "time": "2022-04-15T23:03:00Z"}'
    )

    assert payload3.calculate_small_order_surcharge() == 0
    assert payload3.calculate_distance_surcharge() == 400
    assert payload3.calculate_item_number_surcharge() == 100
    assert payload3.calculate_friday_rush_surcharge() == 1.0
    assert payload3.calculate_delivery_fee() == 500


def test_random_payload4_charges():
    """Logic test that the delivery fee is calculated correctly.

    This is for a random payload with no special cases, except
    that it is Friday at 5 pm (so the rush hour surcharge applies).
    """
    payload4 = logic.DeliveryInfo.parse_raw(
        '{"cart_value": 3124, "delivery_distance": 1718, "number_of_items": 6, "time": "2023-09-29T17:03:00Z"}'
    )

    assert payload4.calculate_small_order_surcharge() == 0
    assert payload4.calculate_distance_surcharge() == 400
    assert payload4.calculate_item_number_surcharge() == 100
    assert payload4.calculate_friday_rush_surcharge() == 1.2
    assert payload4.calculate_delivery_fee() == 600


###############################################################

# These next tests are for edge cases, like zero values, etc.
test_zero_items_cart = logic.DeliveryInfo.parse_raw(
    '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 0, "time": "2021-10-12T13:00:00Z"}'
)


def test_zero_items_zero_delivery_fee():
    """Test that the delivery fee for an empty cart is zero.

    An empty cart requires no delivery. This is a special case
    that should be caught by the frontend, but just in case
    something degrades, let's handle it gracefully here.
    """
    assert test_zero_items_cart.calculate_delivery_fee() == 0


test_zero_distance_cart = logic.DeliveryInfo.parse_raw(
    '{"cart_value": 790, "delivery_distance": 0, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'
)


def test_zero_distance_zero_delivery_fee():
    """Test that the delivery fee for a zero-distance cart is zero.

    A zero-distance cart requires no delivery. This is a special case
    that should be caught by the frontend, but just in case
    something degrades, let's handle it gracefully here.
    """
    assert test_zero_distance_cart.calculate_delivery_fee() == 0


test_zero_cost_cart = logic.DeliveryInfo.parse_raw(
    '{"cart_value": 0, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}'
)


def test_zero_cost_cart_nonzero_delivery_fee():
    """Test that the delivery fee for a zero-cost cart is NOT zero.

    Businesses sometimes run free promotions, but we don't want
    to have to subsidize their delivery costs by default for
    such a thing. In more robust code we would probably turn
    this off with a flag, but for the purposes of this exercise
    we'll just assume we never negotiate this.
    """
    assert test_zero_cost_cart.calculate_delivery_fee() != 0
    assert test_zero_cost_cart.calculate_small_order_surcharge() == 1000
