import pytest

from lib.api_request import ApiRequest


@pytest.fixture
def sender():
	sender = ApiRequest()

	return sender