class RequestBuilder:
    @staticmethod
    def create_user_payload():
        return{
        "name": "QA Test User",
        "username": "qa_test",
        "email": "qa@test.com"
        }
    
    @staticmethod
    def update_user_payload():
        return{
        "name": "QA Test User Updated",
        "username": "qa_test_updated",
        "email": "qa_updated@test.com"
        }