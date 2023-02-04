"""Wolt Summer Eng Assignment, 2023.

This module is a simple API server which calculates the delivery
fees based on a JSON payload. The business logic is noted at
https://github.com/woltapp/engineering-summer-intern-2023 - for
robustness's sake this doc-only repo is also added here as a git submodule
(`.gitmodule`) but you absolutely don't need it to run the rest of this
project as-is.

Example:
    Start the server::
        poetry install
        poetry run wolt-summer-eng-assignment

Example:
    Run the tests::
        poetry install
        nox

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import click
import uvicorn
from fastapi import FastAPI

from .logic import DeliveryFee
from .logic import DeliveryInfo


app = FastAPI()


@app.post("/")
async def respond_delivery_fee(delivery_info: DeliveryInfo):
    """Respond to the delivery fee request.

    The request payload is a JSON object with the following
    fields:

    - cart_value: int
    - delivery_distance: int
    - number_of_items: int
    - time: str

    The response payload is a JSON object with the following
    fields:

    - delivery_fee: int
    """
    return DeliveryFee(delivery_fee=delivery_info.calculate_delivery_fee())


def start():
    """Start the API server."""
    uvicorn.run(
        "wolt_summer_eng_assignment.__main__:app",
        port=8000,
        reload=True,
    )


@click.command()
@click.version_option()
def main() -> None:
    """Wolt Summer Eng Assignment."""
    print("Hello, world!")
    start()


if __name__ == "__main__":
    main(prog_name="wolt-summer-eng-assignment")  # pragma: no cover
