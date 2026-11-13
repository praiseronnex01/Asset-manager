"""
Asset Management Application Runner
Run this script to launch the local web server.
"""
import os
from app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"🚀 Starting Asset Manager on http://{host}:{port} ...")
    app.run(host=host, port=port, debug=debug)
