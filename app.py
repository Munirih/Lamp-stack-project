from flask import Flask
import socket
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def get_db_connection():
    """
    Creates and returns a MySQL database connection.
    Reads all credentials from environment variables — never hardcoded.
    Returns None if the connection fails, so the app still runs without DB.
    """
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),         # Private subnet EC2 IP e.g. 10.0.2.45
            port=int(os.environ.get("DB_PORT", 3306)),
            database=os.environ.get("DB_NAME"),     # e.g. lampdb
            user=os.environ.get("DB_USER"),         # e.g. lampuser
            password=os.environ.get("DB_PASSWORD"), # stored in GitHub Secrets / .env file
            connect_timeout=5                        # fail fast if DB is unreachable
        )
        return connection
    except Error as e:
        print(f"[DB] Connection failed: {e}")
        return None


def get_db_status():
    """
    Tries to connect to the database and run a simple query.
    Returns a status string shown on the homepage.
    """
    connection = get_db_connection()
    if connection is None:
        return "❌ Database unreachable"
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        connection.close()
        return f"✅ Connected — MySQL {version[0]}"
    except Error as e:
        return f"❌ Query failed: {e}"


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def home():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    db_status = get_db_status()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LAMP Stack Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                text-align: center;
                min-width: 400px;
            }}
            h1 {{ color: #333; margin-bottom: 20px; }}
            .info {{
                background: #f0f0f0;
                padding: 20px;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .label {{ font-weight: bold; color: #667eea; }}
            .value {{ color: #333; font-size: 1.2em; }}
            .db {{ background: #e8f5e9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🖥️ LAMP Stack Demo App</h1>
            <div class="info">
                <p class="label">Server Hostname:</p>
                <p class="value">{hostname}</p>
            </div>
            <div class="info">
                <p class="label">Server IP Address:</p>
                <p class="value">{ip_address}</p>
            </div>
            <div class="info">
                <p class="label">App Status:</p>
                <p class="value">✅ Server is running!</p>
            </div>
            <div class="info db">
                <p class="label">Database (Private Subnet):</p>
                <p class="value">{db_status}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


@app.route('/health')
def health():
    """
    Health check endpoint used by CI/CD pipeline to verify deployment succeeded.
    Also checks database connectivity so we know if the private subnet link is working.
    """
    db_status = get_db_status()
    return {
        'status': 'healthy',
        'hostname': socket.gethostname(),
        'database': db_status
    }, 200


if __name__ == '__main__':
    # Run on port 5000 — NGINX will sit in front and forward traffic to here
    app.run(host='0.0.0.0', port=5000, debug=False)
