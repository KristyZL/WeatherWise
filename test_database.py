import unittest
import database  # Import your module

class TestDatabase(unittest.TestCase):
    def test_connection(self):
        conn = database.get_connection()
        self.assertIsNotNone(conn)

if __name__ == "__main__":
    unittest.main()