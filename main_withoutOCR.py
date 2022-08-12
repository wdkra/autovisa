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
import sys
import re
import os
import time

assert os.access('c://files//visacode.txt', os.F_OK), 'file not found: visacode.txt'
assert os.access('c://files//visacode.txt', os.R_OK), 'unable to read visacode.txt (check your permission)'
assert os.path.exists('c://files//chromedriver.exe'), 'download chromedriver.exe first'

def chooseMode():
    URL_SHANGHAI_Arbeiten_Chef = 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=shan&realmId=96&categoryId=1397'
    URL_SHANGHAI_Uni = 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=shan&realmId=96&categoryId=560'
    URL_SHANGHAI_Familie = 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=shan&realmId=96&categoryId=559'
    URL_SHANGHAI_Schulbesuch = 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=shan&realmId=96&categoryId=892'
    URL_SHANGHAI_Arbeiten_ohneChef = 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=shan&realmId=96&categoryId=558'
    URL_SHANGHAI_Researcher = 'https://service2.diplo.de/rktermin/extern/choose_category.do?locationCode=shan&realmId=96&categoryId=2829'
    URL_KANTON = 'https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=kant&realmId=1004&categoryId=2341'

    print('1. Shanghai \n2. Kanton(testing purposes)')
    
    flag = input('1/2?')
    if flag == '1':
        print('''
    Shanghai:

        1. Chinese chef / cook
        2. university study /  preparation for studies
        3. family reunion / marriage / family reunion for a child
        4. language course / practical training / work (except chefs)
        5. Researcher
        6. (high-)school students / language training followed by (high) school attendance
        7. not listed
    ''')
        flag_shanghai = input('Enter the number of the visa category')
        if flag_shanghai =='1':
            return URL_SHANGHAI_Arbeiten_Chef, 'SHANGHAI'
        elif flag_shanghai == '2':
            return URL_SHANGHAI_Uni, 'SAHNGHAI'
        elif flag_shanghai == '3':
            return URL_SHANGHAI_Familie, 'SHANGHAI'
        elif flag_shanghai == '4':
            return URL_SHANGHAI_Arbeiten_ohneChef, 'SHANGHAI'
        elif flag_shanghai == '5':
            return URL_SHANGHAI_Researcher, 'SHANGHAI'
        elif flag_shanghai == '6':
            return URL_SHANGHAI_Schulbesuch, 'SHANGHAI'
        else:
            URL_SHANGHAI_OTHERS = input('url:')
            return URL_SHANGHAI_OTHERS, 'SHANGHAI'
    elif flag == '2':
        return URL_KANTON, 'KANTON'
    else:
        print("no other than '1' or '2'")
        sys.exit(0)
        
# info for console jscode
def getVisaInfo():
    with open('c://files//visacode.txt','r',encoding='utf8') as content:
        code = content.read().replace(' ','')
        info_m = re.compile(r"='(.*?)'", re.M)
        infos = []
        for info in info_m.findall(code):
            infos.append(info)
        return infos
   

options = Options()
options.page_load_strategy = 'eager'
WebDriver = webdriver.Chrome(service=Service('c://files//chromedriver.exe'),options=options)
time.sleep(2)

# wait up to 3s for elements
wait_time = input('implicitly_time (s)')
try:
    wait_time = int(wait_time)
except Exception:
    print("must be a pure number string e.g.'1','2.5'")
    sys.exit(0)
WebDriver.implicitly_wait(wait_time)

location = chooseMode()
WebDriver.get(location[0])

print('check captcha code and make sure it is 100% right \n request a new one if you are not sure')
print('Press ENTER when time is up')
input('')
time.sleep(0.5)
captcha_submit = WebDriver.find_element(By.ID, 'appointment_captcha_month_appointment_showMonth')
captcha_submit.click()

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

if location[1] == 'KANTON':
    WebDriver.execute_script('''document.getElementById('appointment_newAppointmentForm_fields_2__content').value = 'Schulbesuch / (High) School Attendance';''')
else:
    WebDriver.execute_script('''document.getElementById('appointment_newAppointmentForm_fields_2__content').options.selectedIndex = 1''')

print("In Kanton, it is normal if the 'telephone number...' and 'purpose of...' are reversed.")
print("Click 'Load another picture' to check if all elements in the form are still there after refresh. Ay means success.")

input('done. press enter to close')
WebDriver.quit()