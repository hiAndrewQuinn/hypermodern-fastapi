"""Data models for the delivery fee calculation.

The business logic is all inside the DeliveryInfo model.
We test it in test_logic.py.
"""
import arrow
from pydantic import BaseModel


# A whole bunch of global variables,
# because this is a simple project!
SMALL_ORDER_SURCHARGE_LIMIT = 1000
SMALL_ORDER_SURCHARGE_UPPER_DIFF = 1000

SMALL_DISTANCE_SURCHARGE_LIMIT = 1000
SMALL_DISTANCE_SURCHARGE = 200
LARGE_DISTANCE_DELTA = 500
LARGE_DISTANCE_DELTA_SURCHARGE = 100

MANY_ITEMS_SURCHARGE_LIMIT = 5
MANY_ITEMS_SURCHARGE_PER_ITEM = 50
MANY_ITEMS_SURCHARGE_BULK_LIMIT = 12
MANY_ITEMS_SURCHARGE_BULK = 120

MAX_DELIVERY_SURCHARGE = 1500


class DeliveryInfo(BaseModel):
    """Delivery info model. The request payload data model.

    For now the business logic is all inside
    calculate_delivery_fee(self). It isn't elegant, but it is
    simple and easy to understand. We could factor this
    out pretty cleanly if the project evolved.
    """

    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

    def small_order_surcharge(self):
        """Calculate the small order surcharge.

        If the cart value is less than 10€, a small order
        surcharge is added to the delivery price. The surcharge is
        the difference between the cart value and 10€. For example
        if the cart value is 8.90€, the surcharge will be 1.10€.

        We're using global variables for now, but they
        could be easily factored out if we wanted to
        make this more robust to international changes.
        """
        surcharge = 0
        if self.cart_value < SMALL_ORDER_SURCHARGE_LIMIT:
            surcharge += SMALL_ORDER_SURCHARGE_UPPER_DIFF - (self.cart_value)
        return surcharge

    def distance_surcharge(self):
        """Calculate the distance surcharge.

        A delivery fee for the first 1000 meters (=1km) is 2€. If
        the delivery distance is longer than that, 1€ is added for
        every additional 500 meters that the courier needs to travel
        before reaching the destination. Even if the distance would
        be shorter than 500 meters, the minimum fee is always 1€.

        We're using global variables for now, but they
        could be easily factored out if we wanted to
        make this more robust to international changes.
        """
        surcharge = SMALL_DISTANCE_SURCHARGE
        if self.delivery_distance > SMALL_DISTANCE_SURCHARGE_LIMIT:
            additional_distance_intervals = (
                1
                + (self.delivery_distance - SMALL_DISTANCE_SURCHARGE_LIMIT)
                // LARGE_DISTANCE_DELTA
            )
            surcharge += additional_distance_intervals * LARGE_DISTANCE_DELTA_SURCHARGE
        return surcharge

    def item_number_surcharge(self):
        """Calculate the item number surcharge.

        If the number of items is five or more, an additional 50
        cent surcharge is added for each item above and including
        the fifth item. An extra "bulk" fee applies for more than
        12 items of 1,20€.

        We're using global variables for now, but they
        could be easily factored out if we wanted to
        make this more robust to international changes.
        """
        surcharge = 0

        if self.number_of_items > MANY_ITEMS_SURCHARGE_LIMIT:
            surcharge += MANY_ITEMS_SURCHARGE_PER_ITEM * (
                self.number_of_items - MANY_ITEMS_SURCHARGE_LIMIT
            )
        if self.number_of_items > MANY_ITEMS_SURCHARGE_BULK_LIMIT:
            surcharge += MANY_ITEMS_SURCHARGE_BULK
        return surcharge

    def friday_rush_surcharge(self):
        """Calculate the Friday rush surcharge.

        During the Friday rush (3 - 7 PM UTC), the delivery fee (the
        total fee including possible surcharges) will be multiplied
        by 1.2x. However, the fee still cannot be more than the max
        (15€).

        We're using global variables for now, but they
        could be easily factored out if we wanted to
        make this more robust to international changes.
        """
        utc_time = arrow.get(self.time).to("UTC")
        if all(
            [
                utc_time.weekday() == 5,
                utc_time.hour >= (12 + 3),
                utc_time.hour <= (12 + 7),
            ]
        ):
            return 1.2
        else:
            return 1.0

    def calculate_delivery_fee(self):
        """Method to calculate the delivery fee.

        This used to be a bunch of nested functions, but
        I've refactored them out to make the logic more
        readable. The return is the same as before.
        """
        # Handle the null case. An empty cart isn't supposed to
        # be ordered, but let's not charge someone if it is.
        if self.cart_value == 0:
            return 0
        return int(
            min(
                MAX_DELIVERY_SURCHARGE,
                (
                    self.small_order_surcharge()
                    + self.distance_surcharge()
                    + self.item_number_surcharge()
                )
                * self.friday_rush_surcharge(),
            )
        )


class DeliveryFee(BaseModel):
    """Delivery fee model. The response payload data model.

    The delivery fee is in cents, hence the int type.
    """

    delivery_fee: int
