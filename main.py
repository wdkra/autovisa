# Program: VisaHelper(non-production ready)
# It is a HALF-AUTO program. NOT full-auto! It ONLY HELPS you with the submission 
# of the visa appointment form faster. But you still have to submit the form by 
# YOURSELF at last. I cannot get any of your information through this program. 
# All information will be processed locally and submitted ONLY to the German 
# Consulate Shanghai(/Guangdong if you test it improperly).

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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests


# get the console code
def readVisaCode():
    VisaCode = open('visacode.txt','r',encoding='utf-8')
    ConsoleScript = VisaCode.read()
    VisaCode.close()
    return ConsoleScript

# not finished    
# # download Captcha image
# def getCaptcha():
#     img_style = WebDriver.find_element(By.XPATH, "//div[contains(@style,'background:white url')]").get_attribute('style')
#     img_data = ''.join(img_style.split('"')[1:2])


def datepicker(birthDay = '2', birthMonth = '', birthYear = ''):
    WebDriver.find_element(By.XPATH, "//input[@id='fields0content']").click()
    
    WebDriver.find_element(By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select > option[value='6']").click()
    WebDriver.find_element(By.CSS_SELECTOR, "#ui-datepicker-div > div > div > select > option[value='2005']").click()
    
    days = WebDriver.find_elements(By.XPATH, "//div[@id='ui-datepicker-div']/table/tbody/tr/td")
    for day in days:
        if str(day.text) == birthDay:
            break
    day.click()

WebDriver = webdriver.Chrome(service=Service('chromedriver.exe'))

#wait 3s for the appearance of the element
WebDriver.implicitly_wait(3)

# consulate kanton -> for testing
WebDriver.get('https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kant&realmId=1004&categoryId=2341&dateStr=27.08.2022')

# test autoCaptcha
# Manual entry is required due to the delayed completion of the autoCaptcha(OCR).
captcha_input = WebDriver.find_element(By.ID, 'appointment_captcha_month_captchaText')
captcha_input.clear()
captcha_input.send_keys('test input')
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

WebDriver.execute_script('''
        document.getElementById('appointment_newAppointmentForm_lastname').value = 'testFirstName';
        document.getElementById('appointment_newAppointmentForm_firstname').value = 'testLastName';
        document.getElementById('appointment_newAppointmentForm_email').value = 'no@thankyou.com';
        document.getElementById('appointment_newAppointmentForm_emailrepeat').value = 'why@repeat.com';
        document.getElementById('fields0content').value = '02.07.2005';
        document.getElementById('appointment_newAppointmentForm_fields_1__content').value = 'testPassportNumber';
        document.getElementById('appointment_newAppointmentForm_fields_2__content').value = 'Schulbesuch / (High) School Attendance';
        document.getElementById('appointment_newAppointmentForm_fields_3__content').value = '12345678910';
        document.getElementById('appointment_newAppointmentForm_fields_4__content').checked = true;
        window.scrollTo(1,9999999999)
                        ''')

# pick the date
datepicker()

print("It is normal if the 'telephone number...' and 'purpose of...' are reversed.")
print("Click 'Load another picture' to check if all elements in the form are still there after refresh. Ay means success. Captcha autofill(OCR) will be completed in the short term")

input('done. press enter to close')
WebDriver.quit()