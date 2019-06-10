# -'''- coding: utf-8 -'''-

"""
    AnonymousWatcher
    Copyright (C) 2019  Ardyn von Eizbern

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

import cv2
import pytesseract
import requests
import wx
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from twilio.rest import Client

import model
import view


def main():
    app = wx.App(False)
    frame = view.MainWindow(None)
    app.MainLoop()


def setData(emailstr):
    model.genenrateXML(emailstr)


def getData():
    return model.parseXML()

def sendWarningMail(png):
    img_data = open(png, 'rb').read()
    xMime = MIMEMultipart()
    xMimeText = MIMEText("注意！家中有人闖入！！", "plain", "utf-8")
    xMime["Subject"] = "注意"
    xMime["From"] = "防盜監視器"
    xMime["To"] = "使用者"
    xMime.attach(xMimeText)
    xMimeImage = MIMEImage(img_data, name=png)
    xMime.attach(xMimeImage)
    
    xMime = xMime.as_string()
    sendTemplateEmail(getData()["Email"], xMime)
    
    
def sendWarningSMS():
    # browser = webdriver.Chrome()
    # try:
    #     browser.get("https://globfone.com/send-text/")

    #     country = browser.find_element_by_xpath("//select[@id=countries-sms-cloned_title]" +"//option[@value='196']")
    nstring = (getData()["Cellphone"]).replace("0", "", 1)
    #     print(nstring)
    #     country.click()
    #     mnumber = browser.find_element_by_id("sms-number")
    #     mnumber.send_keys(nstring)
    #     nextx = browser.find_element_by_id("next-step")
    #     nextx.click()

    #     message = browser.find_element_by_xpath("//textarea")
    #     message.send_keys("注意！家中有人闖入！！")
    #     nexty = browser.find_element_by_id("next-step")
    #     nexty.click()
    #     vtuber = browser.find_element_by_id("captcha")
    #     vtuber.screenshot("captcha.png")
    #     img = cv2.imread("captcha.png")
    #     vkey = pytesseract.image_to_string(img)
    #     meaqua = vkey[0:5]

    #     vcode = browser.find_element_by_xpath("//input[@type='text'][@style='width:80px']")
    #     vcode.send_keys(meaqua)
    #     sendx = browser.find_element_by_name("submit")
    #     sendx.click()
    #     sleep(1)
    # finally:
    #     browser.close()

    
    # carriers = {
    #     "att": "@txt.att.net",	    
    #     "tmobile": "@tmomail.net",
	#     "verizon": "@vtext.com",
	#     "sprint": "@page.nextel.com",
    #     "cht": "",
    #     "twm": "@twmmms.catch.net.tw",
    #     "fet": "",
    #     "tstar": "",
    #     "chinamobile": "@139.com",
    #     "google": "@msg.fi.google.com"
    # }
    
    # phonenum = f"{nstring}{carriers['twm']}" 

    # sendTemplateEmail(nstring, "Attention User: Snake sneaks in home.")

    # re = requests.post("https://api.smsglobal.com/http-api.php", {
    #     "action": "sendsms",
    #     "phone": nstring,
    #     "text": "注意！家中有人闖入！！".encode("utf-8"),
    #     "key": "",
    # })
    # if(re.status_code == 200):
    #     print("簡訊發送成功")

    # re = requests.post("https://textbelt.com/text", {
    #     "phone": nstring,
    #     "message": "注意！家中有人闖入！！".encode("utf-8"),
    #     "key": "",
    # })
    # if(re.status_code == 200):
    #     print("簡訊發送成功")

    # keys = ""
    # r = requests.get("http://world.msg91.com/api/sendhttp.php?", {
    #     "authkey": keys,
    #     "mobiles": int(nstring),
    #     "message": "注意！家中有人闖入！！".encode("utf-8"),
    #     "sender": "",
    #     "route": 4,
    #     "country": 0,
    #     "unicode": 1
    # })
    # print(r)
    # if(r.status_code == 200):
    #     print("簡訊發送成功")

    # account_sid = ""
    # auth_token = ""
    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #                  body = "注意！家中有人闖入！！",
    #                  from_ = '+15109240423',
    #                  to = nstring
    #              )

    # print(message.body)
    

def sendTemplateEmail(PositionZero, Starlight):
    auth = ("", "")

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
    except:
        print("伺服器連線不成功")
    statustup1 = server.ehlo()
    statustup2 = server.starttls()

    if((statustup1[0] == 250) and (statustup2[0] == 220)):
        statustup3 = server.login(auth[0], auth[1])
    else:
        print("加密連線失敗")
    
    if(statustup3[0] == 235):   
        stautusfin = server.sendmail(auth[0], PositionZero, Starlight)
    else:
        print("登入失敗")
    
    if(not stautusfin):
        print("寄信成功")
    else:
        print("寄信失敗", stautusfin)
    
    server.quit()

if __name__ == "__main__":
    sendWarningMail(None)
