from dns.rdatatype import NULL
import numpy as np
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from flask import Flask, flash, request, redirect, url_for, current_app,send_from_directory
from werkzeug.utils import secure_filename
from datetime import  date, datetime
from flask import Flask, render_template, flash, url_for, session, request
from functools import wraps
import pandas as pd
import datetime

try:
    mydb = mysql.connector.connect(
        host="hypegenai.com",
        user="hypegena",
        password="aZ5xjXf133",
        database="hypegena_sprbkn"
    )
    mycursor = mydb.cursor(buffered=True)
   
except Exception as e:
    pass

dataframe_array=[]
try:
    sql = "SELECT *FROM reminder"
    mycursor.execute(sql)
   
    for i in mycursor:
        
        dataframe_array.append([i[1],i[2]])

      
   

   
except Exception as e:
    print(e)
dataframe = pd.DataFrame(dataframe_array, columns=['Text','Date'])


now_time=datetime.datetime.now()
for i in range(len(dataframe)):
    old_time=dataframe['Date'][i]
    new_time=(old_time-now_time)
    diff_minutes = (new_time.days * 24 * 60) + (new_time.seconds/60)
    # dakika = divmod(new_time.seconds, 60) 
    # print("kalan_dakika "+str(dakika[0]))
    print(diff_minutes)
    if (int(diff_minutes))<240 and  (int(diff_minutes))>180:
       
        
        konu = "TESİS HATIRLATMA"
        baslik = "SPOR BAKANLIĞI TESİSİ"
        mesaj = dataframe['Text'][i]
        to = ['yildizemre2@hotmail.com']
        subject = baslik
        body = "\n "+konu+"\n = "+mesaj

        account = 'ali.gkky196@gmail.com'
        password = 'Ali19671570'

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.ehlo()

        server.starttls()

        server.login(account, password)
        mail = MIMEText(body, 'html', 'utf-8')
        mail['From'] = account
        mail['Subject'] = subject
        mail['To'] = ','.join(to)
        mail = mail.as_string()

        try:
            server.sendmail(account, to, mail)
            result_mail = ('Mail gönderimi başarılı')

        except:
            result_mail = ('Mail gönderimi başarısız')


    
        print(result_mail)