from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_page_load_by_id(driver, timeout, elem_id):
    """wait for page to load by checking presence of element by id"""
    try:
        present = EC.presence_of_element_located((By.ID, elem_id))
        return WebDriverWait(driver, timeout).until(present)
    except TimeoutException:
        print("Timed out waiting for", elem_id)
        return None


def wait_element_clickable_by_id(driver, timeout, elem_id):
    """wait for given element to be clickable by id"""
    try:
        clickable = EC.element_to_be_clickable((By.ID, elem_id))
        return WebDriverWait(driver, timeout).until(clickable)
    except TimeoutException:
        print("Timed out waiting for", elem_id)
        return None


def wait_page_load_by_class_name(driver, timeout, class_name):
    """wait for page to load by checking presence of element by class name"""
    try:
        present = EC.presence_of_element_located((By.CLASS_NAME, class_name))
        return WebDriverWait(driver, timeout).until(present)
    except TimeoutException:
        print("Timed out waiting for", class_name)
        return None


def wait_element_clickable_by_class_name(driver, timeout, class_name):
    """wait for given element to be clickable by id"""
    try:
        clickable = EC.element_to_be_clickable((By.CLASS_NAME, class_name))
        return WebDriverWait(driver, timeout).until(clickable)
    except TimeoutException:
        print("Timed out waiting for", class_name)
        return None


def wait_page_load_by_xpath(driver, timeout, xpath):
    """wait for page to load by checking presence of element by xpath"""
    try:
        present = EC.presence_of_element_located((By.XPATH, xpath))
        return WebDriverWait(driver, timeout).until(present)
    except TimeoutException:
        print("Timed out waiting for", xpath)
        return None


def wait_element_clickable_by_xpath(driver, timeout, xpath):
    """wait for given element to be clickable by id"""
    try:
        clickable = EC.element_to_be_clickable((By.XPATH, xpath))
        return WebDriverWait(driver, timeout).until(clickable)
    except TimeoutException:
        print("Timed out waiting for", xpath)
        return None


def check_exists_by_id(driver, elem_id):
    """returns true if element exists given id"""
    try:
        driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_class_name(driver, class_name):
    """returns true if element exists given class name"""
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True


def check_exists_by_xpath(driver, xpath):
    """returns true if element exists given xpath"""
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
