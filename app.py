from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEM_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

#Table
class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

    def __init__(self, text):
        self.text = text

class AnswerSchema(ma.Schema):
    class Meta:
        fields = ("id", "text")

answer_schema = AnswerSchema()
multiple_answer_schema = AnswerSchema(many=True)


@app.route("/answers/add", methods=["POST"])
def add_quote():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    text = post_data.get("text")

    record = Quote(text)
    db.session.add(record)
    db.session.commit()

    return jsonify(quote_schema.dump(record))

@app.route("/quote/get/<id>", methods=["GET"])
def get_quote_by_id(id):
    record = db.session.query(Quote).filter(Quote.id == id).first()
    return jsonify(quote_schema.dump(record))