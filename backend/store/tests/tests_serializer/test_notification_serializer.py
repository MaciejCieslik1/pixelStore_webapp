from datetime import datetime
import unittest

from store.serializers.notification_serializer import FindAllNotificationsSerializer, CreateNotificationSerializer, \
    DeleteNotificationSerializer


class TestFindAlNotificationsSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"date_from": "2025-01-01", "date_to": "2025-02-01", "order": "asc", "page": 2, "page_size": 20}
        parsed_date_from = datetime.strptime(self.data["date_from"], "%Y-%m-%d").date()
        parsed_date_to = datetime.strptime(self.data["date_to"], "%Y-%m-%d").date()
        self.validated_data = {"date_from": parsed_date_from, "date_to": parsed_date_to, "order": "asc", "page": 2, "page_size": 20}

    def test_find_all_success(self):
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_desc(self):
        self.data["order"] = "desc"
        self.validated_data["order"] = "desc"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_delete_spaces(self):
        self.data = {"date_from": "  2025-01-01  ", "date_to": "  2025-02-01  ", "order": "  asc  ", "page": 2, "page_size": 20}
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_none_all_fields(self):
        self.data = {}
        self.validated_data = {"date_from": None, "date_to": None, "order": "desc", "page": 1, "page_size": 10}
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_edge_case(self):
        self.data["page"] = 1
        self.validated_data["page"] = 1
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_min_page_size_edge_case(self):
        self.data["page_size"] = 1
        self.validated_data["page_size"] = 1
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_success_max_page_size_edge_case(self):
        self.data["page_size"] = 100
        self.validated_data["page_size"] = 100
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_date_from(self):
        self.data["date_from"] = ""
        self.validated_data["date_from"] = None
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_date_to(self):
        self.data["date_to"] = ""
        self.validated_data["date_to"] = None
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_order(self):
        self.data["order"] = ""
        self.validated_data["order"] = "desc"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_page(self):
        self.data["page"] = ""
        self.validated_data["page"] = 1
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_empty_page_size(self):
        self.data["page_size"] = ""
        self.validated_data["page_size"] = 10
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_find_all_invalid_data_date_from(self):
        self.data["date_from"] = "wrwggrg"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"date_from": "Date must have YYYY-MM-DD format."})

    def test_find_all_invalid_data_date_to(self):
        self.data["date_to"] = "sfsffsfs"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"date_to": "Date must have YYYY-MM-DD format."})

    def test_find_all_invalid_data_order(self):
        self.data["order"] = "ssfsff"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"order": "Order must be 'asc' or 'desc'."})

    def test_find_all_invalid_data_page(self):
        self.data["page"] = "fwefefefe"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_data_page_size(self):
        self.data["page_size"] = "sffssffs"
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_min_page(self):
        self.data["page"] = 0
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page": "Page number must be a positive integer."})

    def test_find_all_invalid_min_page_size(self):
        self.data["page_size"] = 0
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})

    def test_find_all_invalid_max_page_size(self):
        self.data["page_size"] = 101
        serializer = FindAllNotificationsSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"page_size": "Page size must be between 1 and 100."})


class TestCreateNotificationSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"username": "tester", "text": "Hello"}
        self.validated_data = {"username": "tester", "text": "Hello"}

    def test_create_notification_success(self):
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_notification_success_delete_spaces(self):
        self.data = {"username": "   tester   ", "text": " Hello "}
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_success_max_page_size_edge_case(self):
        self.data["text"] = "a" * 1024
        self.validated_data["text"] = "a" * 1024
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_create_notification_empty_username(self):
        self.data["username"] = ""
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"username": "Username is not provided."})

    def test_create_notification_none_username(self):
        self.data["username"] = None
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"username": "Username is not provided."})

    def test_create_notification_empty_text(self):
        self.data["text"] = ""
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"text": "Text is not provided."})

    def test_create_notification_none_text(self):
        self.data["text"] = None
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"text": "Text is not provided."})

    def test_create_invalid_text_too_long(self):
        self.data["text"] = "a" * 1025
        serializer = CreateNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"text": "Text cannot be longer than 1024 characters."})


class TestDeleteNotificationSerializer(unittest.TestCase):
    def setUp(self):
        self.data = {"notification_id": 1}
        self.validated_data = {"notification_id": 1}

    def test_delete_notification_success(self):
        serializer = DeleteNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertTrue(result)
        self.assertEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {})

    def test_delete_notification_empty_text(self):
        self.data["notification_id"] = ""
        serializer = DeleteNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"notification_id": "Notification id must be a positive integer and exist."})

    def test_delete_notification_none_text(self):
        self.data["notification_id"] = None
        serializer = DeleteNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"notification_id": "Notification id must be a positive integer and exist."})

    def test_delete_notification_not_positive_integer(self):
        self.data["notification_id"] = 0
        serializer = DeleteNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"notification_id": "Notification id must be a positive integer and exist."})

    def test_delete_notification_string(self):
        self.data["notification_id"] = "dfffwfw"
        serializer = DeleteNotificationSerializer(data=self.data)

        result = serializer.is_valid()

        self.assertFalse(result)
        self.assertNotEqual(serializer.validated_data, self.validated_data)
        self.assertEqual(serializer.errors, {"notification_id": "Notification id must be a positive integer and exist."})
