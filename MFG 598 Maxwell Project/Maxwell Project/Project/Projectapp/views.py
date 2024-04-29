from django.shortcuts import render,HttpResponse,redirect
import pymongo
from django.contrib import messages
from Projectapp.models import SignUp;
import hashlib
import joblib
import numpy as np
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import base64
import json
from io import BytesIO
# Create your views here.
number=random.randrange(100000,999999)
url="mongodb://localhost:27017"
client=pymongo.MongoClient(url)
db=client['maxwell_project']
col = db["Projectapp_signup"]
special_char='[@_!$%^&*()<>?/\|}{~:]#'


def index(request):
    if request.method=="POST":
        username=request.POST.get("usernameinput")
        password=request.POST.get("passwordinput")
        h = hashlib.new('sha512')
        password = password.encode('utf-8')
        h.update(password)
        enpassword=h.hexdigest()
        a=col.find({"username":username,"password":enpassword})
        data=""
     
        for x in a:

            data=x
        
        if len(data)!=0:
            
            return redirect("http://127.0.0.1:8000/analysis")
        
        else:
        
            messages.error(request,"Incorrect Username or Password")
    
    return render(request,'index.html')
def signup(request):
    if request.method=="POST":
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        username=request.POST.get("username")
        password=request.POST.get("password")
        confirmpassword=request.POST.get("confirmpassword")
        mailbox=request.POST.get("mailbox")
        mailbox=mailbox.lower()
        ans=col.find({"username":username}).count()>0
        if ans==True:
        
            messages.error(request,"Username already taken")
        elif firstname.isalpha()==False:
            messages.error(request,"Firstname should only contain alphabets")
        elif lastname.isalpha()==False:
            messages.error(request,"Lastname should only contain alphabets")
        elif '@' not in mailbox:
            messages.error(request,"Invalid Email")
        elif any(x.isalpha() for x in password)==False or any(x.isnumeric() for x in password)==False or any(x in special_char for x in password) == False:
            messages.error(request,"Password should be alphanumeric")
        elif password==username:
            messages.error(request,"Username and Password cannot be same")
        elif confirmpassword!=password:
            messages.error(request,"Confirmpassword and Password should match")
        else:
         
            h = hashlib.new('sha512')
            password = password.encode('utf-8')
            h.update(password)
            enpassword=h.hexdigest()
            confirmpassword=enpassword
            mysignup=SignUp(firstname=firstname,lastname=lastname,username=username,password=enpassword,mailbox=mailbox)
            mysignup.save() 
            return redirect('http://127.0.0.1:8000/')
    return render(request,'signup.html')

def reset(request):
    if request.method=="POST":
        resetusername=request.POST.get("resetusername")
        resetpassword=request.POST.get("resetpassword")
        resetconfirmpassword=request.POST.get("resetconfirmpassword")
        resetotp=int(request.POST.get("resetotp"))
        ans=col.find({"username":resetusername}).count()>0
        print(number)
        print(resetotp)
        if ans==False:
        
            messages.error(request,"Username does not exist")
        elif any(x.isalpha() for x in resetpassword)==False or any(x.isnumeric() for x in resetpassword)==False or any(x in special_char for x in resetpassword) == False:
            messages.error(request,"Password should be alphanumeric")
        elif resetotp!=number:
            messages.error(request,"Wrong OTP")
        elif resetpassword==resetusername:
            messages.error(request,"Username and Password cannot be same")
        elif resetconfirmpassword!=resetpassword:
            messages.error(request,"Confirmpassword and Password should match")
        else:
            a=col.find_one({"username":resetusername})
            oldpassword=a["password"]
            h = hashlib.new('sha512')
            password = resetpassword.encode('utf-8')
            h.update(password)
            enpassword=h.hexdigest()
            myquery={"password":oldpassword}
            newvalue={"$set":{"password":enpassword}}
            col.update_one(myquery,newvalue)
            return redirect('http://127.0.0.1:8000/')
    return render(request,"reset.html")

def forgotpassword(request):
    
    if request.method=="POST":
            forgotemailinput=request.POST.get("forgotemailinput")
            forgotusernameinput=request.POST.get("forgotusernameinput")
            a=col.find({"username":forgotusernameinput,"mailbox":forgotemailinput})
            data=''
        
            for x in a:
                data=x 
            if len(data)!=0:
                sender_email = "maxsidalmran@gmail.com"
                receiver_email = str(forgotemailinput)
                subject = "One Time Password"
                message = "Your OTP is "+str(number) 
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                smtp_server = "smtp.gmail.com"
                port = 587  
                username = "maxsidalmran@gmail.com"
                password = "vwqpogkkupvajcqu"
                try:
                        server = smtplib.SMTP(smtp_server, port)
                        server.starttls()  
                        server.login(username, password)
                        text = msg.as_string()
                        server.sendmail(sender_email, receiver_email, text)
                        return redirect("http://127.0.0.1:8000/reset")
                    
                except Exception as e:
                        messages.error(request,"Error")
                finally:
                        server.quit()
            
                
            else:
                messages.error(request,"Incorrect Details")
    return render(request,'forgotpassword.html')





def graphs(request):

    
 
    return render(request,"graphs.html")


