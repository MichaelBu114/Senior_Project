import time
import redis
from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=True)
