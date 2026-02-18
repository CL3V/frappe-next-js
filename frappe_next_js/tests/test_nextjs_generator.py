"""
Tests for the Next.js generator
"""

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestNextJSGenerator(unittest.TestCase):
    """Test cases for NextJSGenerator class."""

    def test_validate_spa_name_same_as_app(self):
        """Test that SPA name cannot be same as app name."""
        from frappe_next_js.commands.nextjs_generator import NextJSGenerator
        
        with self.assertRaises(SystemExit):
            NextJSGenerator(
                spa_name="test_app",
                app="test_app",
                typescript=True,
                tailwindcss=True,
            )

    @patch('frappe_next_js.commands.nextjs_generator.Path')
    def test_validate_spa_name_directory_exists(self, mock_path):
        """Test that generator fails if directory already exists."""
        from frappe_next_js.commands.nextjs_generator import NextJSGenerator
        
        mock_spa_path = MagicMock()
        mock_spa_path.exists.return_value = True
        mock_path.return_value.__truediv__.return_value = mock_spa_path
        
        with self.assertRaises(SystemExit):
            NextJSGenerator(
                spa_name="frontend",
                app="test_app",
                typescript=True,
                tailwindcss=True,
            )


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""

    def test_get_app_package_name(self):
        """Test app name to package name conversion."""
        from frappe_next_js.commands.utils import get_app_package_name
        
        self.assertEqual(get_app_package_name("my-app"), "my_app")
        self.assertEqual(get_app_package_name("my_app"), "my_app")
        self.assertEqual(get_app_package_name("myapp"), "myapp")


if __name__ == "__main__":
    unittest.main()
