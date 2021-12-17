# -*- coding: utf-8 -*-
import datetime
import io
import logging
import os
import shutil
import smtplib
import time
import unittest
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from subprocess import call
import requests

import schedule
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from constants import SMTP_SERVER, USERNAME, PASSWORD, SENDER
from email_template import email_template
import socket

logger = logging.getLogger()
logger.level = logging.INFO

# mo 和  zju 互查

RC_URL = 'https://s.momodel.cn'
ZJU_URL = 'https://mo.zju.edu.cn'
MO_URL = 'https://momodel.cn'
#
# check_url_dict = {
#     MO_URL: ZJU_URL,
#     ZJU_URL: MO_URL,
#     # RC_URL: MO_URL
# }

# check_url = check_url_dict.get(WEB_ADDR, MO_URL)

# check_url = 'https://s.momodel.cn'
check_url = 'https://momodel.cn'
# 机器人
api_url = "https://oapi.dingtalk.com/robot/send?access_token=06a7524b4c4ea76c895887cbde3e32f0656fdab66bab424c6f3d087342655f9c"

# 0 不测试
# 1 本地测试
# 2 rc 或 prod 或 zju 上测试
debugMode = 0

# check_url_name_dict = {
#     MO_URL: 'MOMODEL 公有云',
#     RC_URL: 'RC',
#     ZJU_URL: 'ZJU 浙大版'
# }

# check_url_name = check_url_name_dict.get(check_url)

if debugMode == 1:
    temp_file_path = '/Users/wangyujie/Pictures/test'
else:
    temp_file_path = '/home/admin/e-picture'


def send_email_now(email, subject, msg):
    msg['Subject'] = subject
    msg['From'] = formataddr(['AI 建模平台 Mo', 'service@momodel.ai'])
    msg['To'] = email
    smtp = smtplib.SMTP()
    smtp.connect(SMTP_SERVER)
    smtp.login(USERNAME, PASSWORD)
    receiver = email
    smtp.sendmail(SENDER, receiver, msg.as_string())
    smtp.quit()


def send_DinTalk(log_contents):
    IP = get_host_ip()
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    json_text = {
        "msgtype": "text",
        "at": {
            "atMobiles": [

            ],
            "isAtAll": False
        },
        "text": {
            "content": "公有云环境的项目创建异常,请检查网站.详情查收邮件" + format(log_contents) + str(IP)
        }
    }

    requests.post(api_url, json=json_text, headers=headers)


