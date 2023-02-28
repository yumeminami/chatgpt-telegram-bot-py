import unittest
import json
from user.user import update_user_copy
from utils.redis import get_redis_client
class TestUser(unittest.TestCase):
    def test_update_user_copy(self):
        update_user_copy("123",chat_id="123",email="123")
        redis_client = get_redis_client()
        user_copy = redis_client.hget("user", "123")
        user_copy = json.loads(user_copy)
        self.assertEqual(user_copy["email"], "123")



unittest.main()