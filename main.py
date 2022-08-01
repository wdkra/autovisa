# Program: VisaHelper(non-production ready)
# It is a HALF-AUTO program. NOT full-auto! It ONLY HELPS you with the submission 
# of the visa appointment form. But you still have to submit the form by YOURSELF 
# at last. I cannot get any of your information through this program. All your
# information will be processed locally and submitted ONLY to the German Consulate 
# Shanghai(/Guangdong if you test it improperly).

# This file is an INTEGRAL part of the program VisaHelper

#     Copyright (C) 2022  Tom Zhang

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published by
#     the Free Software Foundation, AGPL-3.0-only.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

#from argparse import Action
from distutils.log import info
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import sys
import re
import imgProcess

# def ErrorDisp(errorcode):
#     str(errorcode)
#     print("The program is now terminated. The cessation has been included in the ErrorCode(local), which is: " + errorcode)
#     input('copied?y')

def chooseMode():
    print('1. Shanghai \n2. Kanton(testing purposes)')
    flag = input('1/2?')
    if flag == '1':
        url = 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=shan&realmId=96&categoryId=892&dateStr=28.08.2022'
        return url
    elif flag == '2':
        url = 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kant&realmId=1004&categoryId=2341&dateStr=27.08.2022'
        return url
    else:
        print('error')
        sys.exit(0)

# get info for console jscode
def getVisaInfo():
    with open('C:\\visacode.txt','r',encoding='utf8') as content:
        code = content.read().replace(' ','')
        info_m = re.compile(r"='(.*?)'", re.M)
        infos = []
        for info in info_m.findall(code):
            infos.append(info)
        return infos
   
# download Captcha image and send to imgProcess.py
def getCaptcha(page):
    img_style = WebDriver.find_element(By.XPATH, "//div[contains(@style,'background:white url')]").get_attribute('style')
    img_data64 = ''.join(''.join(img_style.split('"')[1:2]).split(',')[1:2])
    print(f'img_base64 data: {img_data64}')
    CaptchaCode = imgProcess.b2img(page, img_data64, 'jpg')
    print(f'main.py now got the CaptchaCode No. {page}: {CaptchaCode}')
    return CaptchaCode

def fillCaptcha(CaptchaCode, page):
    print(f'fillCaptcha() expect to fill CaptchaCode on page {page}')
    if page == '1':
        captcha_id = 'appointment_captcha_month_captchaText'
    elif page == '2':
        captcha_id = 'appointment_newAppointmentForm_captchaText'
    else:
        print("ERROR: The value 'code' for 'fillCaptcha()' cannot be other than '1' or '2'")
    captcha_input = WebDriver.find_element(By.ID, f'{captcha_id}')
    captcha_input.clear()
    print(CaptchaCode)
    captcha_input.send_keys(CaptchaCode)

def datepicker(birthDay = '2', birthMonth = '', birthYear = ''):
    WebDriver.find_element(By.XPATH, "//input[@id='fields0content']").click()
    
    # WebDriver.find_element(By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select > option[value='6']").click()
    # WebDriver.find_element(By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select > option[value='2005']").click()
    
    days = WebDriver.find_elements(By.XPATH, "//div[@id='ui-datepicker-div']/table/tbody/tr/td")
    for day in days:
        if str(day.text) == birthDay:
            break
    day.click()

WebDriver = webdriver.Chrome(service=Service('chromedriver.exe'))

#wait 3s for the appearance of the element
WebDriver.implicitly_wait(3)

# consulate kanton -> for testing
url = chooseMode()
WebDriver.get(url)

# test autoCaptcha
# Manual entry is required due to the delayed completion of the autoCaptcha(OCR).
# CaptchaCode = getCaptcha()
# captcha_input = WebDriver.find_element(By.ID, 'appointment_captcha_month_captchaText')
# captcha_input.clear()
# print(CaptchaCode)
# captcha_input.send_keys(CaptchaCode)
fillCaptcha(getCaptcha('1'), '1')
ifnext = input('y/n')
if ifnext == 'y':
    captcha_submit = WebDriver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')
    captcha_submit.click()
else:
    print('keep going anyway~')

# go to date confirmation page
gototable_1 = WebDriver.find_element(By.CSS_SELECTOR, '#content > div.wrapper > div > div > a.arrow[href]:nth-of-type(1)')
gototable_1.click()
print("c1")

# go to appointment form page
gototable_2 = WebDriver.find_element(By.CSS_SELECTOR, '#content > div.wrapper > div > div > a.arrow[href]:nth-of-type(1)')
gototable_2.click()
print("c2")

infolist = getVisaInfo()
WebDriver.execute_script(f'''
        document.getElementById('appointment_newAppointmentForm_lastname').value = '{infolist[0]}';
        document.getElementById('appointment_newAppointmentForm_firstname').value = '{infolist[1]}';
        document.getElementById('appointment_newAppointmentForm_email').value = '{infolist[2]}';
        document.getElementById('appointment_newAppointmentForm_emailrepeat').value = '{infolist[3]}';
        document.getElementById('fields0content').value = '{infolist[4]}';
        document.getElementById('appointment_newAppointmentForm_fields_1__content').value = '{infolist[5]}';
        document.getElementById('appointment_newAppointmentForm_fields_2__content').value = 'Schulbesuch / (High) School Attendance';
        document.getElementById('appointment_newAppointmentForm_fields_3__content').value = '{infolist[7]}';
        document.getElementById('appointment_newAppointmentForm_fields_4__content').checked = true;
        window.scrollTo(1,9999999999)''')

# pick the date
datepicker()
fillCaptcha(getCaptcha('2'), '2')

print("It is normal if the 'telephone number...' and 'purpose of...' are reversed.")
print("Click 'Load another picture' to check if all elements in the form are still there after refresh. Ay means success. Captcha autofill(OCR) will be completed in the short term")

input('done. press enter to close')
WebDriver.quit()