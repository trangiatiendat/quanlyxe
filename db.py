from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

def init_db(app: Flask):
    # Kết nối tới PostgreSQL
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://quanlyxe_db_user:ieN0pEd72kUvQpD1HVFo6LUKH495DeMl@dpg-ctfjm8t6l47c73b9coi0-a.oregon-postgres.render.com/quanlyxe_db')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo SQLAlchemy
    db.init_app(app)