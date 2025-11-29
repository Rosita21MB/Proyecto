from flask import request, jsonify, render_template, current_app
from src.application.use_cases import UploadBinaryUseCase, SignBinaryUseCase, ApproveBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService
from src.domain.services import SigningService
from src.domain.models import BinaryFile

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/files', methods=['GET'])
    def list_files():
        return jsonify(JsonRepository().list_records()), 200

    @app.route('/upload', methods=['POST'])
    def upload_binary():
        file = request.files['file']
        environment = request.form.get('environment', 'dev')
        
        # Usamos el correo configurado en main.py como destino
        target_email = app.config['MAIL_USERNAME']

        use_case = UploadBinaryUseCase(
            FileRepository(), 
            JsonRepository(), 
            EmailService()
        )
        
        binary = use_case.execute(file, environment, target_email)
        return jsonify(binary.to_dict())

    @app.route("/sign", methods=["POST"])
    def sign_file():
        data = request.get_json()
        use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        result = use_case.execute(data.get("file_id"))
        if result: return jsonify(result.to_dict()), 200
        return jsonify({"error": "Error signing"}), 500

    # --- RUTA QUE SE ABRE DESDE EL CORREO ---
    @app.route('/approve/<file_id>', methods=['GET'])
    def approve_file(file_id):
        sign_use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        approve_use_case = ApproveBinaryUseCase(sign_use_case)
        
        success = approve_use_case.execute(file_id)
        
        if success:
            return """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Archivo Aprobado ✅</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                        background: linear-gradient(135deg, #f5f3ff 0%, #fce7f3 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }
                    
                    .success-container {
                        background: #faf8ff;
                        border-radius: 16px;
                        box-shadow: 0 20px 60px rgba(184, 160, 216, 0.25);
                        padding: 60px 40px;
                        text-align: center;
                        max-width: 600px;
                        border: 1px solid #e9d5ff;
                        animation: slideUp 0.6s ease-out;
                    }
                    
                    @keyframes slideUp {
                        from {
                            opacity: 0;
                            transform: translateY(30px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                    
                    .checkmark {
                        width: 80px;
                        height: 80px;
                        margin: 0 auto 30px;
                        background: linear-gradient(135deg, #b3d9b3 0%, #9dd99d 100%);
                        border-radius: 50%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 50px;
                        animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                        box-shadow: 0 10px 25px rgba(179, 217, 179, 0.4);
                        color: #5a4e6f;
                    }
                    
                    @keyframes popIn {
                        0% {
                            transform: scale(0);
                        }
                        50% {
                            transform: scale(1.1);
                        }
                        100% {
                            transform: scale(1);
                        }
                    }
                    
                    h1 {
                        color: #5a4e6f;
                        font-size: 32px;
                        font-weight: 700;
                        margin-bottom: 15px;
                        letter-spacing: -0.5px;
                    }
                    
                    .subtitle {
                        color: #9b8faa;
                        font-size: 16px;
                        margin-bottom: 25px;
                        line-height: 1.6;
                    }
                    
                    .info-box {
                        background: rgba(212, 191, 255, 0.15);
                        border-left: 4px solid #b8a0d8;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 25px 0;
                        text-align: left;
                    }
                    
                    .info-item {
                        color: #5a4e6f;
                        margin: 10px 0;
                        font-size: 14px;
                    }
                    
                    .info-label {
                        color: #b8a0d8;
                        font-weight: 600;
                        display: inline-block;
                        min-width: 150px;
                    }
                    
                    .steps {
                        margin: 30px 0;
                        text-align: left;
                    }
                    
                    .step {
                        display: flex;
                        margin: 15px 0;
                        color: #5a4e6f;
                    }
                    
                    .step-number {
                        background: linear-gradient(135deg, #b8a0d8 0%, #d4bfff 100%);
                        width: 36px;
                        height: 36px;
                        border-radius: 50%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-weight: 700;
                        color: white;
                        flex-shrink: 0;
                        margin-right: 15px;
                    }
                    
                    .step-text {
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    }
                    
                    .step-title {
                        font-weight: 600;
                        margin-bottom: 3px;
                    }
                    
                    .step-desc {
                        font-size: 13px;
                        color: #9b8faa;
                    }
                    
                    .action-btn {
                        display: inline-block;
                        background: linear-gradient(135deg, #b8a0d8 0%, #d4bfff 100%);
                        color: white;
                        padding: 14px 40px;
                        border-radius: 8px;
                        text-decoration: none;
                        font-weight: 700;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-top: 20px;
                        transition: all 0.3s ease;
                        box-shadow: 0 10px 25px rgba(184, 160, 216, 0.3);
                        border: none;
                        cursor: pointer;
                        font-size: 14px;
                    }
                    
                    .action-btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 15px 35px rgba(184, 160, 216, 0.4);
                    }
                    
                    .footer {
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #e9d5ff;
                        color: #9b8faa;
                        font-size: 12px;
                    }
                </style>
            </head>
            <body>
                <div class="success-container">
                    <div class="checkmark">✓</div>
                    
                    <h1>¡Aprobado y Firmado!</h1>
                    <p class="subtitle">
                        El archivo ha sido procesado exitosamente y firmado digitalmente en el entorno de producción.
                    </p>
                    
                    <div class="info-box">
                        <div class="info-item">
                            <span class="info-label">🎯 Estado:</span>
                            <strong>COMPLETADO</strong>
                        </div>
                        <div class="info-item">
                            <span class="info-label">📝 Acción:</span>
                            <strong>Firma Digital Aplicada</strong>
                        </div>
                        <div class="info-item">
                            <span class="info-label">⏱️ Hora:</span>
                            <strong>Procesado correctamente</strong>
                        </div>
                    </div>
                    
                    <div class="steps">
                        <div class="step">
                            <div class="step-number">1</div>
                            <div class="step-text">
                                <div class="step-title">Validación Completada</div>
                                <div class="step-desc">Se verificó la integridad del archivo</div>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">2</div>
                            <div class="step-text">
                                <div class="step-title">Firma Digital Aplicada</div>
                                <div class="step-desc">Se aplicó la firma criptográfica</div>
                            </div>
                        </div>
                        <div class="step">
                            <div class="step-number">3</div>
                            <div class="step-text">
                                <div class="step-title">Archivo Guardado</div>
                                <div class="step-desc">El archivo firmado está disponible</div>
                            </div>
                        </div>
                    </div>
                    
                    <p style="color: #9b8faa; font-size: 14px; margin-top: 20px;">
                        Puede cerrar esta ventana. El estado será actualizado automáticamente en el panel de control.
                    </p>
                    
                    <button class="action-btn" onclick="window.close(); window.opener.location.reload();">
                        Cerrar y Actualizar
                    </button>
                    
                    <div class="footer">
                        <p>🔐 Transacción segura - Sistema de Firma Digital de Binarios</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            return """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error en la Aprobación ❌</title>
                <style>
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body {
                        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                        background: linear-gradient(135deg, #f5f3ff 0%, #fce7f3 100%);
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        padding: 20px;
                    }
                    
                    .error-container {
                        background: #faf8ff;
                        border-radius: 16px;
                        box-shadow: 0 20px 60px rgba(255, 179, 179, 0.25);
                        padding: 60px 40px;
                        text-align: center;
                        max-width: 600px;
                        border: 1px solid #e9d5ff;
                        animation: slideUp 0.6s ease-out;
                    }
                    
                    @keyframes slideUp {
                        from {
                            opacity: 0;
                            transform: translateY(30px);
                        }
                        to {
                            opacity: 1;
                            transform: translateY(0);
                        }
                    }
                    
                    .error-icon {
                        width: 80px;
                        height: 80px;
                        margin: 0 auto 30px;
                        background: linear-gradient(135deg, #ffb3b3 0%, #ff9999 100%);
                        border-radius: 50%;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 50px;
                        animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                        box-shadow: 0 10px 25px rgba(255, 179, 179, 0.4);
                        color: white;
                    }
                    
                    @keyframes popIn {
                        0% {
                            transform: scale(0);
                        }
                        50% {
                            transform: scale(1.1);
                        }
                        100% {
                            transform: scale(1);
                        }
                    }
                    
                    h1 {
                        color: #5a4e6f;
                        font-size: 32px;
                        font-weight: 700;
                        margin-bottom: 15px;
                        letter-spacing: -0.5px;
                    }
                    
                    .subtitle {
                        color: #9b8faa;
                        font-size: 16px;
                        margin-bottom: 25px;
                        line-height: 1.6;
                    }
                    
                    .error-box {
                        background: rgba(255, 179, 179, 0.15);
                        border-left: 4px solid #ffb3b3;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 25px 0;
                        text-align: left;
                    }
                    
                    .error-message {
                        color: #d9797a;
                        font-size: 14px;
                        line-height: 1.6;
                    }
                    
                    .reasons {
                        margin: 30px 0;
                        text-align: left;
                    }
                    
                    .reason {
                        display: flex;
                        margin: 12px 0;
                        color: #5a4e6f;
                        font-size: 14px;
                    }
                    
                    .reason-icon {
                        color: #e8a651;
                        margin-right: 12px;
                        font-weight: bold;
                    }
                    
                    .action-btn {
                        display: inline-block;
                        background: linear-gradient(135deg, #b8a0d8 0%, #d4bfff 100%);
                        color: white;
                        padding: 14px 40px;
                        border-radius: 8px;
                        text-decoration: none;
                        font-weight: 700;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-top: 20px;
                        transition: all 0.3s ease;
                        box-shadow: 0 10px 25px rgba(184, 160, 216, 0.3);
                        border: none;
                        cursor: pointer;
                        font-size: 14px;
                    }
                    
                    .action-btn:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 15px 35px rgba(184, 160, 216, 0.4);
                    }
                    
                    .footer {
                        margin-top: 40px;
                        padding-top: 20px;
                        border-top: 1px solid #e9d5ff;
                        color: #9b8faa;
                        font-size: 12px;
                    }
                </style>
            </head>
            <body>
                <div class="error-container">
                    <div class="error-icon">✕</div>
                    
                    <h1>Error en la Aprobación</h1>
                    <p class="subtitle">
                        No se pudo procesar la solicitud. Verifique los detalles a continuación.
                    </p>
                    
                    <div class="error-box">
                        <div class="error-message">
                            El archivo no existe, ya fue procesado o el enlace ha expirado.
                        </div>
                    </div>
                    
                    <div class="reasons">
                        <div class="reason">
                            <span class="reason-icon">•</span>
                            <span>El enlace puede haber expirado (máximo 24 horas)</span>
                        </div>
                        <div class="reason">
                            <span class="reason-icon">•</span>
                            <span>El archivo ya fue procesado anteriormente</span>
                        </div>
                        <div class="reason">
                            <span class="reason-icon">•</span>
                            <span>El ID del archivo es inválido</span>
                        </div>
                    </div>
                    
                    <p style="color: #9b8faa; font-size: 14px; margin-top: 20px;">
                        Por favor, contacte con el administrador del sistema si el problema persiste.
                    </p>
                    
                    <button class="action-btn" onclick="window.close();">
                        Cerrar Ventana
                    </button>
                    
                    <div class="footer">
                        <p>🔐 Sistema de Firma Digital de Binarios</p>
                    </div>
                </div>
            </body>
            </html>
            """
    
    @app.route('/clear', methods=['POST'])
    def clear_history():
        try:
            JsonRepository().delete_all()
            FileRepository().delete_all()
            return jsonify({"msg": "ok"}), 200
        except: return jsonify({"error": "err"}), 500