import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.pdf_routes import pdf_bp

def create_app():
    app = Flask(__name__)
    
    # Enable Cross-Origin Resource Sharing (CORS) so our local frontend (usually port 5173)
    # can communicate with the backend API (port 5000)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register modular blueprints
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")

    # Simple health check route
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy", "service": "scan_to_pdf_backend"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    # Run server locally on 127.0.0.1:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
