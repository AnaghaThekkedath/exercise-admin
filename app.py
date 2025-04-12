# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask
from flask_restx import Api
from exercise.views import exercises_api, programs_api
from exercise.database import init_db

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
api = Api(
    app,
    version='1.0',
    title='Exercise API',
    description='A simple Exercise API',
    doc='/swagger'
)

# Initialize database
init_db()

# Register namespaces
api.add_namespace(exercises_api)
api.add_namespace(programs_api)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)