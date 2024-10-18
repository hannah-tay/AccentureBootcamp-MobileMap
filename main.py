from flask import Flask, request, jsonify
from flask_restx import Api
from app import Route, NewRoute, HazardIdentification

application = Flask(__name__)

# Create a Flask-RESTX Namespace
api = Api(application, doc='/docs/', default='mappi', default_label='Super API', version='1.0')
auth_ns = api.namespace('api/v2/auth', description='Authentication operations')

mappi_namespace = api.namespace('api/',
                                    description='Mappi API')

# route resources
mappi_namespace.add_resource(Route, '/route')
mappi_namespace.add_resource(NewRoute, '/new_route')

# hazard identification resource
mappi_namespace.add_resource(HazardIdentification, '/hazard')

# route processing for use case
@application.route('/process_routes', methods=['POST'])
def process_routes():
    data = request.get_json()

    response = []
    response.append(Route().post()) # run route method by default

    # run reroute method if a hazard is reported and the user confirms
    if data['user_confirmation']==1 and data['except_coords']:
        response.append(NewRoute().post())

    return jsonify(response)

# json data for postman
# {
#     "start_coords": [-37.83360117708017, 144.98787920571158],
#     "end_coords": [-37.83354253194787, 144.98234802465515],
#     "except_coords": [-37.834644, 144.987392],
#     "user_confirmation": 1
# }

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8888,debug=True)