class NotebookTest(unittest.TestCase):
    def setUp(self):
        # 在服务器上跑改headless模式，测试使用可视化模式
        if debugMode == 1:
            # 可视化模式
            self.driver = webdriver.Chrome()
        else:
            # headless模式
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--window-size=1024,1024")
            self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def screen_shot(self):
        driver = self.driver
        picture_time = time.strftime("%Y-%m-%d-%H_%M_%S",
                                     time.localtime(time.time()))
        # 若目录不存在，创建新目录
        file_path = os.path.join(temp_file_path, 'picture')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        # 使用save_screenshot来截图
        try:
            driver.save_screenshot(
                os.path.join(file_path, picture_time + '.png'))
        except BaseException as pic_msg:
            print("截图失败：%s" % pic_msg)

    def test_notebook(self):
        driver = self.driver
        driver.get(check_url + "/user/login")
        logger.warning("窗口最大化")
        # 将浏览器最大化显示
        driver.maximize_window()
        # 点击选中登录tab
        driver.find_element_by_xpath(
            '//*[@id="content-wrap"]/div[1]/div/div/div[3]/div/div[1]/div/div[1]/div[2]').click()
        driver.find_element_by_id("username").clear()
        logger.warning("输入用户名")
        driver.find_element_by_id("username").send_keys("luxu99")
        driver.find_element_by_id("password").clear()
        logger.warning("输入密码")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("password").send_keys(Keys.RETURN)
        logger.warning("登录")
        time.sleep(3)
        # driver.find_element_by_id("Header-workspace").click()
        # driver.find_element_by_css_selector(
        # '#workspace > div:nth-child(3) > div.ant-tabs.ant-tabs-top.ant-tabs-line.ant-tabs-no-animation > div.ant-tabs-bar.ant-tabs-top-bar > div.ant-tabs-nav-container > div > div > div > div:nth-child(1) > div:nth-child(2)').click()
        # logger.warning("点击项目")
        # time.sleep(10)
        logger.warning("关闭活动弹窗")
        try:
            driver.find_element_by_css_selector(
                "body > div > div > div.ant-modal-wrap.ant-modal-centered > div > div.ant-modal-content > button > span ").click()
        except:
            pass
        time.sleep(5)

        # 上去之前改
        # 打开制造错误，测试发邮件
        # driver.find_element_by_xpath("(sakdfkashdf").click()

        # 跳转进工作台
        driver.get(check_url + "/workspace?tab=app")
        # print(driver.capabilities['version'])
        # logger.warning(driver.capabilities['version'])

        logger.warning("点击新建 app 按钮")
        driver.find_element_by_id("Newapp").click()
        time.sleep(5)
        logger.warning("点击确认按钮")
        driver.find_element_by_css_selector(
            "#Newapp > button").click()

        logger.warning("切换到 tab 2")
        time.sleep(60)

        for _ in range(3):
            try:
                self.switch_tab(2)
                break
            except:
                pass
            logger.warning('等待 30 s 后重试')
            time.sleep(30)

        logger.warning('进入 notebook 页面')
        for _ in range(3):
            try:
                if self.is_element_present(By.ID, "filebrowser"):
                    break
                else:
                    driver.refresh()
            except:
                pass
            time.sleep(60)

        # 点击进入 launcher 页面
        try:
            logger.warning("点击关闭小提示")
            driver.find_element_by_css_selector(
                'body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > button > span').click()
            time.sleep(3)
        except:
            logger.warning("没有找到小提示，跳过")
            pass

        # 确认 notebook 已打开
        logger.warning("找到 filebrowser 确保 notebook 成功打开")
        driver.find_element_by_css_selector("#filebrowser")

        #
        # 点击进入 launcher 页面
        logger.warning("点击 launcher tab")
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div.p-Widget.p-TabBar.p-DockPanel-tabBar.jp-Activity > ul > li:nth-child(1)").click()

        logger.warning('点击新建 notebook')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "* > div > div > div:nth-child(2) > div.jp-Launcher-cardContainer > div").click()

        logger.warning('点击新建 cell')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-commandMode > div > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div > div > div > div.CodeMirror-code > pre").click()
        logger.warning("input print('hello test') in the cell")

        time.sleep(3)
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div > textarea").send_keys(
            "print('hello test')\nprint('hello world')")

        logger.warning('运行 cell')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div > textarea").send_keys(
            Keys.SHIFT + Keys.ENTER)

        # 输入循环代码
        logger.warning('点击新建 cell')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div.p-Widget.jp-Cell.slideCell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-active.jp-mod-selected.jp-mod-collapsed > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div > div > div > div.CodeMirror-code > pre").click()
        logger.warning("input for-loop in the cell")
        time.sleep(3)

        data = 'sum1=0\nfor i in range(100):\nsum1 += i\n\bprint(sum1)'
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div.p-Widget.jp-Cell.slideCell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-active.jp-mod-selected.jp-mod-collapsed > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div > textarea").send_keys(
            data)
        logger.warning('运行 cell')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div.p-Widget.jp-Cell.slideCell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-active.jp-mod-selected.jp-mod-collapsed > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.p-Panel.code-bar-parent > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div > textarea").send_keys(
            Keys.SHIFT + Keys.ENTER)
        assert driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div > div.p-Widget.jp-Notebook.jp-mod-scrollPastEnd.jp-NotebookPanel-notebook.jp-mod-editMode > div:nth-child(2) > div.p-Widget.p-Panel.jp-Cell-outputWrapper > div.p-Widget.jp-OutputArea.jp-Cell-outputArea > div > div.p-Widget.jp-RenderedText.jp-mod-trusted.jp-OutputArea-output > pre").text == '4950'
        driver.close()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.screen_shot()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def switch_tab(self, num):
        driver = self.driver
        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        driver.switch_to.window(handles[num - 1])  # 跳转到第num个窗口


