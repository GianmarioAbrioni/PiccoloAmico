import os
import logging
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure the database (SQLite locally, PostgreSQL on Render)
database_url = os.environ.get("DATABASE_URL", "sqlite:///dog_breeding.db")
# Fix for Render PostgreSQL (if URL starts with postgres:// instead of postgresql://)
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Template filters
@app.template_filter('date')
def date_filter(value, format='%d/%m/%Y'):
    if value:
        return value.strftime(format)
    return ""

@app.template_filter('short_date')
def short_date_filter(value):
    if value:
        return value.strftime('%d/%m')
    return ""

@app.template_filter('calculate_age')
def calculate_age(birth_date):
    if birth_date:
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    return ""

@app.template_filter('birth_type')
def birth_type_filter(value):
    """Translate birth type from English to Italian"""
    if not value:
        return ""
    if value == "cesarean":
        return "Cesareo"
    elif value == "natural":
        return "Naturale"
    return value.capitalize()

@app.template_filter('mating_type')
def mating_type_filter(value):
    """Translate mating type from English to Italian"""
    if not value:
        return ""
    if value == "natural":
        return "Naturale"
    elif value == "artificial":
        return "Artificiale"
    return value.capitalize()

# Import models and routes
with app.app_context():
    import models  # noqa: F401
    import routes  # noqa: F401
    import update_routes  # noqa: F401

    # Create all tables
    db.create_all()
