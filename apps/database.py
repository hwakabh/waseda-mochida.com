from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from apps.settings import DatabaseConfigs

class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


# expecting args `app` is type Flask
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # Migrate(app, db)
    return db