def get_host_ip():
    ip = '0.0.0.0'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.0.0.1', 8080))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def send_email(log_contents):
    # 通知开发者
    IP = get_host_ip()
    if check_url == 'https://momodel.cn' and not debugMode:
        emails = 'a498593970@163.com,13879892236@163.com,lzfxxx@foxmail.com,jx.li@momodel.ai,progerchai@qq.com,taiyangfushezhi@qq.com,498593970@qq.com'
        # ['491730572@qq.com', 'chengsi1992@126.com', '291003720@qq.com',
        #       'rainbowgirlanita@gmail.com', 'lzfxxx@gmail.com',
        #       'jx.li@momodel.ai','498593970@qq.com']
        subject = '公有云' + ' 项目创建异常，请检查网站' + str(IP)
        # print('线上已发送')
    else:
        emails = '498593970@qq.com,taiyangfushezhi@qq.com,progerchai@qq.com,13879892236@163.com'
        subject = '公有云' + '测试环境的项目创建异常，请检查网站' + str(IP)

    text = email_template(
        title="<div><h3 style='margin-left: 12px; line-height: 1.1;"
              "color: #000; font-size: 27px;'>{0} 项目创建错误"
              "<a href= '{1}/workspace' target='_blank' "
              "style='color: #1980FF !important;"
              "text-decoration:underline;margin-left: "
              "24px;font-size: 24px;'>进入网站查看</a></h3></div>".format(
            '公有云', 'momodel.cn'),
        middle="<div style='margin-left: 24px; margin-top: -24px; "
               "list-style-position: inside;'>"
               "<div>日志如下:</div>"
               "<div style='white-space: pre-wrap;'>{0}</div>"
               "<div>".format(log_contents))
    msg = MIMEMultipart('mixed')

    text_plain = MIMEText(text, 'html', 'utf-8')
    msg.attach(text_plain)

    # 错误截图
    image_dir = os.path.join(temp_file_path, 'picture')

    pictures = os.listdir(image_dir)
    for p in pictures:
        image_file = os.path.join(image_dir, p)
        with open(image_file, 'rb') as f:
            image_content = f.read()
        image_apart = MIMEImage(image_content,
                                image_file.split('.')[-1])
        image_apart.add_header('Content-Disposition', 'attachment', filename=(
            'utf-8', '', time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(
                time.time())) + '_screen_shot.png'))
        msg.attach(image_apart)
    shutil.rmtree(image_dir)
    # print('screen本地文件删除成功！')

    # 发送邮件

    send_email_now(emails, subject, msg)
    # 发送钉钉
    send_DinTalk(log_contents)


def run_all_test():
    # 删除创建的文件
    # user = UserBusiness.get_by_username('luxu99')
    # projects = Project.objects(user=user, type='app')
    # for key, e in enumerate(projects):
    #     if 'luxu' in e.display_name:
    #         AppBusiness.remove_project_by_id(str(e.id), user.user_ID)
    #         time.sleep(2)
    # call(
    #     "kubectl delete pods $(kubectl get pods | grep jupyter-4f4549ll415a42z14e4a1cffn5a5834474acy84927x5147505 | awk '{print $1}')",
    #     shell=True)
    result = requests.delete(
        'https://momodel.cn/pyapi/user/notebook_autotest_project?username=luxu99&token=a2c4bebb78d5569572dc486c761f1723')
    print(result.text)

    # 只在 prod 和 rc 上开启测试
    # if not debugMode and WEB_ADDR not in ['https://momodel.cn',
    #                                       'https://s.momodel.cn',
    #                                       'https://mo.zju.edu.cn']:
    #     return
    # 最多尝试 3 次，
    all_test_times = 3
    log_capture_string = io.StringIO()
    stream_handler = logging.StreamHandler(log_capture_string)
    logger.addHandler(stream_handler)
    for i in range(all_test_times):
        # logger.warning(
        #     '------------------第 {i} 次测试------------------')
        logger.warning(
            '------  时间: {0} ------'.format(
                datetime.datetime.now()))
        suite = unittest.TestLoader().loadTestsFromTestCase(NotebookTest)
        test_result = unittest.TextTestRunner(verbosity=0).run(suite)
        # 如果报错，记录错误，并等待 300 秒后重试一次或发送错误邮件
        if test_result.errors:
            # test, errors = test_result.errors[0]
            # all_errors.append(errors)
            log_contents = log_capture_string.getvalue()
            # 如果是最后一次，发送错误邮件通知
            if i == all_test_times - 1:
                send_email(log_contents)
            # 否则，五分钟后再次尝试
            else:
                time.sleep(60)
        else:
            break
    log_capture_string.close()
    logger.removeHandler(stream_handler)


if __name__ == "__main__":
    if debugMode:
        run_all_test()
    else:
        schedule.every().hour.do(run_all_test)
        while True:
            schedule.run_pending()
            time.sleep(1)
