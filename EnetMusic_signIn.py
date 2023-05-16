import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

print('---程序开始执行---')
wd = webdriver.Chrome(service=Service(r'./tools/chromedriver.exe'))
wd.implicitly_wait(5)

wd.get('https://music.163.com/musician/artist/home')
# time.sleep(5)

# 选择其他登陆模式按钮
wd.switch_to.frame('g_iframe')
wd.find_element(By.XPATH, '//*[@id="login-wrapper"]/div/div[2]/div/div/div/a').click()  # 选择其他方式登录<a>tag
wd.find_element(By.XPATH, '//*[@id="j-official-terms"]').click()  # 勾选同意条款checkbox
wd.find_element(By.XPATH,
                '//*[@id="login-wrapper"]/div/div[2]/div/div/div/div[1]/div[2]/ul/li[4]/a').click()  # 选择使用邮箱登录
wd.switch_to.default_content()
# 使用邮箱登录
wd.switch_to.frame(wd.find_element(By.CSS_SELECTOR, '[id^="x-URS-iframe"]'))  # 点击选择邮箱登录后 出现的 新frame
wd.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/input').send_keys('你的邮箱')
wd.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div[2]/input[2]').send_keys('你的密码')
wd.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[8]/a').click()  # 点击登录按钮
wd.switch_to.default_content()
# 点登录之后，此时可能会跳转到新页面，也可能不跳转(网易BUG)
while True:
    try:
        print('Info:正在监视转圈圈消失...')
        tmp = wd.find_element(By.CSS_SELECTOR, '[id^="x-URS-iframe"]')  # 判断是否存在，若不存在，find_element方法会抛异常
    except Exception:
        print('Info:转圈圈已经消失，即将刷新页面...')
        wd.refresh()
        break
    else:
        time.sleep(1)

try:
    wd.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]').click()
except Exception:
    print('异常:登录之后，没有弹窗，未找到[跳过]按钮(可能官网已经更新)')

try:
    tmpBtn = wd.find_element(By.XPATH, '//*[@id="ct-musician-sidebar"]/div[2]/div[1]')
    if 'signed' in tmpBtn.get_attribute('class'):
        print('Info:今日已签到，无需再签到')
    else:
        tmpBtn.click()
        print('Info:签到成功，已领取1云豆')
except Exception:
    print('异常:[签到领1云豆]按钮不存在,或其他异常')

# input01 = wd.find_element(By.XPATH, '//*[@id="auto-id-1683979527725"]')
# wd.refresh()
# print(input02.get_attribute('outerHTML'))
# print(input01.get_attribute('outerHTML'))

# 打印结果
# for element in elements:
#     print('----------------')
#     print(element.get_attribute('outerHTML'))
print('Info:即将关闭Chrome浏览器(3秒后)')
time.sleep(3)
wd.quit()
print('Info:浏览器已关闭')

print('---执行完毕，等待手动退出程序---')
input()
