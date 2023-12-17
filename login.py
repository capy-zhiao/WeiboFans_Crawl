import json
import os
from time import sleep
from selenium.webdriver.common.by import By
from cookie import CookieLogin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv
from selenium.common.exceptions import NoSuchElementException

file_path = 'data.csv'
file_exists = os.path.isfile(file_path)

with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['id', 'name', 'location'])

prefs = {
    'profile.default_content_setting_values': {
        'notifications': 2
    },
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False
}

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-gpu')

service = Service(executable_path=r'D:\CODING\Chrome\chrome-win64\chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = "https://weibo.com/"
driver.get(url=url)

sleep(4)
driver.delete_all_cookies()
login = CookieLogin("cookie.json")
cookies = login.load_cookies()
try:
    for cookie in cookies:
        cookie_dict = {
            'domain': '.weibo.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        driver.add_cookie(cookie_dict)
except Exception as e:
    print(e)
sleep(2)

driver.refresh()
sleep(2)

with open('id.txt', 'a+') as id_file:
    id_file.seek(0)
    existing_ids = set(id_file.read().splitlines())
    print(existing_ids)

with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    for i in range(1, 101):
        url = f"https://weibo.com/ajax/friendships/friends?relate=fans&page={i}&uid=3178093153&type=all&newFollowerCount=0"
        driver.get(url)
        page_source = driver.page_source

        json_data = driver.find_element(By.TAG_NAME, 'pre').text
        data = json.loads(json_data)

        extracted_ids = [user["id"] for user in data["users"]]

        for extracted_id in extracted_ids:

            if str(extracted_id) in existing_ids:
                print(f"ID {extracted_id} already exists.")
                continue

            url2 = f"https://weibo.com/u/{extracted_id}"
            driver.get(url2)
            sleep(2)

            try:
                name = driver.find_element(By.CLASS_NAME, "ProfileHeader_name_1KbBs").text
                print(name)
            except NoSuchElementException:
                name = "null"
                print(name)

            try:
                location = driver.find_element(By.XPATH, "//div[contains(text(), 'IP属地')]").text
                location = location[5:]
                print(location)
            except NoSuchElementException:
                location = "null"
                print(location)

            writer.writerow([extracted_id, name, location])
            with open('id.txt', 'a') as id_file:
                id_file.write(f"{extracted_id}\n")

        sleep(2)
