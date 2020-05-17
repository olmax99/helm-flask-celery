from flask_restx import Api
from flaskapi.apis.resources.sample_endpoint import ns as ns1

api = Api(title='Project: Docker Flask Api')

api.add_namespace(ns1, path='/api/v0.0/sample')
