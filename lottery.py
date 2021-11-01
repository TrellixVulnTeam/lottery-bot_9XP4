# Participate in lottery

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import json

from time import sleep
from datetime import datetime
import csv

class trackerBot(): 

    # initializing chromewebdriver
    def __init__(self):
        
        chrome_options = Options()

        # enable if you want to run app in a background
        # chrome_options.add_argument("--headless")

        ## prevents website from chekcing if you are a bot

        # assign fake user agent
        chrome_options.add_argument(f'user-agent={"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}')
        
        # disables website from checking if you are using automation in controls
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # if website is disabled automation in js
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # prevents js from adding any automation flags itself
        chrome_options.add_experimental_option('useAutomationExtension', False)

        WINDOW_SIZE = "1920,1080"
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        
        self.driver = webdriver.Chrome(options=chrome_options)

        # disables website from checking if you are usin automation in navigation
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.driver.implicitly_wait(10) # seconds


    #  loads web page
    def load_website(self, uri):

        self.driver.get(uri)

    # accept cookies once website is loaded
    def accept_cookies(self):

        accept_btn = self.driver.find_element_by_xpath('//*[@id="kc-acceptAndHide"]')
        accept_btn.click()

    # execute task to participate in lottery
    def do_some_task(self):

        # air pods
        task_btn = self.driver.find_element_by_xpath('//*[@id="competition-form-container"]/form/div[1]/ul/li[3]/div[1]/div')
        task_btn.click()

        # suklaata jouluksi
        # task_field = self.driver.find_element_by_xpath('//*[@id="free-text"]')
        # task_field.send_keys('Koko suvulle jakoon, koska ovat tulossa viettämään joulua tänä vuonna meille!')


    # enter contact info
    def enter_conatct_info(self, contact_info):

        input_firstname = self.driver.find_element_by_xpath('//*[@id="firstName"]')
        input_firstname.send_keys(contact_info['first_name'])

        input_lastname = self.driver.find_element_by_xpath('//*[@id="lastName"]')
        input_lastname.send_keys(contact_info['last_name'])

        input_address = self.driver.find_element_by_xpath('//*[@id="streetAddress"]')
        input_address.send_keys(contact_info['address'])

        input_postalcode = self.driver.find_element_by_xpath('//*[@id="zipCode"]')
        input_postalcode.send_keys(contact_info['postal_code'])

        input_city = self.driver.find_element_by_xpath('//*[@id="city"]')
        input_city.send_keys(contact_info['city'])

        input_email = self.driver.find_element_by_xpath('//*[@id="email"]')
        input_email.send_keys(contact_info['email'])

        input_phone= self.driver.find_element_by_xpath('//*[@id="phoneNumber"]')
        input_phone.send_keys(contact_info['phone_number'])

    # submit and participate in lottery
    def submit(self):
        
        submit_btn = self.driver.find_element_by_xpath('//*[@id="competition-form-submit"]')
        submit_btn.click()

        sleep(3)

    def check_result(self):
            
            success_check = self.driver.find_element_by_xpath('//*[@id="competition-form-container"]/div/div')
            success_check = success_check.get_attribute('class')

            # if participation failed the value would be 'submit-error'
            if(str(success_check) == 'submit-success'):
                return(1)
            else:
                return(0)

# functions execution order
def bot(uri):

    # get contact info from config file
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
        # print(data)

        # contact info
        contact_info = {
            'first_name'    : data['contact']['first_name'],
            'last_name'     : data['contact']['last_name'],
            'email'         : data['contact']['email'],
            'address'       : data['contact']['address'],
            'postal_code'   : data['contact']['postal_code'],
            'city'          : data['contact']['city'],
            'phone_number'  : data['contact']['phone_number']
        }

    # creates new 'bot' by touching bot class
    bot = trackerBot()

    # catch basic selenium Exceptions regarding finding elements etc...
    try:
        # execute bot actions
        bot.load_website(uri)
        bot.accept_cookies()
        bot.do_some_task()
        bot.enter_conatct_info(contact_info)
        bot.submit()

        automation_bypass_check = bot.check_result()
        
        # catch if website identifies this session as automation
        if (automation_bypass_check == 1):
            return(1)
        else:
            return(0)    

    except:
        return(0)


def main():
    
    # uri for lottery
    # air pods
    uri = 'https://www.k-ruoka.fi/kilpailut/apetit-evaskippo-arvonta'
    # suklaata jouluksi 
    # uri = 'https://www.k-ruoka.fi/kilpailut/panda-vaajakoski-primus-arvonta'

    # ask user for # times to participate
    proper_value = 1
    while proper_value != 0:
        try:
            times_to_participate = int(input('\nHow many times would you like to participate in lottery?\nGive value: '))
            proper_value = 0
        except:
            print('Give proper integer value...\n')
            continue

    execution_report = []
    success_count = 0
    failed_count = 0
    
    print('\nStarting Execution...\n')

    # initialize bot as many times as user requested
    for round in range (1, (times_to_participate+1)):
        
        execution_object = []
        start_time = datetime.now()
        dt_execution_start_time = str(start_time.strftime("%d/%m/%Y %H:%M:%S"))

        status = bot(uri)
            
        # assign execution run_values
        run_round = str(round)
        dt_start_time = str(start_time.strftime("%d/%m/%Y %H:%M:%S"))
        stop_time = datetime.now()
        dt_stop_time = str(stop_time.strftime("%d/%m/%Y %H:%M:%S"))
        
        # checks if participation was succesfull
        if (status == 1):
            run_status = 'success'
            success_count = success_count + 1
        
        else:
            run_status = 'failed'
            failed_count = failed_count + 1
        
        print('Round : ' + str(round) + '   status : ' + run_status)
        
        # assign values to execution object 
        execution_object.append(run_round)
        execution_object.append(dt_start_time)
        execution_object.append(dt_stop_time)
        execution_object.append(run_status)
        execution_report.append(execution_object)


    dt_execution_stop_time = str(stop_time.strftime("%d/%m/%Y %H:%M:%S"))     
    print('\nStopping Execution...\n')

    # create execution report 

    print('\nExecution report is located on the same folder as the program\n\n')

    header = ['round', 'start_time', 'end_time', 'run_status']

    report_time = datetime.now()
    dt_report_time = str(report_time.strftime("%d-%m-%Y_%H:%M:%S"))

    with open(dt_report_time + '.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow('')
        writer.writerow(['EXECUTION OVERVIEW'])
        writer.writerow('')
        writer.writerow(['lottery the bot participated in:'])
        writer.writerow([uri])
        writer.writerow('')
        writer.writerow(['# of participations in lottery :'])
        writer.writerow([run_round])
        writer.writerow(['execution started at :'])
        writer.writerow([dt_execution_start_time])
        writer.writerow('')
        writer.writerow(['execution eneded at :'])
        writer.writerow([dt_execution_stop_time])
        writer.writerow('')
        writer.writerow(['# of success executions :'])
        writer.writerow([str(success_count)])
        writer.writerow('')
        writer.writerow(['# of failed executions :'])
        writer.writerow([str(failed_count)])
        writer.writerow('')
        writer.writerow('')
        writer.writerow(['EXECUTION DEATAILS'])
        writer.writerow('')
        writer.writerow(header)
        writer.writerows(execution_report)

main()
    
