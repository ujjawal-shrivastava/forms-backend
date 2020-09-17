from celery import shared_task
from decouple import config



@shared_task
def send_register_email(email,password,name):
    import smtplib

    msg_body = '''
Hello {name},

You are successfully registered at DeForm. Your login details are as follows:

Email: {email}
Password: {password}
Login URL: http://192.168.43.159:3000/login/

Start creating and distributing some awesome Forms!

Regards,
DeForm
'''

    sender = {
        "name":f"{config('EMAIL_NAME')}",
        "email":f"{config('EMAIL_USERNAME')}",
        "password":f"{config('EMAIL_PASSWORD')}"
    }

    subject=f"Welcome {name} | Thanks for registering at DeForm!"
    recepient = {"name":name, "email":email, "password":password}
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender["email"],sender["password"]) 
    msg_sub = f'''From: {sender["name"]} <{sender["email"]}>
To: {recepient["name"]} <{recepient["email"]}>
Reply-to: {sender["email"]}
Subject: {subject}'''
    message =  msg_sub+ msg_body.format(**recepient)
    s.sendmail(sender["email"], recepient["email"], message)
    return None


@shared_task
def send_forgot_password_email(email,url,name):
    import smtplib

    msg_body = '''
Hello {name},

You have requested for a password reset. Click on the link given below to confirm the request:

{url}

This link is only valid for 10 minutes.
If you didn't made this request, please ignore this e-mail.

Regards,
DeForm
'''

    sender = {
        "name":f"{config('EMAIL_NAME')}",
        "email":f"{config('EMAIL_USERNAME')}",
        "password":f"{config('EMAIL_PASSWORD')}"
    }

    subject=f"Reset Password | You have requested for password reset at DeForm!"
    recepient = {"name":name, "email":email, "url":url}
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender["email"],sender["password"]) 
    msg_sub = f'''From: {sender["name"]} <{sender["email"]}>
To: {recepient["name"]} <{recepient["email"]}>
Reply-to: {sender["email"]}
Subject: {subject}'''
    message =  msg_sub+ msg_body.format(**recepient)
    s.sendmail(sender["email"], recepient["email"], message)
    return None