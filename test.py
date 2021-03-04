import time
from selenium import webdriver
import pyautogui

url = 'https://www.baidu.com'
print(url)
driver = webdriver.Chrome()
driver.get(url)

pyautogui.hotkey('command', 's')
time.sleep(1)

filename = url.replace('https://', '')
pyautogui.typewrite(filename + '.html')
pyautogui.hotkey('enter')

