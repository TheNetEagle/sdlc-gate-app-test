import unittest

from strutils import reverse


class TestReverse(unittest.TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("abc"), "cba")
        self.assertEqual(reverse(""), "")


if __name__ == "__main__":
    unittest.main()
