from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import LoadingAnimation



def getMail(stop_event):
    options = Options()
    options.add_argument('--headless')
    print('Wait for prompt...Downloading webdriver...')
    t = LoadingAnimation.start_animation(stop_event)
    options.add_argument('--no-sandbox')
    options.add_argument('--diable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('http://newep.lge.com/portal/main/portalMain.do')
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="USER"]'))
    )
    LoadingAnimation.end_animation(t, stop_event)
    username = input('EP ID: ')
    username_field.send_keys(username)
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="LDAPPASSWORD"]'))
    )
    password_field.send_keys('')
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBiobtn"]'))
    )
    login_button.click()
    print('Waiting for bio auth and loading...')
    t = LoadingAnimation.start_animation(stop_event)
    WebDriverWait(driver, 60).until(EC.url_contains('http://newep.lge.com/portal/main/portalMain.do'))
    driver.get('http://lgekrhqms28.lge.com/mail6/312996.nsf/M30FirstFrame?ReadForm')
    LoadingAnimation.end_animation(t, stop_event)
    print('Fetching mail list...This could take some time...')
    t = LoadingAnimation.start_animation(stop_event)
    driver.switch_to.frame('Main')
    gunte_button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[title="근태"]'))
    )
    WebDriverWait(driver, 60).until(
        EC.invisibility_of_element_located((By.XPATH, '/html/body/div[5]/div[1]'))
    )
    gunte_button.click()
    html = driver.page_source
    while '[근태]' not in html:
        time.sleep(1)
        html = driver.page_source
    driver.quit()
    LoadingAnimation.end_animation(t, stop_event)
    return html