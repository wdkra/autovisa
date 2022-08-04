# coding=utf-8

# Das ist kein vollautomatsches Programm!!!
# Es kann nur dir dabei helfen(nicht fuer dich), die Formulare schneller auszufuellen.
# Du muss es SELBST einreichen.

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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from predict_onnx import Predictonnx
import sys
import re
import numpy as np
import cv2
# import imgProcess
import base64

ocr=Predictonnx('models/ocr.onnx','models/ocr.txt')


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
        print("no other than '1' or '2'")
        sys.exit(0)

# info for console jscode
def getVisaInfo():
    with open('C:\\visacode.txt','r',encoding='utf8') as content:
        code = content.read().replace(' ','')
        info_m = re.compile(r"='(.*?)'", re.M)
        infos = []
        for info in info_m.findall(code):
            infos.append(info)
        return infos
   
# get img base64 from <style>
def getCaptcha(page):
    img_style = WebDriver.find_element(By.XPATH, "//div[contains(@style,'background:white url')]").get_attribute('style')
    img_data64 = ''.join(''.join(img_style.split('"')[1:2]).split(',')[1:2])
    print(f'img_base64 data: {img_data64}')
    img = base64.b64decode(img_data64)
    img = np.frombuffer(img,np.uint8)
    img = cv2.imdecode(img,cv2.IMREAD_COLOR)
    CaptchaCode = ocr(img)[0][0]
    # CaptchaCode = imgProcess.b2img(page, img_data64, 'jpg')
    print(f'(main.py)CaptchaCode No. {page}: {CaptchaCode}')
    return CaptchaCode

def fillCaptcha(CaptchaCode, page):
    print(f'fillCaptcha() expect to fill CaptchaCode on page {page}')
    if page == '1':
        captcha_id = 'appointment_captcha_month_captchaText'
    elif page == '2':
        captcha_id = 'appointment_newAppointmentForm_captchaText'
    else:
        raise TypeError
    captcha_input = WebDriver.find_element(By.ID, f'{captcha_id}')
    captcha_input.clear()
    print(CaptchaCode)
    captcha_input.send_keys(CaptchaCode)

# def datepicker(birthDay):
#     WebDriver.find_element(By.XPATH, "//input[@id='fields0content']").click()
#     days = WebDriver.find_elements(By.XPATH, "//div[@id='ui-datepicker-div']/table/tbody/tr/td")
#     for day in days:
#         if str(day.text) == birthDay:
#             break
#     day.click()

options = Options()
options.page_load_strategy = 'eager'
WebDriver = webdriver.Chrome(service=Service('chromedriver.exe'),options=options)

# wait up to 3s for elements
WebDriver.implicitly_wait(1)

url = chooseMode()
WebDriver.get(url)

fillCaptcha(getCaptcha('1'), '1')
ifnext = input('y/n')
if ifnext == 'y':
    captcha_submit = WebDriver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')
    captcha_submit.click()
else:
    print('keep going anyway~')

def if_month_bookable():
    try:
        table1_entry = WebDriver.find_element(By.CSS_SELECTOR, '#content > div.wrapper > div > div > a.arrow[href]:nth-of-type(1)')
        return 'Available'
    except Exception:
        next_month = WebDriver.find_element(By.XPATH, "//img[@src='images/go-next.gif']")
        next_month.click()
        return 'NotAvailable'

if_bookable = if_month_bookable()
while True:
    flag = if_month_bookable()
    print(flag)
    if flag == 'Available':
        gototable_1 = WebDriver.find_element(By.CSS_SELECTOR, '#content > div.wrapper > div > div > a.arrow[href]:nth-of-type(1)')
        gototable_1.click()
        print("c1")
        break

# form
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
        document.getElementById('fields0contenthidden').value = '{infolist[5]}';
        document.getElementById('appointment_newAppointmentForm_fields_1__content').value = '{infolist[6]}';
        document.getElementById('appointment_newAppointmentForm_fields_3__content').value = '{infolist[7]}';
        document.getElementById('appointment_newAppointmentForm_fields_4__content').checked = true;
        window.scrollTo(1,9999999999)''')

if url =='https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=shan&realmId=96&categoryId=892&dateStr=28.08.2022':
    WebDriver.execute_script('''document.getElementById('appointment_newAppointmentForm_fields_2__content').options.selectedIndex = 1''')
else:
    WebDriver.execute_script('''document.getElementById('appointment_newAppointmentForm_fields_2__content').value = 'Schulbesuch / (High) School Attendance';''')

# repick the date
# datepicker(date)
fillCaptcha(getCaptcha('2'), '2')

print("It is normal if the 'telephone number...' and 'purpose of...' are reversed.")
print("Click 'Load another picture' to check if all elements in the form are still there after refresh. Ay means success. Captcha autofill(OCR) will be completed in the short term")

input('done. press enter to close')
WebDriver.quit()