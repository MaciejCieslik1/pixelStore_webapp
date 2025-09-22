import unittest

from store.serializers.check_username_serializer import CheckUsernameSerializer


class TestCheckUsernameSerializer(unittest.TestCase):
    def setUp(self):
        self.username = "tester"
        self.validated_username = "tester"

    def test_check_username_correct(self):
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, None)

    def test_check_username_correct_delete_spaces(self):
        self.username = "   tester   "
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, None)

    def test_check_username_correct_delete_spaces_max_length(self):
        self.username = "   " + "a" * 32 + "   "
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, None)

    def test_check_username_empty(self):
        self.username = ""
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, "Username cannot be empty")

    def test_check_username_none(self):
        self.username = None
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, "Username cannot be empty")

    def test_check_username_not_string(self):
        self.username = 2
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, "Username must be string")

    def test_check_username_too_long(self):
        self.username = "   " + "a" * 32 + "   "
        serializer = CheckUsernameSerializer(username=self.username)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_username, self.validated_username)
        self.assertEqual(serializer.error, None)
