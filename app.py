from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://fmwaabysivqwbe:a9f0e34cb0f69040b3091799ebcd101625b511af1dab910b36779fc01332955c@ec2-54-160-109-68.compute-1.amazonaws.com:5432/d560aemd6nkddu"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

#Table
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

    def __init__(self, text):
        self.text = text

class AnswerSchema(ma.Schema):
    class Meta:
        fields = ("id", "text")

answer_schema = AnswerSchema()
multiple_answer_schema = AnswerSchema(many=True)

#EndPoints
@app.route("/answers/add", methods=["POST"])
def add_answers():
    if request.content_type != "application/json":
        return jsonify("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    text = post_data.get("text")

    record = Answer(text)
    db.session.add(record)
    db.session.commit()

    return jsonify(answer_schema.dump(record))

@app.route("/answers/get/<id>", methods=["GET"])
def get_answers_by_id(id):
    record = db.session.query(Answer).filter(Answer.id == id).first()
    
    
    return jsonify(answer_schema.dump(record))

if __name__ == "__main__":
    app.run(debug=True)    