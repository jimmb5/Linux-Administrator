from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="exampledb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")  # Get current database time
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    # HTML content with some basic styling and personalization
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>LEMP App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f8ff;
                color: #333;
                margin-top: 50px;
            }}
            h1 {{
                color: #0077cc;
            }}
            p {{
                font-size: 1.2em;
            }}
        </style>
    </head>
    <body>
        <h1>LEMP Python app toimii!</h1>
        <p>Aika databasesta haettuna: <strong>{result[0]}</strong></p>
        <p>Tämä sivu noudattaa tehtävän antoa ja githubia on käytetty.</p>
        <p style="margin-top: 30px;">
            <a href="/data-analysis" style="display: inline-block; padding: 10px 20px; background-color: #0077cc; color: white; text-decoration: none; border-radius: 5px; font-size: 1.1em;">
                 Tästä data analysis sivulle
            </a>
        </p>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
