#!/usr/bin/env python3
"""
ATM Web Simulator using Flask
A fully functional web-based ATM with Python backend
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from datetime import datetime
import json
import os
from pathlib import Path

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production!

# Configuration
DEFAULT_PIN = "1234"
ADMIN_PASSWORD = "4321"
STARTING_BALANCE = 123.45
TRANSACTION_FILE = Path("data/transactions.json")

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# ========================================
# UTILITY FUNCTIONS
# ========================================

def load_transactions():
    """Load transactions from JSON file"""
    if TRANSACTION_FILE.exists():
        try:
            with open(TRANSACTION_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_transactions(transactions):
    """Save transactions to JSON file"""
    with open(TRANSACTION_FILE, 'w') as f:
        json.dump(transactions, f, indent=2)

def add_transaction(amount, balance_after, transaction_type="withdrawal"):
    """Add a new transaction to the log"""
    transactions = load_transactions()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    transaction = {
        "timestamp": timestamp,
        "type": transaction_type,
        "amount": amount,
        "balance_after": balance_after,
        "formatted": f"{timestamp} | {transaction_type.title()} £{amount:.2f} | Balance £{balance_after:.2f}"
    }
    
    transactions.append(transaction)
    save_transactions(transactions)
    return transaction

def initialize_session():
    """Initialize session variables"""
    if 'pin' not in session:
        session['pin'] = DEFAULT_PIN
    if 'balance' not in session:
        session['balance'] = STARTING_BALANCE
    if 'logged_in' not in session:
        session['logged_in'] = False
    if 'is_admin' not in session:
        session['is_admin'] = False
    if 'pin_change_step' not in session:
        session['pin_change_step'] = 0

def validate_withdrawal(amount_str, balance):
    """Validate withdrawal amount"""
    try:
        amount = float(amount_str)
        
        if amount <= 0:
            return False, "Amount must be greater than £0."
        
        if amount != int(amount):
            return False, "Please enter a whole number (e.g., 10, 20, 30)."
        
        amount = int(amount)
        
        if amount % 10 != 0:
            return False, "Please enter an amount in multiples of £10."
        
        if amount > balance:
            return False, f"Insufficient funds. Your balance is £{balance:.2f}"
        
        return True, amount
        
    except ValueError:
        return False, "Please enter a valid number."

# ========================================
# ROUTES
# ========================================

@app.route('/')
def index():
    """Main ATM interface"""
    initialize_session()
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle login attempts"""
    data = request.get_json()
    pin_attempt = data.get('pin', '')
    
    initialize_session()
    
    # Admin login
    if pin_attempt == ADMIN_PASSWORD:
        session['logged_in'] = True
        session['is_admin'] = True
        return jsonify({
            'success': True,
            'is_admin': True,
            'message': 'Admin login successful!'
        })
    
    # Customer login
    elif pin_attempt == session['pin']:
        session['logged_in'] = True
        session['is_admin'] = False
        transactions = load_transactions()
        return jsonify({
            'success': True,
            'is_admin': False,
            'message': 'Login successful!',
            'transaction_count': len(transactions),
            'balance': session['balance']
        })
    
    else:
        return jsonify({
            'success': False,
            'message': 'Incorrect PIN or password. Please try again.'
        })

@app.route('/api/balance')
def api_balance():
    """Get current balance"""
    if not session.get('logged_in') or session.get('is_admin'):
        return jsonify({'error': 'Not authorized'}), 401
    
    return jsonify({
        'balance': session['balance']
    })

@app.route('/api/withdraw', methods=['POST'])
def api_withdraw():
    """Process withdrawal"""
    if not session.get('logged_in') or session.get('is_admin'):
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    amount_str = data.get('amount', '')
    
    # Validate withdrawal
    valid, result = validate_withdrawal(amount_str, session['balance'])
    
    if not valid:
        return jsonify({
            'success': False,
            'message': result
        })
    
    # Process withdrawal
    amount = result
    session['balance'] -= amount
    
    # Log transaction
    transaction = add_transaction(amount, session['balance'])
    
    return jsonify({
        'success': True,
        'message': f'Success! £{amount:.2f} withdrawn.',
        'balance': session['balance'],
        'transaction': transaction
    })

@app.route('/api/change-pin', methods=['POST'])
def api_change_pin():
    """Handle PIN change process"""
    if not session.get('logged_in') or session.get('is_admin'):
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    pin_input = data.get('pin', '')
    step = session.get('pin_change_step', 0)
    
    if step == 0:
        # Verify current PIN
        if pin_input == session['pin']:
            session['pin_change_step'] = 1
            return jsonify({
                'success': True,
                'step': 1,
                'message': 'Current PIN verified. Enter new PIN.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Incorrect current PIN.'
            })
    
    elif step == 1:
        # Validate new PIN
        if len(pin_input) == 4 and pin_input.isdigit():
            session['new_pin'] = pin_input
            session['pin_change_step'] = 2
            return jsonify({
                'success': True,
                'step': 2,
                'message': 'New PIN entered. Please confirm.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'PIN must be exactly 4 digits.'
            })
    
    elif step == 2:
        # Confirm new PIN
        if pin_input == session.get('new_pin'):
            session['pin'] = session['new_pin']
            session['pin_change_step'] = 0
            session.pop('new_pin', None)
            return jsonify({
                'success': True,
                'step': 0,
                'message': 'PIN changed successfully!',
                'complete': True
            })
        else:
            session['pin_change_step'] = 1
            return jsonify({
                'success': False,
                'step': 1,
                'message': 'PINs do not match. Enter new PIN again.'
            })

@app.route('/api/transactions')
def api_transactions():
    """Get transaction history"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Not authorized'}), 401
    
    transactions = load_transactions()
    
    if session.get('is_admin'):
        # Admin sees all transactions
        return jsonify({
            'transactions': [tx['formatted'] for tx in transactions],
            'count': len(transactions)
        })
    else:
        # Customer sees their transactions (for demo, showing all)
        return jsonify({
            'transactions': [tx['formatted'] for tx in transactions],
            'count': len(transactions)
        })

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Handle logout"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Thank you for using Secure Bank ATM!'
    })

@app.route('/api/reset-pin-change', methods=['POST'])
def api_reset_pin_change():
    """Reset PIN change process"""
    session['pin_change_step'] = 0
    session.pop('new_pin', None)
    return jsonify({'success': True})

# ========================================
# ERROR HANDLERS
# ========================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# ========================================
# DEVELOPMENT ROUTES (Remove in production)
# ========================================

@app.route('/debug')
def debug():
    """Debug endpoint to view session data"""
    if app.debug:
        return jsonify({
            'session': dict(session),
            'transactions': load_transactions()
        })
    return jsonify({'error': 'Debug mode disabled'}), 403

@app.route('/reset-data', methods=['POST'])
def reset_data():
    """Reset all data (development only)"""
    if app.debug:
        session.clear()
        if TRANSACTION_FILE.exists():
            TRANSACTION_FILE.unlink()
        return jsonify({'success': True, 'message': 'All data reset'})
    return jsonify({'error': 'Not available in production'}), 403

# ========================================
# MAIN
# ========================================

if __name__ == '__main__':
    # Development server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)