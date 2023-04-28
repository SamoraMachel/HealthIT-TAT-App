# Your code goes here
from flask import Flask, request
app = Flask(__name__)

response = ""

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    if text == '':
        response  = "CON Dear patient you test results are ready. Kindly enter the day when you'll be able to collect them \n"
        response += "1. 1 day \n"
        response += "2. 4 days \n"
        response += "3. 7 days \n"
        response += "4. 14 days \n"
        response += "00. Opt Out \n"

    elif text == '1':
        response = "END Dear patient thank you for your response, we expect you in a days time"
    elif text == '2':
        response = "END Dear patient thank you for your response, we expect you within 4 days"
    elif text == '3':
        response = "END Dear patient thank you for your response, we expect you within 7 days"

    elif text == '4':
        response = "END Dear patient thank you for your response, we expect you within 14 days"
    elif text == '00':
        response = "END Your have opt Out Successfully"
    else:
        response = "CON Not a valid Response. Select one from below.\n"
        response += "1. 1 day \n"
        response += "2. 4 days \n"
        response += "3. 7 days \n"
        response += "4. 14 days \n"
        response += "00. Opt Out \n"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9005, debug=True)