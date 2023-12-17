from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from cookie import CookieLogin

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
driver.maximize_window()
driver.implicitly_wait(5)


url = "https://weibo.com/"
driver.get(url=url)

sleep(20)

cookies = driver.get_cookies()

cookie_fname = './cookie.json'
login = CookieLogin(cookie_fname)

login.save_cookies(cookies)


driver.close()
driver.quit()