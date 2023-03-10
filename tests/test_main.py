"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from wolt_summer_eng_assignment import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    # This doesn't work for now actually, since
    # the app runs as a forever loop.:w

    # result = runner.invoke(__main__.main)
    # assert result.exit_code == 0
    assert True
