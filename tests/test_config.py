import unittest
import os
from importlib import reload
import service.config as config


class TestConfig(unittest.TestCase):
    """Testfall för att täcka konfigurationslogik"""

    def test_config_build_uri(self):
        """Det ska bygga DATABASE_URI från enskilda variabler om URI saknas"""
        # Spara undan nuvarande URI om den finns
        original_uri = os.environ.get("DATABASE_URI")

        # Radera DATABASE_URI för att tvinga fram if-satsen (rad 13-17)
        if "DATABASE_URI" in os.environ:
            del os.environ["DATABASE_URI"]

        # Ladda om modulen så att if-satsen körs igen
        reload(config)

        # Kontrollera att den byggde en giltig sträng
        self.assertIn("postgresql://", config.SQLALCHEMY_DATABASE_URI)
        self.assertIn("localhost", config.SQLALCHEMY_DATABASE_URI)

        # Återställ miljön för andra tester
        if original_uri:
            os.environ["DATABASE_URI"] = original_uri
        reload(config)
