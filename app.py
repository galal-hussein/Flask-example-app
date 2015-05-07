from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.script import Manager, Server
from flask.ext.pymongo import PyMongo
import socket


# MongoDB Settings
#Just For Testing
#MONGO_HOST = "104.155.92.47"
MONGO_HOST = "10.42.183.103"
MONGO_PORT = 27017
MONGO_DBNAME = "counter"
#MONGO_REPLICA_SET = "rancher"

SECRET_KEY = "KeepThisS3cr3t"
SITE_WIDTH = 800


app = Flask(__name__)

Bootstrap(app)
manager = Manager(app)
app.config.from_object(__name__)


mongo = PyMongo(app)

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)


@app.route('/')
def cntr():
    mongo.db.rancher.update({"Project" : "Rancher"}, {"$inc" : {"pageviews" : 1}}, True)
    posts = mongo.db.rancher.find({"Project":"Rancher"})[0]
    return render_template('index.html', posts=posts, hostname=socket.gethostname())

@app.route("/healthcheck")
def healthcheck():
    return "200 OK"

if __name__ == '__main__':
    manager.run()
