from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os, time, platform
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
import webbrowser
import glob

stu_user = "your_gmail_here@gmail.com"
stu_passwd = 'gmail_pass'
TEXT = "驗證碼："
mail = MIMEMultipart('alternative')
mail['From'] = stu_user
mail['Subject'] = "LINE自動請求"
#server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#server.ehlo()
#server.login(stu_user, stu_passwd)

jquery = r'$("#_chat_room_input").text(arguments[0])'
chrome_option = Options()
# chrome_option.add_argument('--headless')
ext_path = "/Default/Extensions/ophjlpahpchlmihnnnihgmmeilfjmjjc/*"
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
#C:\Users\willchen\AppData\Local\Google\Chrome\User Data\Default\Extensions\ophjlpahpchlmihnnnihgmmeilfjmjjc
if platform.system() == 'Linux':
    ext_path = os.environ['HOME'] + "/.config/google-chrome"+ext_path if os.path.exists(os.environ['HOME']+"/.config/google-chrome") else os.environ['HOME'] + "/.config/chromium"+ext_path
else:
    ext_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data"+ext_path
ext_path = glob.glob(ext_path)
if not ext_path:
    webbrowser.get(chrome_path).open("https://chrome.google.com/webstore/detail/line/ophjlpahpchlmihnnnihgmmeilfjmjjc?hl=zh-TW")
else:
    print(ext_path[-1])
    #chrome_option.add_argument("--load-extension=" + ext_path[-1])
    #browser = Chrome(options=chrome_option)
chrome_option.add_argument('--ignore-certificate-errors')
chrome_option.add_argument('--ssl-client-certificate-file=' + 'C:\\Users\\willchen\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\ophjlpahpchlmihnnnihgmmeilfjmjjc\\3.5.1_0.pem')
idle_time = 0
chrome_option.add_extension("C:\\Users\\willchen\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\ophjlpahpchlmihnnnihgmmeilfjmjjc\\3.5.1_0.crx")

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )

chrome_option.add_argument('user-agent=%s'%user_agent)
browser = Chrome(options=chrome_option)


def choose_room(room):
    global data_local_id, input_area

    element = WebDriverWait(browser, 99).until(
        EC.presence_of_element_located((By.ID, "_search_input")))
    element.send_keys(room)
    # time.sleep(0.5)
    # time.sleep(1)
    element = WebDriverWait(browser, 99).until(
        EC.presence_of_element_located((By.XPATH, '//ul[@id="_chat_list_body"]/li[@title="%s"]' % room)))
    ActionChains(browser).move_to_element(element).click().perform()
    #element.click()

    time.sleep(0.5)
    element = WebDriverWait(browser, 99).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#_search > div > .MdBtn01Delete01")))
    element.click()
    # time.sleep(0.5)
    element = WebDriverWait(browser, 99).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.MdRGT07Cont:last-child")))
    data_local_id = element.get_attribute("data-local-id")
    # data_local_id = browser.find_element_by_css_selector("div.MdRGT07Cont:last-child").get_attribute("data-local-id")
    input_area = browser.find_element_by_id("_chat_room_input")

def check_idle(check_time=20):
    global idle_time
    if time.time()-idle_time > check_time:
        ActionChains(browser).move_to_element(input_area).send_keys(Keys.ENTER).perform()
        idle_time =time.time()

def has_new(setwho="All"):
    global data_local_id
    if setwho == "All":
        updated = WebDriverWait(browser, 99).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "MdRGT07Cont")))[-1]
        # updated = browser.find_elements_by_class_name("MdRGT07Cont")[-1]
    else:
        updated = WebDriverWait(browser, 99).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "mdRGT07"+setwho)))[-1]
        # updated = browser.find_elements_by_class_name("mdRGT07" + setwho)[-1]
    data_local_id_now = updated.get_attribute("data-local-id")
    if data_local_id != data_local_id_now:
        data_local_id = data_local_id_now
        # new_text = 0
        loop = True
        while loop:
            try:
                new_text = updated.find_element_by_class_name("mdRGT07MsgTextInner").text
                loop = False
            except StaleElementReferenceException:
                loop = True

        return new_text
    else:
        check_idle()


def read():
    return browser.find_elements_by_css_selector("div.mdRGT07Own .mdRGT07MsgTextInner")[-1].text


def send(msg):
    # data_local_id = browser.find_elements_by_css_selector("div.mdRGT07Cont").get_attribute("data-local-id")
    browser.execute_script(jquery, msg)
    loop = True
    if loop:
        try:
            input_area.send_keys(Keys.ENTER)
            loop = False
        except WebDriverException:
            input_area.click()
            loop = True



def login(username, pwd, email=None):
    if email is None:
        email = username
    browser.get("chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html"
    )
    time.sleep(5)
    element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "email")))
    element.send_keys('Python_user')
    element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "password")))
    element.send_keys('Python_pwd')


    element = WebDriverWait(browser, 99).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'loginForm-module__button_login__gnKsN')))
    element.click()
    # sent LINE login submit



if __name__ == "__main__":
    login(*args_here)
    choose_room("Alo Smo")

    timestamp = time.time()
    text = None
    while True:
        # try:
        timenow = time.time()

        if (timenow-timestamp)<=0.5:
            text = has_new()
            if text and text != str(timestamp):
                print(text)

        else:
            send(timenow)
            # print(timenow)
            timestamp = timenow
        # text = has_new()
        # if text:
        #     print(text)
