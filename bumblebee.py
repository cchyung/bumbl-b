import os
import re
import time
from flask import Flask, request, jsonify, g
from datetime import datetime
import traceback

from werkzeug.exceptions import HTTPException



app = Flask(__name__)
@app.route('/healthz')
def healthz():
    return "ok", 200

@app.route('/')
def index():
    return "ok", 200


if __name__ == "__main__":
    app.run()
