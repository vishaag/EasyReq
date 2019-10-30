from flask import Flask, Response, request
import json
import API_bot
import pandas as pd
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import requests
from datetime import datetime


app = Flask(__name__)


user_data = {'name': [None], 'NRIC/FIN': [None], 'Contact Number': [None], 'Email address': [None], 
'LastFourdigitNRIC': [None], 'Relocation Date': [None], 'RelocationAddress': [None], 
'Block No' : [None], 'Floor Number': [None], 'Unit Number': [None], 'Postal Code': [None],
'Race': [None], 'Salutation' : [None],'FULL NRIC/FIN': [None], 'NRIC/Fin Date Issue': [None],'DOB': [None],
'NRIC Front Image': [None], 'NRIC Back Image' : [None], 'Selected Option': [None], 'Relocation DateTime':[None]
}

options = ['Singtel', 'Starhub', 'SP Group', 'Singtel & SP Group', 'Starhub & SP Group']


@app.route("/", methods = ["POST"])
def main():
    
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]
    print(intent_name)


    if(intent_name == "Name"):
        name = req["queryResult"]["parameters"]["person"]["name"]
        user_data["name"] = [name]
        resp_text = name
        resp = {
            "fulfillmentText": resp_text
        }
        
    if(intent_name == "OPTION"):
        selected_option = int(req["queryResult"]["parameters"]["number"])
        user_data["Selected Option"] = [str(selected_option)]
        resp_text = options[selected_option - 1]
        resp = {
            "fulfillmentText": 'You have chosen - ' + resp_text
        }

    if(intent_name == "NRIC"):
        print('nric')
        nric = req["queryResult"]["queryText"]
        nric = nric[5:]
        user_data["FULL NRIC/FIN"] = [nric]
        user_data["NRIC/FIN"] = [nric[1:]]
        user_data["LastFourdigitNRIC"] = [nric[-4:]]
        resp_text = nric
        resp = {
            "fulfillmentText": resp_text
        }
    
    if(intent_name == "PHONE"):
        print('phone')
        phone = req["queryResult"]["parameters"]["phone-number"]
        user_data["Contact Number"] = [phone]
        resp_text = phone
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "EMAIL"):
        print('phone')
        email = req["queryResult"]["parameters"]["email"]
        user_data["Email address"] = [email]
        resp_text = email
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "RELOCATION_DATE"):
        print('relocate date')
        relocate_date = req["queryResult"]["parameters"]["date"]
        print(relocate_date)
        user_data['Relocation DateTime'] =[relocate_date]
        relocate_date = relocate_date[:10]
        print(relocate_date)

        relocate_date = datetime.strptime(relocate_date, '%Y-%m-%d')
        relocate_date = relocate_date.strftime('%d-%m-%Y')
        user_data["Relocation Date"] = [relocate_date]
        print(relocate_date)
        resp_text = relocate_date
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "RELOCATION_ADDRESS"):
        print('new address')
        address = req["queryResult"]["queryText"]
        address = address.split("#")
        address = address[1]
        user_data["RelocationAddress"] = [address]

        address_split = address.split(",")
        print(address_split)

        # get block 
        block = address_split[1]
        block = [int(i) for i in block.split() if i.isdigit()] 
        user_data["Block No"] = [str( block[0])]
        # print(user_data["Block No"])

        #get floor & unit
        floor_unit = address_split[0].split('-')
        floor = floor_unit[0]
        unit = floor_unit[1]
        user_data["Floor Number"] = [str(floor)]
        user_data["Unit Number"] = [str(unit)]
        # print(floor, unit)

        # get postal

        postal = int(address_split[2])
        user_data["Postal Code"] = [str(postal)]
        # print(postal)


        resp_text = address
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "RACE"):
        print('race')
        race = req["queryResult"]["queryText"]
        user_data["Race"] = [race[5:]]
        resp_text = race[5:]
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "SALUTATION"):
        print('salutation')
        salutation = req["queryResult"]["parameters"]["salutation"]
        user_data["Salutation"] = [salutation]
        resp_text = salutation
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "DOB"):
        print('dob')
        dob = req["queryResult"]["parameters"]["date"]
        
        dob = dob[:10]
        dob = datetime.strptime(dob, '%Y-%m-%d')
        dob = dob.strftime('%d-%m-%Y')
    
        user_data["DOB"] = [dob]
        resp_text = dob
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "NRIC_ISSUE_DATE"):
        print('nric issue date')
        nric_issue_date = req["queryResult"]["parameters"]["date"]
        
        nric_issue_date = nric_issue_date[:10]
        nric_issue_date = datetime.strptime(nric_issue_date, '%Y-%m-%d')
        nric_issue_date = nric_issue_date.strftime('%d-%m-%Y')
                        
        user_data["NRIC/Fin Date Issue"] = [nric_issue_date]
        resp_text = nric_issue_date
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "NRIC_IMAGE"):
        print('nric front')
        image = req["originalDetectIntentRequest"]["payload"]["data"]["message"]["attachments"]
        nric_front = image[0]["payload"]["url"]
        nric_back = image[1]["payload"]["url"]

        user_data['NRIC Front Image'] = [nric_front]
        user_data['NRIC Back Image'] = [nric_back]

        print(nric_front)
        print(nric_back)

        filename = 'fin1.png'
        r = requests.get(nric_front, allow_redirects=True)
        open(filename, 'wb').write(r.content)


        filename = 'fin2.png'
        r = requests.get(nric_back, allow_redirects=True)
        open(filename, 'wb').write(r.content)

        if (nric_front is not '' and nric_back is not ''):
            resp_text = 'uploaded!'
        else:
            resp_text = 'Did you upload both front and back?'
        resp = {
            "fulfillmentText": resp_text
        }



    if(intent_name == "DISPLAY_DETAILS"):
        print('details')
        data = ''
        for k,v in user_data.items():
            if(v[0] is not None):
                print(k,v)
                data += k + ' : ' + v[0] + '\n'
        resp_text = data
        resp = {
            "fulfillmentText": resp_text
        }

    if(intent_name == "STATUS"):
        print('status')
        all_filenames = ['Sintel.png', 'Sintel1.png', 'SpGroup.png', 'starhub.png']
        filenames = []
        doesFilesExist = True
        
        for file in all_filenames:
            if(os.path.exists(file)):
                filenames.append(file)
                
        for file in filenames:
            if(not os.path.exists(file)):
                doesFilesExist = False
                
        
        #Set up users for email
        gmail_user = "commonmail721@gmail.com"
        gmail_pwd = "commonmail123"
        recipients = user_data['Email address']
        
        #Create Module
        def mail(to, subject, text, attach):
           msg = MIMEMultipart()
           msg['From'] = gmail_user
           msg['To'] = ", ".join(recipients)
           msg['Subject'] = subject
        
           msg.attach(MIMEText(text))
        
           #get all the attachments
           for file in filenames:
              part = MIMEBase('application', 'octet-stream')
              part.set_payload(open(file, 'rb').read())
              encoders.encode_base64(part)
              part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
              msg.attach(part)
              
           mailServer = smtplib.SMTP("smtp.gmail.com", 587)
           mailServer.ehlo()
           mailServer.starttls()
           mailServer.ehlo()
           mailServer.login(gmail_user, gmail_pwd)
           mailServer.sendmail(gmail_user, to, msg.as_string())
           # Should be mailServer.quit(), but that crashes...
           mailServer.close()
        
        #send it
        if(doesFilesExist):
            mail(recipients,
               "Todays report",
               "Please find attached your status",
               filenames)
            resp_text = 'Your process has been completed. Please check your e-mail for confirmation!'
        else:
            resp_text = 'Your process has not been completed yet. Please check back after a few minutes.'
        
        for file in filenames:
            if(os.path.exists(file)):
                os.remove(file)
              
        resp = {
                "fulfillmentText": resp_text
        }
        

    if(intent_name == "SUBMIT"):
        print('submit')
        returnText = 'Please fill the following before submitting! \n'
        notFilled = False
        for k,v in user_data.items():
            if(v[0] is None):
                returnText += k + '\n'
                notFilled = True
        notFilled = False
        print(notFilled)
        if(notFilled):
            resp_text = returnText
        else:
            
            resp_text = "Submitted! We have started your process. Please check back and type in 'status' to check your form status"
            #call 
            print("calling bot",user_data['Selected Option'][0])
            result = API_bot.main(user_data['Selected Option'][0])
            print(result)
            
        resp = {
                "fulfillmentText": resp_text
        }
        
        

#    pd.DataFrame(user_data).to_excel('out.xlsx', index=False)
  
    return Response(json.dumps(resp), status=200, content_type="application/json")

app.run(host='0.0.0.0', port=5000, debug=True)

			

