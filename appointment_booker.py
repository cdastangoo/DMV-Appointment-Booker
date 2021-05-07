import sys
import subprocess
import calendar
import selenium_utils as utils

try:
    from selenium import webdriver
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'selenium'])
finally:
    from selenium import webdriver

try:
    from keyboard import press_and_release, write
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'keyboard'])
finally:
    from keyboard import press_and_release, write


# optional parameters: change these constants if desired

# browser to use (make sure it matches the webdriver you installed)
BROWSER = 'Firefox'

# file path for user/appointment data
FILE_PATH = 'data.txt'

# check the first appointment only, then jump to the next location (recommended only when appointments are very sparse)
FIRST_ONLY = True

# choose latest possible valid appointment time on a given date (recommended to avoid early appointments if possible)
LATEST_TIME = False

# save pdf confirmation after appointment is booked
SAVE_AS_PDF = False


# dummy user data
FIRST_NAME = 'Tommy'
LAST_NAME = 'Tutone'
PHONE_NUMBER = '8088675309'

# dummy current appointment data
CURRENT_MONTH = 'December'
CURRENT_DATE = '31'
CURRENT_TIME = '2:30 PM'
CURRENT_YEAR = '2025'


# setup selenium webdriver based on selected browser
if BROWSER == 'Firefox':
    driver = webdriver.Firefox()
elif BROWSER == 'Chrome':
    driver = webdriver.Chrome()
elif BROWSER == 'Edge':
    driver = webdriver.Edge()
elif BROWSER == 'Safari':
    driver = webdriver.Safari()
else:
    print("Invalid browser for selenium webdriver, using default")
    if sys.platform == 'win32':
        driver = webdriver.Edge()
    elif sys.platform == 'darwin':
        driver = webdriver.Safari()
    else:
        driver = webdriver.Firefox()


# helper methods


def convert_month_int(month_str):
    """returns month in int form given its name in string form"""
    return list(calendar.month_name).index(month_str)


def month_is_valid(month, year):
    """returns true if selected month is same of before current appointment month"""
    return convert_month_int(month) <= convert_month_int(CURRENT_MONTH) or int(year) < int(CURRENT_YEAR)


def date_is_valid(date):
    """returns true if selected date is before current appointment date"""
    return int(date) < int(CURRENT_DATE)


def convert_time_int(time_str):
    """returns time in int form given string in hh:mm tt form"""
    time_int = int(time_str[:-3].replace(':', ''))
    if time_str[0:2] == '12':
        return time_int if 'PM' in time_str else time_int - 1200
    return time_int if 'AM' in time_str else time_int + 1200


def time_is_valid(time):
    """returns true if selected time is earlier than current appointment and before 2:45 PM"""
    time_int = convert_time_int(time)
    return time_int < 1445 and time_int < convert_time_int(CURRENT_TIME)


def appointment_is_valid(date, time, month, year):
    """returns true if selected appointment occurs before current appointment"""
    return month_is_valid(month, year) and date_is_valid(date) and time_is_valid(time)


# functional methods


def load_data():
    """reads data file and returns user data and current appointment data"""
    try:
        file = open(FILE_PATH, 'r')
        data = file.readlines()
        file.close()
        return data
    except (FileNotFoundError, IOError):
        print("Invalid file path, using dummy params.")
        return None


def save_data(data):
    """writes to data file to save appointment data"""
    file = open(FILE_PATH, 'w')
    for line in data:
        file.write(line + "\n")
    file.close()


def init():
    """load user/appointment data and initialize appointment selection"""
    global FIRST_NAME, LAST_NAME, PHONE_NUMBER, CURRENT_MONTH, CURRENT_DATE, CURRENT_YEAR, CURRENT_TIME
    data = load_data()
    if data is not None:
        FIRST_NAME = data[0].rstrip()
        LAST_NAME = data[1].rstrip()
        PHONE_NUMBER = data[2].rstrip()
        if len(data) >= 7:
            CURRENT_MONTH = data[3].rstrip()
            CURRENT_DATE = data[4].rstrip()
            CURRENT_YEAR = data[5].rstrip()
            CURRENT_TIME = data[6].rstrip()
    # navigate to location selection screen
    driver.get("https://alohaq.honolulu.gov")
    driver.find_element_by_xpath("//div[@class='button-look location-category-button'][@data-category_id='1']").click()
    driver.find_element_by_id('newAppointment').click()


