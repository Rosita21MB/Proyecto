# 🔐 Digital Binary Signing System

![upsrj-logo](docs/img/upsrj.png)

**Politécnica de Santa Rosa** - Software Architectures Final Project

| Property | Value |
|----------|-------|
| **Subject** | Software Architectures |
| **Title** | Final Project - Digital Binary Signing System |
| **Owner** | Rosaura Mendoza Barragan (023000360@upsrj.edu.mx) |
| **Status** | ✅ Completed & Deployed |
| **Last Updated** | November 28, 2025 |

---

## 🎯 Project Overview

A Flask-based web application for secure digital signing of binary files with environment-based approval workflows. Features a modern pastel UI, professional email system, advanced file validation, and dual environment support (Development Auto-Sign, Production Email-Approval).

### ✨ Key Features

- 🎨 **Modern Pastel UI** - Beautiful responsive design with smooth animations
- 📧 **Professional Email System** - HTML-formatted approval emails with security features
- ✔️ **Advanced File Validation** - Size limits, type checking, real-time feedback
- 🔐 **Digital Signatures** - Cryptographic signing with RSA/Fernet encryption
- 📊 **Dual Environment Support** - Dev (auto-sign) and Prod (email approval)
- 🎯 **Production Workflow** - Email-based approval with secure approval links
- 💾 **Persistent Storage** - JSON database with file tracking

---

## 🏗️ Architecture

### Deployment Diagram
![Deployment](docs/img/deployment.png)

### Components UML
![Components UML](docs/img/components.png)

### Project Structure

```
ProyectoFinal/
│
├── src/
│   ├── app/
│   │   ├── _init_.py
│   │   ├── main.py                 # Flask entrypoint with mail config
│   │   ├── routes.py               # HTTP routes + approval pages
│   │   └── templates/
│   │       └── home.html           # Pastel UI with real-time validation
│   │
│   ├── domain/
│   │   ├── _init_.py
│   │   ├── models.py               # Entities: BinaryFile, Signature
│   │   └── services.py             # Domain logic: signing, validation
│   │
│   ├── application/
│   │   ├── _init_.py
│   │   ├── use_cases.py            # Use cases: upload, sign, approve
│   │   └── ports.py                # Interfaces to infrastructure
│   │
│   ├── infrastructure/
│   │   ├── _init_.py
│   │   ├── file_repository.py      # File storage management
│   │   ├── json_repository.py      # JSON-based database simulation
│   │   ├── email_service.py        # Professional email sending
│   │   └── crypto_adapter.py       # Cryptographic operations
│   │
│   ├── common/
│   │   ├── _init_.py
│   │   └── vars.py                 # Global configuration variables
│   │
│   └── config/
│       ├── _init_.py
│       └── settings.py             # Environment-specific settings
│
├── data/
│   ├── binaries/                   # Uploaded binary files
│   ├── signed/                     # Digitally signed files
│   ├── dev_keys/                   # Development cryptographic keys
│   └── prod_keys/                  # Production cryptographic keys
│
├── docs/
│   ├── headers/                    # Documentation headers
│   ├── img/                        # Diagrams and images
│   └── tree/                       # Structure documentation
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py                # Main test suite
│   └── vars.py                     # Test configuration
│
├── database.json                   # Local database file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🎨 UI Design

### Color Palette (Pastel Theme)

| Name | Color | Usage |
|------|-------|-------|
| **Primary** | #b8a0d8 | Buttons, headers, links |
| **Secondary** | #d4bfff | Accents, highlights |
| **Success** | #b3d9b3 | Success messages, status |
| **Warning** | #ffe4b3 | Warning messages |
| **Error** | #ffb3b3 | Error messages |
| **Background** | #f5f3ff → #fce7f3 | Gradient background |
| **Text** | #5a4e6f | Main text color |

### Animations & Effects

- ✨ Smooth slide-in animations for notifications
- 🎯 Pop-in effect for status indicators
- 🖱️ Hover effects on all interactive elements
- ⏳ Loading state transitions with feedback

---

## 📧 Email System

### Professional Email Template

The system sends beautifully formatted HTML emails with:
- Pastel color scheme matching the UI
- Clear approval buttons with fallback links
- Security information and expiration notices
- Plain text alternative for compatibility

### Email Features

- **HTML Templates**: Modern responsive design
- **Plain Text Fallback**: Compatibility with all email clients
- **Security Warnings**: Link expiration (24 hours) notification
- **Detailed Information**: File name, ID, timestamp, status
- **One-Click Approval**: Secure approval links from email

### Gmail Configuration

To send emails via Gmail:

1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com
   - Settings → Security → 2-Step Verification

2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password

3. **Configure in main.py** or use environment variables:
   ```bash
   export MAIL_USERNAME=your_email@gmail.com
   export MAIL_PASSWORD=your_16_char_app_password
   ```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- Gmail account (for email features)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Rosita21MB/Proyecto.git
cd Proyecto

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure email (optional)
# Edit src/app/main.py or set environment variables

# 4. Run the application
python src/app/main.py
```

### Running the Application

```bash
cd ProyectoFinal_Entrega
python src/app/main.py
```

The application will start on:
- **Local**: http://127.0.0.1:8080
- **Network**: http://192.168.1.181:8080 (adjust IP as needed)

---

## 📊 API Endpoints

### Web Interface

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with upload form |
| GET | `/files` | List all processed files (JSON) |
| POST | `/upload` | Upload and process binary file |
| POST | `/sign` | Sign file (development environment) |
| GET | `/approve/<file_id>` | Approve and sign from email link |
| POST | `/clear` | Clear all files and database |

### Request Examples

**Upload File**
```bash
curl -X POST -F "file=@binary.bin" \
     -F "environment=dev" \
     http://127.0.0.1:8080/upload
```

