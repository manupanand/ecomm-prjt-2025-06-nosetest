"""
Flask CLI Command Extensions
"""
from service import app
from service.models import db


######################################################################
# Command to force tables to be rebuilt
# Usage: flask db-create
######################################################################
@app.cli.command("db-create")
def db_create():
    """
    Recreates a local database. You probably should not use this on production.
    """
    try:
        db.drop_all()
        db.create_all()
        db.session.commit()
        app.logger.info("Database recreated successfully.")
    except Exception as e:
        app.logger.error(f"Error recreating database: {e}")