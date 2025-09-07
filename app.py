from flask import Flask
from models import DB, Trainers, Appointments
from blueprints.trainers import trainers_bp
from blueprints.appointments import appointments_bp

app = Flask(__name__)
app.register_blueprint(trainers_bp)
app.register_blueprint(appointments_bp)

if __name__ == "__main__":
    DB.connect()
    DB.create_tables([Trainers, Appointments], safe=True)
    DB.close()
    app.run(debug=True)