**List Files**
```bash
curl http://127.0.0.1:8080/files
```

**Sign File (Dev)**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"file_id":"xxx-xxx-xxx"}' \
     http://127.0.0.1:8080/sign
```

---

## 🔐 Security Features

### File Validation

- **Size Limits**: 
  - Maximum: 500 MB
  - Minimum: 1 KB
- **Type Checking**: Support for `.exe`, `.bin`, `.dll`, `.so`, `.elf`
- **Real-time Feedback**: Visual indicators for validation status

### Digital Signatures

- **Algorithm**: Fernet (symmetric encryption)
- **Key Generation**: Secure random key generation
- **Signature Storage**: Hash-based signature tracking

### Email Security

- **Link Expiration**: 24-hour expiration on approval links
- **Secure Transport**: TLS encryption with Gmail SMTP
- **App Passwords**: OAuth app-specific passwords (not main password)

### Data Protection

- **File Encryption**: Signed files stored securely
- **Database**: JSON with structured record tracking
- **Access Control**: Environment-based restrictions

---

## 🔄 Workflow Examples

### Development Environment (Auto-Sign)

```
1. Upload file
   └─ File stored in /data/binaries/
   └─ Record added to database.json
   
2. Auto-sign triggered
   └─ Signature generated
   └─ Signed file saved to /data/signed/
   └─ Status changed to "signed"
   
3. Immediate availability
   └─ User sees signed status in UI
   └─ File ready for download
```

### Production Environment (Email Approval)

```
1. Upload file
   └─ File stored in /data/binaries/
   └─ Record added to database.json
   └─ Status set to "pending"
   
2. Approval email sent
   └─ HTML formatted email
   └─ Unique approval link generated
   └─ Email sent to configured address
   
3. Email review
   └─ User receives professional email
   └─ Clicks approval button or link
   
4. Approval & signing
   └─ Link verification
   └─ Signature generated
   └─ Signed file saved
   └─ Status changed to "signed"
   
5. Notification
   └─ Success page displayed
   └─ File available in main dashboard
```

---

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_main.py

# Run with verbose output
python -m pytest tests/ -v
```

### Manual Testing

1. **File Upload Validation**
   - Try uploading files larger than 500 MB → Should show error
   - Try uploading empty files → Should show error
   - Upload valid binary file → Should succeed

2. **Development Environment**
   - Select "dev" environment
   - Upload file → Should auto-sign immediately
   - Check file list for "signed" status

3. **Production Environment**
   - Select "prod" environment
   - Upload file → Status should be "pending"
   - Check email for approval link
   - Click link and verify signing

---

## 🛠️ Configuration

### Environment Variables

```bash
# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password

# Server Configuration
FLASK_ENV=development  # or production
DEBUG=True             # or False
```

### Configuration Files

- **src/common/vars.py**: Global variables and port settings
- **src/app/main.py**: Flask app configuration and mail settings
- **src/config/settings.py**: Environment-specific settings

---

## 📦 Dependencies

### Core Dependencies

```
flask==3.1.2              # Web framework
flask-mail==0.10.0        # Email sending
cryptography==46.0.3      # Cryptographic operations
```

See `requirements.txt` for complete list.

---

## 📈 Performance

- **File Upload**: < 2 seconds
- **Email Send**: < 5 seconds
- **File Signing**: < 1 second
- **Page Load**: < 500ms

---

## 🐛 Troubleshooting

### Email Not Sending

**Problem**: "Username and Password not accepted"

**Solution**:
1. Verify you're using an App Password (not main password)
2. Check 2FA is enabled on your Google Account
3. Verify email and password are correct in main.py
4. Check internet connection to SMTP server

### File Upload Issues

**Problem**: "File too large"

**Solution**: Maximum file size is 500 MB. Compress or split larger files.

**Problem**: "File type not supported"

**Solution**: Only `.exe`, `.bin`, `.dll`, `.so`, `.elf` files are supported.

### Port Already in Use

**Problem**: "Address already in use"

**Solution**: 
- Change port in `src/common/vars.py`
- Or kill the process using the port

---

## 📝 Development Notes

### Code Structure

- **Hexagonal Architecture**: Separation of concerns with adapter pattern
- **Clean Code**: SOLID principles applied throughout
- **Error Handling**: Comprehensive exception handling with logging
- **Comments**: Spanish comments for educational purposes

### File Organization

- Domain logic isolated in `domain/` package
- Use cases in `application/` package
- External adapters in `infrastructure/` package
- Web interface in `app/` package

---

## 🔄 Recent Updates (v2.0)

- ✅ Pastel color theme implementation
- ✅ Professional HTML email templates
- ✅ Advanced file validation system
- ✅ Real-time validation feedback
- ✅ Improved error handling and logging
- ✅ Approval page redesign
- ✅ Enhanced security notices

---

## 🤝 Contributing

For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Contributors

**Rosaura Mendoza Barragan**
- Student ID: 023000360
- Email: 023000360@upsrj.edu.mx
- Institution: Politécnica de Santa Rosa
- Subject: Software Architectures

---

## 🎓 Academic Context

This is a final project for the **Software Architectures** course at **Politécnica de Santa Rosa**, demonstrating:

- Clean architecture principles
- Design patterns (Adapter, Repository, Use Case)
- Secure file handling
- Email integration
- Web development best practices
- Professional UI/UX design

---

## 📞 Support & Contact

For questions or issues:
- Email: 023000360@upsrj.edu.mx
- GitHub Issues: [Project Issues](https://github.com/Rosita21MB/Proyecto/issues)

---

**Project Status**: ✅ Production Ready  
**Last Updated**: November 28, 2025  
**Version**: 2.0
