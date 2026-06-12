from api.api_client import APIClient
import pytest

from api.endpoints import Endpoints
from test_data.api_test_data import EXPECTED_USER_FIELDS, USER_DATA_TYPES
from utils.api_assertions import ApiAssertions

@pytest.mark.api
@pytest.mark.smoke
def test_get_user_by_id(api_client: APIClient):
    """Test: GET /users/1 returns correct user data structure and types."""
    response = api_client.get(f"{Endpoints.USERS}/1")
    ApiAssertions.validate_status_code(response, 200)

    user_data = response.json()
    ApiAssertions.validate_json_structure(user_data, EXPECTED_USER_FIELDS)
    
    ApiAssertions.validate_data_types(user_data, USER_DATA_TYPES)

    # Validate expected fields are present
    for field in EXPECTED_USER_FIELDS:
        ApiAssertions.validate_field_present(user_data, field)

    # Validate data types of key fields
    for field, expected_type in USER_DATA_TYPES.items():
        assert isinstance(user_data[field], expected_type), (
            f"Field '{field}' is not of type {expected_type.__name__}"
        )