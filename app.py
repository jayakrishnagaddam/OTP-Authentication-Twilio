from flask import Flask, render_template, request, redirect, url_for, session
from twilio.rest import Client
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def generate_otp():
    return random.randint(100000, 999999)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        if not phone_number.startswith('+'):
            return 'Please enter a valid phone number with country code.'
        
        otp = generate_otp()
        session['otp'] = otp
        session['phone_number'] = phone_number
        
        try:
            message = client.messages.create(
                body=f'Your OTP is {otp}',
                from_=twilio_phone_number,
                to=phone_number
            )
        except Exception as e:
            return f'An error occurred: {str(e)}'
        
        return redirect(url_for('verify_otp'))
    
    return render_template('signup.html')


@app.route('/')
def sign_up():
    return render_template('signup.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if int(user_otp) == session.get('otp'):
            return 'OTP verified successfully!'
        else:
            return 'Invalid OTP, please try again.'
    
    return render_template('verify_otp.html')

if __name__ == '__main__':
    app.run(debug=True)
