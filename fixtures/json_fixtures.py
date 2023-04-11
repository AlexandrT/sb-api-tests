import pytest

from faker import Faker


@pytest.fixture
def credit_card_json(scope="function"):
	fake = Faker('ru_RU')
	gender = fake.random_element(['m', 'f'])
	payload = {
		"credit_target": {
			"value": "credit_card",
			"title": "Кредитная карта"
		},
		"credit_sum": str(fake.random_int(min=1000, max=99999999)),
		"name": fake.first_name_female() if gender == 'f' else fake.first_name_male(),
		"surname": fake.last_name_female() if gender == 'f' else fake.last_name_male(),
		"patronymic": fake.middle_name_female() if gender == 'f' else fake.middle_name_male(),
		"email": fake.email(),
		"phone_number": f"7{fake.numerify('##########')}",
		"gender": {
			"value": "FEMALE" if gender == 'f' else "MALE",
			"title": "Женский" if gender == 'f' else "Мужской"
		}
	}

	return payload