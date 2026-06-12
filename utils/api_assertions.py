class ApiAssertions:

    @staticmethod
    def validate_status_code(response, expected):
        assert response.status_code == expected

    @staticmethod
    def validate_json_structure(response_json, required_fields):
        for field in required_fields:
            assert field in response_json, f"Missing required field: {field}"

    @staticmethod
    def validate_field_present(response_json, field):
        assert field in response_json, f"Missing required field: {field}"

    @staticmethod
    def validate_required_fields(response_json, required_fields):
        for field in required_fields:
            assert field in response_json, f"Missing required field: {field}"

    @staticmethod
    def validate_data_types(response_json, expected_types):
        for field, expected_type in expected_types.items():
            assert field in response_json, f"Missing field for type check: {field}"
            assert isinstance(response_json[field], expected_type), \
                f"Field '{field}' is not of type {expected_type.__name__}"