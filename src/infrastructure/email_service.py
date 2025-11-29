
from flask_mail import Message
from flask import current_app, url_for
from datetime import datetime

class EmailService:
    def send_approval_email(self, recipient_email: str, file_id: str, filename: str):
        try:
            # Genera el enlace: http://localhost:8080/approve/ID...
            approval_link = url_for('approve_file', file_id=file_id, _external=True)
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            short_id = file_id[:8] + "..." if len(file_id) > 8 else file_id
            
            # Versión de texto plano como alternativa
            text_body = f"""
SOLICITUD DE APROBACIÓN - FIRMA DIGITAL
═══════════════════════════════════════════════

Hola,

Se ha recibido una solicitud para firmar un archivo en el entorno de PRODUCCIÓN.

DETALLES:
─────────
Archivo:        {filename}
ID de Solicitud: {short_id}
Fecha/Hora:     {current_time}
Estado:         PENDIENTE DE APROBACIÓN

ACCIÓN REQUERIDA:
─────────────────
Para aprobar y firmar digitalmente el archivo, acceda a:
{approval_link}

SEGURIDAD:
──────────
Si usted no solicitó esta acción, ignore este mensaje.
Este enlace expirará después de 24 horas.

═══════════════════════════════════════════════
Sistema de Firma Digital de Binarios
© 2024 - Todos los derechos reservados
            """
            
            # HTML profesional para el correo
            html_body = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Aprobación de Firma Digital</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(135deg, #f5f3ff 0%, #fce7f3 100%);
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        background: #faf8ff;
                        border-radius: 12px;
                        overflow: hidden;
                        box-shadow: 0 20px 50px rgba(184, 160, 216, 0.2);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #b8a0d8 0%, #d4bfff 100%);
                        padding: 40px 30px;
                        text-align: center;
                        color: #5a4e6f;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 700;
                        letter-spacing: -0.5px;
                    }}
                    .content {{
                        padding: 40px 30px;
                        color: #5a4e6f;
                    }}
                    .info-box {{
                        background: rgba(212, 191, 255, 0.15);
                        border-left: 4px solid #b8a0d8;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                    }}
                    .info-row {{
                        display: flex;
                        justify-content: space-between;
                        margin: 12px 0;
                        font-size: 14px;
                    }}
                    .info-label {{
                        color: #9b8faa;
                        font-weight: 600;
                    }}
                    .info-value {{
                        color: #5a4e6f;
                        font-family: 'Courier New', monospace;
                        font-weight: 500;
                    }}
                    .action-section {{
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .btn {{
                        display: inline-block;
                        background: linear-gradient(135deg, #b3d9b3 0%, #9dd99d 100%);
                        color: #5a4e6f;
                        padding: 14px 40px;
                        border-radius: 8px;
                        text-decoration: none;
                        font-weight: 700;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin: 10px 0;
                        transition: transform 0.3s ease;
                        box-shadow: 0 10px 25px rgba(179, 217, 179, 0.3);
                    }}
                    .btn:hover {{
                        transform: translateY(-2px);
                    }}
                    .fallback-text {{
                        color: #9b8faa;
                        font-size: 12px;
                        margin-top: 15px;
                        word-break: break-all;
                    }}
                    .warning {{
                        background: rgba(255, 179, 179, 0.15);
                        border-left: 4px solid #ffb3b3;
                        padding: 15px;
                        border-radius: 8px;
                        margin-top: 20px;
                        font-size: 13px;
                        color: #d9797a;
                    }}
                    .footer {{
                        background: rgba(212, 191, 255, 0.1);
                        padding: 20px 30px;
                        text-align: center;
                        color: #9b8faa;
                        font-size: 12px;
                        border-top: 1px solid #e9d5ff;
                    }}
                    .footer a {{
                        color: #b8a0d8;
                        text-decoration: none;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Aprobación de Firma Digital</h1>
                    </div>
                    
                    <div class="content">
                        <p style="font-size: 16px; margin-top: 0;">Hola,</p>
                        
                        <p style="font-size: 15px; color: #9b8faa; line-height: 1.6;">
                            Se ha recibido una solicitud para firmar un archivo en el entorno de <strong>PRODUCCIÓN</strong>. 
                            Por favor revise los detalles a continuación:
                        </p>
                        
                        <div class="info-box">
                            <div class="info-row">
                                <span class="info-label">📄 Archivo:</span>
                                <span class="info-value">{filename}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">🔑 ID de Solicitud:</span>
                                <span class="info-value">{short_id}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">⏰ Fecha/Hora:</span>
                                <span class="info-value">{current_time}</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">🎯 Estado:</span>
                                <span class="info-value" style="color: #e8a651;">PENDIENTE DE APROBACIÓN</span>
                            </div>
                        </div>
                        
                        <div class="action-section">
                            <p style="font-weight: 600; margin-bottom: 15px; color: #5a4e6f;">Haga clic en el botón a continuación para aprobar y firmar digitalmente el archivo:</p>
                            <a href="{approval_link}" class="btn">Aprobar y Firmar</a>
                            
                            <div class="fallback-text">
                                Si el botón anterior no funciona, copie y pegue este enlace en su navegador:<br>
                                <strong>{approval_link}</strong>
                            </div>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Seguridad:</strong> Si usted no solicitó esta acción, no haga clic en el enlace e ignore este mensaje. 
                            Este enlace expirará después de 24 horas.
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p style="margin: 0 0 10px 0;">
                            Sistema de Firma Digital de Binarios<br>
                            © 2024 - Todos los derechos reservados
                        </p>
                        <p style="margin: 10px 0 0 0;">
                            ¿Preguntas? <a href="mailto:support@example.com">Contacte con soporte</a>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f"🔐 Aprobación Requerida: {filename}",
                recipients=[recipient_email],
                body=text_body,
                html=html_body
            )
            
            current_app.mail.send(msg)
            print(f"✅ Correo enviado exitosamente a {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando correo a {recipient_email}: {str(e)}")
            print(f"   Detalles: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False