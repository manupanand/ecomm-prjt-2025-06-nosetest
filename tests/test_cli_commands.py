"""
CLI Command Extensions for Flask
"""
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from service.common.cli_commands import db_create


class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = CliRunner()

    @patch('service.common.cli_commands.db')
    def test_db_create(self, db_mock):
        """It should call the db-create command"""
        db_mock.return_value = MagicMock()
        with patch.dict(os.environ, {"FLASK_APP": "service:app"}, clear=True):
            result = self.runner.invoke(db_create)
            self.assertEqual(result.exit_code, 0)
    def test_db_init_command(runner):
        """Test the `flask db init` CLI command"""
        result = runner.invoke(args=["db", "init"])
        assert "Initialized the database" in result.output

    def test_seed_command(runner):
        """Test the `flask seed` CLI command"""
        result = runner.invoke(args=["db", "seed"])
        assert "Seeded the database" in result.output
