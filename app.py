from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from flask_socketio import SocketIO
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///delivery.db"
app.config["SECRET_KEY"] = "your_secret_key"
db = SQLAlchemy(app)
socketio = SocketIO(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="قيد التحضير")
    location = db.Column(db.String(50), default="30.0444, 31.2357")

with app.app_context():
    db.create_all()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    token = jwt.encode({"user": data["username"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"token": token})

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{ "id": order.id, "restaurant": order.restaurant, "status": order.status, "location": order.location } for order in orders])

@app.route("/update_order", methods=["POST"])
def update_order():
    order_id = request.json["id"]
    new_status = request.json["status"]
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
        socketio.emit("order_updated", {"id": order_id, "status": new_status})
        return jsonify({"message": "تم تحديث الطلب"})
    return jsonify({"message": "الطلب غير موجود"}), 404

def predict_delivery_time(data):
    model = LinearRegression().fit(data[:, 0].reshape(-1, 1), data[:, 1])
    predicted_time = model.predict(np.array([[25]]))
    return predicted_time[0]

if __name__ == "__main__":
    socketio.run(app, debug=True)
