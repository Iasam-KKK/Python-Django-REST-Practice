from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__, template_folder='../templates')
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",  # Use in-memory storage for rate limiting
)
limiter.init_app(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

from app import routes