def select_location(location):
    """select location and click buttons to get to time selection"""
    location_id = 'location_3' if location == "koolau" else 'location_1'
    utils.wait_page_load_by_id(driver, 10, location_id).click()
    driver.find_element_by_id('transaction_7').click()
    driver.find_element_by_id('requiredDoc').click()


def start_over():
    """navigate back to location selection page"""
    for i in range(2):
        driver.find_element_by_class_name('back').click()


def check_appointments():
    """loop through valid dates and times and check if valid"""
    utils.wait_page_load_by_id(driver, 20, 'time_0')
    year = driver.find_element_by_class_name('ui-datepicker-year').text
    month = driver.find_element_by_class_name('ui-datepicker-month').text
    date = driver.find_element_by_class_name('ui-state-active').text
    time = driver.find_element_by_id('time_0')
    # if only checking first appointment, break out if it isn't valid
    if FIRST_ONLY:
        if appointment_is_valid(date, time.text, month, year):
            select_appointment(time)
        else:
            start_over()
            return
    # loop through appointments
    while month_is_valid(month, year):
        if not utils.check_exists_by_class_name(driver, 'ui-state-default'):
            continue
        # loop through dates
        for day in driver.find_elements_by_xpath("//a[@class='ui-state-default']"):
            if date_is_valid(day.text):
                time = utils.wait_page_load_by_id(driver, 5, 'time_0')
                # select first time available
                if not LATEST_TIME:
                    if time_is_valid(time.text):
                        select_appointment(time)
                # select latest valid time
                else:
                    idx = 1
                    while utils.check_exists_by_id(driver, 'time_' + str(idx)):
                        time = driver.find_element_by_id('time_' + str(idx))
                        if time_is_valid(time.text):
                            select_appointment(time)
                        idx += 1
            else:
                break
        # check next month
        driver.find_element_by_class_name('ui-datepicker-next').click()
        month = driver.find_element_by_xpath("//span[@class='ui-datepicker-month']").text
    start_over()


def select_appointment(time_element):
    """select valid time and book appointment"""
    time_element.click()
    first_name = driver.find_element_by_id('fname')
    last_name = driver.find_element_by_id('lname')
    phone_number = driver.find_element_by_id('number')
    first_name.send_keys(FIRST_NAME)
    last_name.send_keys(LAST_NAME)
    phone_number.send_keys(PHONE_NUMBER)
    driver.find_element_by_class_name('submit').click()
    # cancel existing appointment if one exists
    # if "Existing Appointments" in driver.find_element_by_id('headerSub').text:
    utils.wait_element_clickable_by_id(driver, 10, 'appointment_duplicates_cancel').click()
    press_and_release('enter')
    # open confirmation screen and save appointment data
    utils.wait_page_load_by_id(driver, 15, 'appointmentSuccess')
    utils.wait_element_clickable_by_class_name(driver, 15, 'print')
    confirmation_date = driver.find_element_by_id('info_date').text
    confirmation_time = driver.find_element_by_id('info_time').text
    confirmation_code = driver.find_element_by_id('info_confirmation').text
    location = driver.find_element_by_id('info_loc').text
    save_month = confirmation_date[6:-8].replace(' ', '')
    save_date = confirmation_date[-8:-6]
    save_year = confirmation_date[-4:]
    save_time = confirmation_time[16:-4]
    save_code = confirmation_code[19:]
    save_location = "Kapalama" if "Kap" in location else "Koolau"
    data = [FIRST_NAME, LAST_NAME, PHONE_NUMBER, save_month, save_date, save_year, save_time, save_code, save_location]
    save_data(data)
    # save pdf confirmation
    if SAVE_AS_PDF:
        save_pdf(save_month, save_date, save_time)
    exit(0)


def save_pdf(month, date, time):
    """save pdf confirmation of appointment"""
    current_tab = driver.current_window_handle
    driver.find_element_by_id('showDLapplication').click()
    driver.switch_to.window(current_tab)
    utils.wait_element_clickable_by_class_name(driver, 10, 'print').click()
    press_and_release('s')
    for i in range(5):
        press_and_release('tab')
    press_and_release('enter')
    pdf_title = "AlohaQ Confirmation %s %s, %s" % (month[0:3], date, time[:-3])
    write(pdf_title)
    press_and_release('enter')


# main loop
locations = ["kapalama", "koolau"]
init()
while True:
    for dmv in locations:
        select_location(dmv)
        check_appointments()
