import sys
import os
from pathlib import Path

# Ajuste de rutas
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail
from src.app.routes import register_routes
from src.common.vars import HOME_HOST

def create_app():
    app = Flask(__name__, template_folder='templates')

    # --- CONFIGURACIÓN DEL CORREO (GMAIL) ---
    # Nota: Usa contraseña de aplicación de Google (no la contraseña normal)
    # Para generar una: https://myaccount.google.com/apppasswords
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    
    # Obtener credenciales de variables de entorno o usar las configuradas
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'mendozarbarragan19@gmail.com')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'ormy viju fzdk kbmr')
    
    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    # Inicializar Flask-Mail
    app.mail = Mail(app)
    
    print(f"✅ Configuración de correo: {app.config['MAIL_USERNAME']} en {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")

    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)