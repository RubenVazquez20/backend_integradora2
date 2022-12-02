import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
import os
#Importación el Modelo
from traffic import Street

# games = {}

app = flask.Flask(__name__)
CORS(app)

port = int(os.getenv('PORT', 8000))

@app.rout('/')
def root():
    return jsonify (
        [
            {
                "message" : "funcionando :)"
            }
        ]
    )

@app.route("/", methods=["POST"])
def create():
    global model
    # id = str(uuid.uuid4())
    model = Street()

    response = jsonify("ok")
    response.status_code = 201
    # response.headers['Location'] = f"/games/{id}"
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.autocorrect_location_header = False
    return response

@app.route("/step", methods=["GET"])
def queryState():
    model.step()
    carros = model.getCarros()
    semaforos = model.getSemaforos()
    volantazos = model.getVolantazos()
    return jsonify({"carros": carros, "semaforos": semaforos, "volantazos": volantazos})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= port, debug=True)