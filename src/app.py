from flask import Flask, url_for

from app_scheduler import scheduler
from routes import pages

app = Flask(__name__)

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())


scheduler.init_app(app)
scheduler.start()

app.register_blueprint(blueprint=pages)
