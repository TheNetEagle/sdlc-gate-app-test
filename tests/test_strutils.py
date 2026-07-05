import unittest

from strutils import reverse, slugify


class TestReverse(unittest.TestCase):
    def test_reverse(self):
        self.assertEqual(reverse("abc"), "cba")
        self.assertEqual(reverse(""), "")


class TestSlugify(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("  Foo__Bar  "), "foo-bar")
        self.assertEqual(slugify("a---b"), "a-b")
        self.assertEqual(slugify("!!!"), "")
        self.assertEqual(slugify(""), "")

    def test_slugify_strips_leading_trailing_hyphens(self):
        self.assertEqual(slugify("-hi-"), "hi")


if __name__ == "__main__":
    unittest.main()
