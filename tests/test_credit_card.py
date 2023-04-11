import pytest

from helpers.support.assertions import assert_valid_schema
from helpers.support.const import *
from helpers.utils import *
from config import settings


REQUEST_PATH = "/api/form/create/credit_parameters_info"
REQUEST_TYPE = "POST"


class TestAdminCreateTicket:
	"""Создание заявки на получение кредитной карты """

	def test_ok(self, sender, credit_card_json):
		"""прошло успешно"""

		data = credit_card_json
		
		sender.add_headers({'Content-Type': 'application/json'})
		sender.set_data(data)

		res = sender.build(REQUEST_TYPE, REQUEST_PATH, user_id=111)

		assert res.status_code == STATUS_CODE_OK
		assert res.text == '"Данные успешно сохранены/изменены на первом этапе"'

	@pytest.mark.parametrize(
		"user_id",
		[
			"test",
			""
		]
	)
	def test_invalid_user_id(self, sender, credit_card_json, user_id):
		"""с невалидным user_id"""

		data = credit_card_json
		
		sender.add_headers({'Content-Type': 'application/json'})
		sender.set_data(data)

		res = sender.build(REQUEST_TYPE, REQUEST_PATH, user_id=user_id)

		payload = text_to_json(res.text)

		assert res.status_code == STATUS_CODE_BAD_REQUEST
		assert_valid_schema(payload, 'error.json')

	def test_without_credit_sum(self, sender, credit_card_json):
		"""без поля credit_sum"""

		data = credit_card_json
		del data["credit_sum"]
		
		sender.add_headers({'Content-Type': 'application/json'})
		sender.set_data(data)

		res = sender.build(REQUEST_TYPE, REQUEST_PATH, user_id="1111")

		payload = text_to_json(res.text)

		assert res.status_code == STATUS_CODE_BAD_REQUEST
		assert_valid_schema(payload, 'error.json')

	@pytest.mark.parametrize(
		"credit_sum",
		[
			"test",
			"",
			"1000.01",
			"1000,22",
			"0",
			"-2000",
			"999",
			"100 000 000",
			20000
		]
	)
	def test_wrong_credit_sum(self, sender, credit_card_json, credit_sum):
		"""с невалидным полем credit_sum"""

		data = credit_card_json
		data["credit_sum"] = credit_sum
		
		sender.add_headers({'Content-Type': 'application/json'})
		sender.set_data(data)

		res = sender.build(REQUEST_TYPE, REQUEST_PATH, user_id="1111")

		payload = text_to_json(res.text)

		assert res.status_code == STATUS_CODE_UNPROCESSIBLE
		assert_valid_schema(payload, 'error_validation.json')

	def test_credit_request_another_type(self, sender):
		"""с невалидным типом запроса"""

		res = sender.build("GET", REQUEST_PATH, user_id="1111")

		payload = text_to_json(res.text)

		assert res.status_code == STATUS_CODE_NO_METHOD
		assert_valid_schema(payload, 'error_no_method.json')

	