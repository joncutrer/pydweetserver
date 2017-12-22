from flask import Flask, request, send_from_directory, render_template
from flask_restful import Resource, Api
import flask_pymongo
from flask_pymongo import PyMongo
from datetime import datetime
import time
import uuid


app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'pydweetserver'
mongo = PyMongo(app)

# Serve the HTML Docs [Human Interface]
@app.route('/docs/')
def serve_docs():
    return send_from_directory('docs', 'index.html')

# Serve Server Stats [Human Interface]
@app.route('/stats/')
def serve_stats():
    return render_template('stats.html')


# Serve Dweet index [Human Interface]
@app.route('/see')
def dweet_index():
    dweets = mongo.db.dweets.find()
    return render_template('see.html', dweets=dweets)


# Serve Dweet detail [Human Interface]
@app.route('/follow/<string:thing>')
def dweet_follow(thing):
    dweet = mongo.db.dweets.find_one({'thing': thing})
    return render_template('follow.html', dweet=dweet)

# Serve Dweet add [Human Interface]
@app.route('/add')
def dweet_add():
    dweets = mongo.db.dweets.find()
    return render_template('see.html', dweets=dweets)


class Root(Resource):
    def get(self):
        return {
            'server': 'pydweetserver', 
            'description': 'Dweet.io API Compliant REST Web Server written in Python/Flask/MongoDB', 
            'url': 'https://github.com/joncutrer/pydweetserver',
            'version': '0.0.1',
            'author': 'Jonathan Cutrer',
            'docs': '/docs'
        }


class CaughtEmptyDweet(Resource):
    def get(self):
        # Error if thing is empty
        return {
            'this': 'failed',
            'with': 404,
            'because': 'we couldn\'t find this'
        }


class DweetFor(Resource):
    def get(self, thing):

        # Compose the thing
        newthing = {
            'thing': thing,
            'created': str(datetime.utcnow()),
            'content': request.args,
            'transaction': str(uuid.uuid4())
        }

        archivething = {**newthing}

        #Update the thing in dweets database
        mongo.db.dweets.update_one(
                {'thing': thing}, 
                {
                    '$set': newthing
                },
                upsert=True
        )

        #Insert the thing in history database
        mongo.db.history.insert_one( archivething )

        # response
        return {
            'this': 'succeeded',
            'by': 'dweeting',
            'the': 'dweet',
            'with': newthing
        }

    def post(self): 
        return {'todo': 'set some data via post'}


class DweetQuietlyFor(Resource):
    def get(self, thing):
        msg = 'set some data for thing named ' + thing
        return {'todo': msg }
    def post(self):
        return {'todo': 'set some data via post'}


class GetLatestDweetFor(Resource):
    def get(self, thing):

        dweet = mongo.db.dweets.find_one({'thing': thing})
        
        # no thing found
        if not dweet:
            return {"this":"failed","with":404,"because":"we couldn't find this"}
        
        dweet.pop('_id', None)
        dweet.pop('transaction', None)

        # response
        return {
            'this': 'succeeded',
            'by': 'getting',
            'the': 'dweets',
            'with': dweet
        }


class GetDweetsFor(Resource):
    def get(self, thing):

        dweets = []
        for dweet in mongo.db.history.find({'thing': thing}).sort("created", flask_pymongo.DESCENDING):
            dweet.pop('_id', None)
            dweet.pop('transaction', None)
            dweets.append(dweet)

        # no thing found
        if not dweets:
            return {"this":"failed","with":404,"because":"we couldn't find this"}
        
        # response
        return {
            'this': 'succeeded',
            'by': 'getting',
            'the': 'dweets',
            'with': dweets
        }


# begin routes
# dweets
api.add_resource(Root, '/')
api.add_resource(CaughtEmptyDweet, '/dweet/for/')
api.add_resource(DweetFor, '/dweet/for/<string:thing>')
api.add_resource(DweetQuietlyFor, '/dweet/quietly/for/<string:thing>')
api.add_resource(GetLatestDweetFor, '/get/latest/dweet/for/<string:thing>')
api.add_resource(GetDweetsFor, '/get/dweets/for/<string:thing>')
#api.add_resource(ListenForDweetsForm, '/listen/for/dweets/form/<string:thing>')

# end routes
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
