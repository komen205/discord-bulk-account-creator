from selenium import webdriver
import time
import csv
import random
import string
import threading
import requests
from concurrent.futures import ThreadPoolExecutor
from tempMail2 import TempMail
from selenium.webdriver.common.by import By

threads = []
proxylist = []
nThreads = 0
maxThreads = 5


def get_random_string(length, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))


def username_password(driver):
    username = driver.find_element_by_name('username')
    password = driver.find_element_by_name('password')
    username_password(username, password)
    username.send_keys(get_random_string(10))
    print('username is written')
    password.send_keys(get_random_string(10))
    print('password is written')


def confirm_creation(driver):

    try:
        button = driver.find_element(By.XPATH, '//label/input').click()
    except:
        pass
    button = driver.find_element(By.XPATH, '//button').click()


def email():
    tm = TempMail(api_key='')
    email = tm.get_email_address()
    print (tm.get_mailbox(email))


def password_month_year(driver):
    day = driver.find_element(
        By.XPATH, '//div[4]/div/div/div/div/div/div/div').click
    print('day is clicked')
    print('selecting day...')
    day = driver.find_element(By.XPATH, '//div[5]').click()
    print('day selected')

    month = driver.find_element(
        By.XPATH, '//div[4]/div/div[2]/div/div/div/div/div').click()
    month = driver.find_element(By.XPATH, '//div[5]').click()

    year = driver.find_element(
        By.XPATH, '//div[3]/div/div/div/div/div[2]/div').click()
    year = driver.find_element(By.XPATH, '//div[21]').click()


def create_account(driver):
    try:
        username_password(driver)
        password_month_year(driver)
        confirm_creation(driver)
        print('sleeping')
        time.sleep(40)
    except:
        print('error somewhere')


def chrome_options(proxy):
    chrome_options = webdriver.ChromeOptions()
    PROXY = proxy

    chrome_options.add_argument(f'--proxy-server={PROXY}')
    return chrome_options


def create_browser(proxy):
    path = "C:\\Users\\nunom\\Documents\\GitHub\\discord-acc-creator\\chromedriver.exe"

    driver = webdriver.Chrome(
        options=chrome_options(proxy), executable_path=path)

    driver.set_page_load_timeout(30)

    try:
        driver.get(
            'https://discord.com/register?email=test@gmail.com')
        create_account(driver)
        driver.quit()
    except:
        print('just another error')
    driver.quit()
    threadsManipulation('remove')
    print('done')


def threadsManipulation(type):
    global nThreads
    if 'add':
        nThreads += 1
    if 'remove':
        nThreads -= 1
    if 'get':
        return nThreads


def create_pool():
    return ThreadPoolExecutor(max_workers=maxThreads)


def create_thread(pool, x):
    future = pool.submit(create_browser, x)


def check_proxy():
    for x in proxylist:
        if threadsManipulation('get') < maxThreads:
            threadsManipulation('remove')
            create_thread(create_pool(), x)
        else:
            time.sleep(5)


def import_proxy():
    with open('proxy.txt', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            proxylist.append(row[0])
    check_proxy()


if __name__ == "__main__":
    email()