def analysis(request):
   
  
    if request.method == "POST":
        countryinput = request.POST.get("countryinput")
        weightinput = float(request.POST.get("weightinput"))  
        shipmentmodeinput = request.POST.get("shipmentmodeinput")
        shipmentmodeinput=shipmentmodeinput.lower()
        countryinput=countryinput.lower()
        modes = ['air', 'ocean','air charter',
                 'truck']
        countrylist=['vietnam', 'haiti', 'mozambique', 'south africa', 'rwanda',
       'malawi', "côte d'ivoire", 'uganda', 'zimbabwe', 'congo, drc',
       'tanzania', 'zambia', 'benin', 'ethiopia', 'nigeria', 'guyana',
       'cameroon', 'namibia', 'ghana', 'togo', 'angola', 'afghanistan',
       'dominican republic', 'guatemala', 'swaziland', 'south sudan',
       'botswana']
        countryinput=countryinput.lower()
        if shipmentmodeinput not in modes:
            messages.error(request, "Shipment mode can only be air,ocean, air charter or truck")
        if countryinput not in countrylist:
            messages.error(request,"Invalid Country Name")
        else:
            country_dict={'Country_afghanistan':False,
                'Country_angola':False, 'Country_benin':False, 'Country_botswana':False,
                'Country_cameroon':False, 'Country_congo, drc':False, "Country_côte d'ivoire":False,
                'Country_dominican republic':False, 'Country_ethiopia':False, 'Country_ghana':False,
                'Country_guatemala':False, 'Country_guyana':False, 'Country_haiti':False,
                'Country_malawi':False, 'Country_mozambique':False, 'Country_namibia':False,
                'Country_nigeria':False, 'Country_rwanda':False, 'Country_south africa':False,
                'Country_south sudan':False, 'Country_swaziland':False, 'Country_tanzania':False,
                'Country_togo':False, 'Country_uganda':False, 'Country_vietnam':False, 'Country_zambia':False,
                'Country_zimbabwe':False}
            shipmentmode_dict={'Shipment Mode_air':False, 'Shipment Mode_air charter':False,
              'Shipment Mode_ocean':False, 'Shipment Mode_truck':False}
           
            for x in countrylist:
                if x==countryinput:
                    dictvalue="Country_"+str(x)
            country_dict[dictvalue]=True 
            
            
            if shipmentmodeinput=="air":
                shipmentmode_dict["Shipment Mode_air"]=True 
            elif shipmentmodeinput=="air charter":
                shipmentmode_dict['Shipment Mode_air charter']=True 
            elif shipmentmodeinput=="truck":
                shipmentmode_dict['Shipment Mode_truck']=True 
            else:
                shipmentmode_dict["Shipment Mode_ocean"]=True 
            
            model_path = "D:\Maxwell Project\Project\latestmodel.pkl"
            model = joblib.load(model_path)
            min_freight_original=30.0
            max_freight_original=146850.66
            min_weight=1
            max_weight=154780
            scaled_weight=(weightinput-min_weight)/(max_weight-min_weight)
            
            
            """'vietnam', 'haiti', 'mozambique', 'south africa', 'rwanda',
       'malawi', "côte d'ivoire", 'uganda', 'zimbabwe', 'congo, drc',
       'tanzania', 'zambia', 'benin', 'ethiopia', 'nigeria', 'guyana',
       'cameroon', 'namibia', 'ghana', 'togo', 'angola', 'afghanistan',
       'dominican republic', 'guatemala', 'swaziland', 'south sudan',
       'botswana'"""
         
            features_2d = np.array([[round(scaled_weight,6),country_dict['Country_afghanistan'],country_dict['Country_angola'],
                                     country_dict['Country_benin'],country_dict['Country_botswana'],country_dict['Country_cameroon'],
                                     country_dict['Country_congo, drc'],country_dict["Country_côte d'ivoire"],
                                     country_dict['Country_dominican republic'],country_dict['Country_ethiopia'],country_dict['Country_ghana'],
                                     country_dict['Country_guatemala'],country_dict['Country_guyana'],country_dict['Country_haiti'],country_dict['Country_malawi'],
                                     country_dict['Country_mozambique'],country_dict['Country_namibia'],country_dict['Country_nigeria'],
                                     country_dict['Country_rwanda'],country_dict['Country_south africa'],country_dict['Country_south sudan'],
                                     country_dict['Country_swaziland'],country_dict['Country_tanzania'],country_dict['Country_togo'],country_dict['Country_uganda'],
                                     country_dict['Country_vietnam'],country_dict['Country_zambia'],country_dict['Country_zimbabwe'],
                                     shipmentmode_dict['Shipment Mode_air'],shipmentmode_dict['Shipment Mode_air charter'],shipmentmode_dict['Shipment Mode_ocean'],
                                     shipmentmode_dict['Shipment Mode_truck']]])
            predictions = model.predict(features_2d)
          
            finalanswer = predictions[0] * (max_freight_original - min_freight_original) + min_freight_original
            finalanswer=str(round(finalanswer,2))
            finalanswer=finalanswer+" $"
            messages.success(request,finalanswer)
          


    return render(request,'analysis.html')  

