"""
Package: service
Fullt dokumenterat paket för kontotjänsten (Account Service).
Detta paket innehåller Flask-applikationen och databasinitieringen.
"""

import sys
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service.common import log_handlers
from service.models import db, init_db

# 1. Skapa Flask-applikationen
app = Flask(__name__)
app.config.from_object("service.config")

# 2. Initiera säkerhet och CORS
talisman = Talisman(app)
CORS(app)

# 3. Set up logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# 4. Initiera databasen
try:
    init_db(app)
    app.logger.info("Database initialized successfully.")
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

# 5. Importera routes sist för att undvika cirkulära beroenden
# pylint: disable=wrong-import-position
from service import routes, models  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# pylint: enable=wrong-import-position

app.logger.info("Service initialized!")
