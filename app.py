from flask import Flask, request, jsonify
import boto3
import random
import datetime

app = Flask(__name__)

# Configure AWS SNS
sns_client = boto3.client('sns', region_name='us-east-1')

# Your database setup will go here (e.g., MongoDB connection)

# OTP storage (for demonstration purposes, using an in-memory dict)
otp_storage = {}

@app.route('/send-otp', methods=['POST'])
def send_otp():
    phone_number = request.json['phone_number']
    otp = generate_otp()

    # Store the OTP with an expiry time
    otp_storage[phone_number] = {
        'otp': otp,
        'expires_at': datetime.datetime.now() + datetime.timedelta(minutes=5)
    }

    # Send OTP via SNS
    sns_client.publish(
        PhoneNumber=phone_number,
        Message=f"Your verification code is {otp}"
    )

    return jsonify({"message": "OTP sent successfully"}), 200

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    phone_number = request.json['phone_number']
    user_input_otp = request.json['otp']

    if phone_number in otp_storage:
        stored_otp_data = otp_storage[phone_number]
        if datetime.datetime.now() > stored_otp_data['expires_at']:
            return jsonify({"message": "OTP expired"}), 400

        if stored_otp_data['otp'] == user_input_otp:
            return jsonify({"message": "OTP verified successfully"}), 200
        else:
            return jsonify({"message": "Invalid OTP"}), 400
    else:
        return jsonify({"message": "OTP not found"}), 400

def generate_otp():
    return str(random.randint(100000, 999999))

if __name__ == '__main__':
    app.run(debug=True)
