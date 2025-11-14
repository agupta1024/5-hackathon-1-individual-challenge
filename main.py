from flask import Flask, Blueprint, Response
from flask import request, url_for
from endpoints import stars_bp, std_bp, avg_bp, health_bp
from endpoints import min_bp, max_bp, argmin_bp, argmax_bp
app = Flask(__name__)
app.register_blueprint(stars_bp, url_prefix='/<org>/stars')
app.register_blueprint(std_bp, url_prefix='/<org>/std')
app.register_blueprint(avg_bp, url_prefix='/<org>/avg')
app.register_blueprint(min_bp, url_prefix='/<org>/min')
app.register_blueprint(max_bp, url_prefix='/<org>/max')
app.register_blueprint(argmin_bp, url_prefix='/<org>/argmin')
app.register_blueprint(argmax_bp, url_prefix='/<org>/argmax')
app.register_blueprint(health_bp, url_prefix='/healthz')


if __name__ == "__main__":
    app.run(debug=True, port=8000)


