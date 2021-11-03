from dns.rdatatype import NULL
import numpy as np
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from flask import Flask, flash, request, redirect, url_for, current_app,send_from_directory
from werkzeug.utils import secure_filename
from datetime import  datetime
from flask import Flask, render_template, flash, url_for, session, request
from functools import wraps
import pandas as pd

from flask_apscheduler import APScheduler


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return decorated_function
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["yetki"]==1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("raporlar"))

    return decorated_function

try:
    mydb = mysql.connector.connect(
        host="hypegenai.com",
        user="hypegena",
        password="aZ5xjXf133",
        database="hypegena_sprbkn"
    )
    mycursor = mydb.cursor(buffered=True)
    mycursor2 = mydb.cursor(buffered=True)
    mycursor3 = mydb.cursor(buffered=True)
except Exception as e:
    pass
app = Flask(__name__)
scheduler = APScheduler() 
with app.app_context():
    # within this block, current_app points to app.
    print(current_app.name)
app.secret_key = 'super secret key'
adi_soyadi = " "
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
tc_kimlik_no = " "
database_url = ""
kayit_tarihi = datetime.now()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000





file = []


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():

    twitter_kullanici_adi = session["username"]

    try:

        mycursor.execute(
            "select*from users WHERE name_surname = '"+str(twitter_kullanici_adi)+"' ")
        myresult = mycursor.fetchall()
        for i in myresult:
            twitter_kullanici_adi = i[3]
            name_surname = i[4]
    except:
        pass

    # username=request.form.get("twitter_user_one") # veritabani sorguları olacak cache'den gelecek giriş yapılan kullanici
    # user_pass=request.form.get("pass")# veritabani sorguları olacak cache'den gelecek giriş yapılan kullanici
    # mail=request.form.get("mail")
    if request.method == 'POST':
        mail = session["username"]

        old_pass = request.form.get("password_current")
        mycursor.execute("select*from users where mail='" +
                         str(mail)+"' and pass='"+str(old_pass)+"'")
        myresult = mycursor.fetchall()
        if myresult:
            newpass1 = request.form.get("password")
            newpass2 = request.form.get("password_confirmation")
            if newpass1 == newpass2:
                mycursor2.execute("update users SET pass='" +
                                  newpass1+"' where mail='"+mail+"'")
                mydb.commit()
            else:
                pass

    new_name = request.form.get("name")
    mail = request.form.get("email")

    if request.method == 'POST':
        if request.form.get("button") == "value":

            try:
                sql = "UPDATE users SET mail = '" + \
                    str(mail)+"' WHERE name_surname = '" + \
                    str(twitter_kullanici_adi)+"' "

                mycursor.execute(sql)
                session["username"] = mail
                twitter_kullanici_adi = session["username"]
                mydb.commit()

            except Exception as e:
                pass
    return render_template("profile.html", mail=mail, twitter_kullanici_adi=twitter_kullanici_adi)


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route("/", methods=['GET', 'POST'])
@login_required
def raporlar():
    hatırlatici_mesaj = []
    hatırlatici_date = []
    hatırlatici_id = []
    # global id_list,isim_soyisim_list,tc_list,plaka_list,giris_list,cikis_list,yemek_durum_list,resepsiyon_not_list,oda_numarasi_list,date1,date2
    try:
        sql = "SELECT *FROM reminder"
        mycursor.execute(sql)
       
        for i in mycursor:
            hatırlatici_id.append(i[0])
            hatırlatici_mesaj.append(i[1])
            hatırlatici_date.append(i[2])
    except Exception as e:
        print(e)
    if request.method == 'POST':
        if request.form.get("button") == "value":
            
                date1 = request.form.get("date1")
                date2 = request.form.get("date2")
        if request.form.get("button") == "gonder":
                mesaj=request.form.get("mesaj")
                ekleme_date=request.form.get("date1_ekle")
                saat_start=request.form.get("saat_start")
                
                ekleme_date=ekleme_date+" "+saat_start
                print(mesaj)
                print(ekleme_date)
                print(saat_start)
              

                try:  
                    sql = "INSERT INTO reminder (text,date) VALUES (%s,%s)"
                    val = (mesaj,ekleme_date)
                    mycursor.executemany(sql, (val,))
                    mydb.commit()
                    print("bastik")
                  
                except Exception as e:
                    print(e)
                hatırlatici_id.clear()
                hatırlatici_mesaj.clear()
                hatırlatici_date.clear()
                try:
                   
                    sql = "SELECT *FROM reminder"
                    mycursor.execute(sql)
                
                    for i in mycursor:
                        hatırlatici_id.append(i[0])
                        hatırlatici_mesaj.append(i[1])
                        hatırlatici_date.append(i[2])
                except Exception as e:
                    print(e)
    
    return render_template("raporlar.html",hatırlatici_id=hatırlatici_id,hatırlatici_date=hatırlatici_date,hatırlatici_mesaj=hatırlatici_mesaj)


def scheduleTask():
    dataframe_array=[]
    # global id_list,isim_soyisim_list,tc_list,plaka_list,giris_list,cikis_list,yemek_durum_list,resepsiyon_not_list,oda_numarasi_list,date1,date2
    try:
        sql = "SELECT *FROM reminder"
        mycursor.execute(sql)
       
        for i in mycursor:
           dataframe_array.append([i[1],i[2]])
    except Exception as e:
        print(e)
    dataframe = pd.DataFrame(dataframe_array, columns=['Text','Date'])
    print(dataframe)
    result_mail=""
    now_time=datetime.now()
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
           

        

@app.route("/forms", methods=['GET', 'POST'])
@login_required
def forms():
    twitter_kullanici_adi = session["username"]
    result_mail = ""
    if request.method == 'POST':

        if request.form.get("button") == "value":
            name_suname = request.form.get("isim_soyisim")
            telefon = request.form.get("telefon")
            konu = request.form.get("konu")
            baslik = request.form.get("baslik")
            mesaj = request.form.get("mesaj")
            to = ['yildizemre2@hotmail.com', 'yildizemre2@gmail.com']
            subject = baslik
            body = name_suname+"n"+telefon+" "+konu+"\n"+mesaj

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
    return render_template("forms.html", result_mail=result_mail, twitter_kullanici_adi=twitter_kullanici_adi)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("pass")
        mycursor.execute("select*from users where mail='" +
                         email+"' and password='"+password+"'")
        myresult = mycursor.fetchall()
        if myresult:
            for i in myresult:
                print(i)
                session["username"]=i[1]
                session["yetki"]=i[5]
            session["logged_in"] = True

            return redirect(url_for("raporlar"))

        else:

            return render_template("login.html")

    return render_template("login.html")






@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))


@app.route("/delete/<id>")
def delete(id):
    try:
        mycursor.execute("delete from reminder where id ="+id+" ")
        mydb.commit()

    except Exception as e:
        pass

    return redirect(url_for("raporlar"))


if __name__ == "__main__":
    scheduler.add_job(id = 'Scheduled Task', func=scheduleTask, trigger="interval", minutes=1)
    scheduler.start()
    app.run(debug=True)
