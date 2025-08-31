# 🏧 ATM Web Simulator - Python Flask Edition

A fully functional web-based ATM (Automated Teller Machine) simulator built with Python Flask backend and modern HTML/CSS/JavaScript frontend.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Flask](https://img.shields.io/badge/Flask-2.3.3-green) ![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🌟 Features

### Backend (Python Flask)
- **RESTful API**: Clean API endpoints for all ATM operations
- **Session Management**: Secure server-side session handling
- **Data Persistence**: JSON file-based transaction storage
- **Input Validation**: Comprehensive server-side validation
- **Error Handling**: Proper HTTP status codes and error messages

### Frontend Features
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Dynamic UI updates via AJAX calls
- **Interactive Keypad**: Physical ATM keypad simulation
- **Loading States**: Visual feedback for all operations

### Banking Functions
- **Customer Login**: PIN-based authentication (PIN: 1234)
- **Balance Inquiry**: View current account balance
- **Cash Withdrawal**: Withdraw in multiples of £10 with validation
- **PIN Management**: Secure 3-step PIN change process
- **Transaction History**: Persistent transaction logging
- **Admin Access**: Special admin mode (Password: 4321)

## 🚀 Live Demo

[Cash Point Simulator](https://cpsim.netlify.app/)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
```bash
# Create project directory
mkdir atm-simulator-python
cd atm-simulator-python

# Copy the files:
# - app.py
# - requirements.txt
# - templates/index.html
```

2. **Create virtual environment (recommended)**
```bash
python -m venv atm_env

# Activate virtual environment
# On Windows:
atm_env\Scripts\activate
# On macOS/Linux:
source atm_env/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
atm-simulator-python/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend template
├── data/
│   └── transactions.json # Transaction storage (auto-created)
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # For development
export SECRET_KEY=your-secret-key-here  # For production
```

### Default Settings (in app.py)
```python
DEFAULT_PIN = "1234"        # Customer PIN
ADMIN_PASSWORD = "4321"     # Admin password
STARTING_BALANCE = 123.45   # Initial balance
```

## 🌐 API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/logout` - User logout

### Banking Operations
- `GET /api/balance` - Get account balance
- `POST /api/withdraw` - Process withdrawal
- `POST /api/change-pin` - Change PIN (multi-step)
- `GET /api/transactions` - Get transaction history

### Admin Operations
- `GET /api/transactions` - View all transactions (admin)

### Development
- `GET /debug` - View session data (debug mode only)
- `POST /reset-data` - Reset all data (debug mode only)

## 💳 How to Use

### Customer Access
1. Enter PIN: `1234`
2. Press `ENT`
3. Choose from menu options:
   - **A**: View Balance
   - **B**: Withdraw Cash (multiples of £10)
   - **C**: Change PIN (3-step process)
   - **D**: View Transaction History
   - **E**: Exit

### Admin Access
1. Enter Password: `4321`
2. Press `ENT`
3. Admin menu options:
   - **1**: View All Transactions
   - **2**: Exit Admin Mode

### Navigation
- **Keypad**: Click numbers or use keyboard
- **Function Buttons**: Back, Menu, Clear, Help
- **Keyboard Shortcuts**:
  - Numbers: Enter digits
  - Enter: Confirm input
  - Escape: Clear input
  - Backspace: Delete last digit

## 🚀 Deployment Options

### 1. Heroku Deployment

Create `Procfile`:
```
web: python app.py
```

Create `runtime.txt`:
```
python-3.11.0
```

Deploy:
```bash
heroku create your-atm-app
git push heroku main
```

### 2. Railway Deployment
```bash
railway login
railway init
railway up
```

### 3. PythonAnywhere Deployment
1. Upload files to PythonAnywhere
2. Create web app with Flask
3. Set source code path
4. Reload web app

### 4. DigitalOcean App Platform
```yaml
# app.yaml
name: atm-simulator
services:
- name: web
  source_dir: /
  github:
    repo: your-username/atm-simulator
    branch: main
  run_command: python app.py
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
```

### 5. AWS Elastic Beanstalk
```bash
pip install awsebcli
eb init
eb create
eb deploy
```

## 🔒 Security Features

- **Session Management**: Secure server-side sessions
- **PIN Masking**: PINs displayed as asterisks
- **Input Validation**: Server-side validation for all inputs
- **CSRF Protection**: Built-in Flask security features
- **Admin Separation**: Separate admin interface
- **Error Handling**: No sensitive data in error messages

## 🧪 Testing

### Manual Testing
1. **Customer Login**: Test with PIN 1234
2. **Admin Login**: Test with password 4321
3. **Withdrawals**: Test various amounts (valid/invalid)
4. **PIN Change**: Test complete PIN change process
5. **Edge Cases**: Test insufficient funds, invalid inputs

### API Testing with curl
```bash
# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"pin": "1234"}'

# Get balance (after login)
curl -X GET http://localhost:5000/api/balance \
  -b cookies.txt

# Withdraw money
curl -X POST http://localhost:5000/api/withdraw \
  -H "Content-Type: application/json" \
  -d '{"amount": "20"}' \
  -b cookies.txt
```

## 📊 Data Storage

Transaction data is stored in `data/transactions.json`:
```json
[
  {
    "timestamp": "2024-01-15 14:30:25",
    "type": "withdrawal",
    "amount": 20.0,
    "balance_after": 103.45,
    "formatted": "2024-01-15 14:30:25 | Withdrawal £20.00 | Balance £103.45"
  }
]
```

## 🎨 Customization

### Frontend Styling
Modify the CSS in `templates/index.html` to change:
- Color schemes
- Fonts and typography  
- Layout and spacing
- Animations

### Backend Logic
Modify `app.py` to:
- Add new transaction types
- Change validation rules
- Implement new features
- Add database integration

### Adding Database Support
Replace JSON storage with SQLAlchemy:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atm.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    balance_after = db.Column(db.Float, nullable=False)
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   # Or use different port
   flask run --port 5001
   ```

2. **Module not found**
   ```bash
   # Activate virtual environment
   source atm_env/bin/activate
   pip install -r requirements.txt
   ```

3. **Permission denied (data directory)**
   ```bash
   chmod 755 data/
   chmod 644 data/transactions.json
   ```

4. **Session issues in production**
   - Set proper SECRET_KEY environment variable
   - Ensure cookies are enabled
   - Check HTTPS configuration

## 📈 Performance Tips

- Use Redis for session storage in production
- Implement database connection pooling
- Add caching for static content
- Use WSGI server like Gunicorn
- Enable gzip compression

## 🔄 Future Enhancements

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] User account management
- [ ] Transaction receipts (PDF generation)
- [ ] Email notifications
- [ ] Mobile app API
- [ ] Multi-currency support
- [ ] Advanced admin dashboard
- [ ] Audit logging
- [ ] Rate limiting
- [ ] Two-factor authentication

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Website: [yourwebsite.com](https://yourwebsite.com)

## 🙏 Acknowledgments

- Built with Flask - Python web framework
- Inspired by real ATM interfaces
- Designed for educational and demonstration purposes

---

**⭐ Star this repository if you found it helpful!**

## 📞 Support

For issues and questions:
1. Check existing [Issues](https://github.com/yourusername/atm-simulator-python/issues)
2. Create new issue with detailed description
3. Contact author directly

**Happy Banking! 🏧💳**
