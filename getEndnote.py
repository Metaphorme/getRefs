#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Metaphorme
# @Site    : https://github.com/Metaphorme/getRefs

import os
import time
from random import uniform
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

refs = []
with open("refs.txt", "r") as f:
    for line in f.readlines():
        refs.append(line.strip())

# 设置代理，chrome 似乎只支持 socks5 代理
PROXY = "socks5://localhost:12345"

# 设置下载方式
# 推荐用 browser，因为 requests 会被谷歌学术识别为机器人
DOWNLOAD_TYPE = 1  # 0: requests, 1: browser


# 检查元素是否存在
def check_element_exists(driver, element, condition):
    try:
        if condition == 'class':
            driver.find_element(By.CLASS_NAME, element)
        elif condition == 'id':
            driver.find_element(By.ID, element)
        elif condition == 'xpath':
            driver.find_element(By.XPATH, element)
        return True
    except Exception:
        return False


def download_by_requests(url):
    enw = requests.get(url=url,
                       headers={
                           'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},
                       proxies={"https": PROXY}
                       ).content
    # 保存文件
    _filename = ref[:15] + ".enw"
    with open("enws/" + _filename, "wb") as _f:
        _f.write(enw)
        print(f"已保存 {ref} 为 {_filename}")


def download_by_browser(url):
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[-1])
    browser.get(url)

    # 重设文件名
    _filename = ref[:15] + ".enw"
    while not os.path.exists("enws/scholar.enw"):
        time.sleep(0.5)
    os.replace("enws/scholar.enw", "enws/" + _filename)
    print(f"已保存 {ref} 为 {_filename}")


def clear_windows():
    while len(browser.window_handles) > 1:
        browser.switch_to.window(browser.window_handles[-1])
        browser.close()


if __name__ == "__main__":
    # 将当前文件夹加入环境变量
    os.environ['PATH'] = os.getcwd() + ';' + os.environ['PATH']

    # 设置下载路径
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd() + '/enws'}

    # 设置代理
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=' + PROXY)
    options.add_experimental_option('prefs', prefs)

    # 打开浏览器
    browser = webdriver.Chrome(options=options)

    # 遍历引文下载 enw 格式文件
    for ref in refs:
        failtime = 0
        while True:
            try:
                # 创建新页面
                browser.execute_script("window.open('');")
                browser.switch_to.window(browser.window_handles[-1])

                # 打开谷歌学术
                browser.get("https://scholar.google.com/scholar?&q=" + ref)

                # 检测是否出现人机验证，若出现则等待
                time.sleep(2)  # 等待元素加载
                if check_element_exists(browser, 'gs_captcha_ccl', 'id'):
                    input("请完成人机验证后按回车继续")
                    time.sleep(2)  # 等待元素加载

                # 点击引用按钮
                sitebottom = browser.find_element(By.XPATH,
                                                  '/html/body/div/div[10]/div[2]/div[3]/div[2]/div/div/div[3]/a[2]')
                sitebottom.click()

                # 下载 enw 文件（gs_citi 类，正文为 Endnote）
                time.sleep(uniform(2, 3))  # 等待元素加载
                endnote = browser.find_element(By.XPATH,
                                               '/html/body/div/div[4]/div/div[2]/div/div[2]/a[2]').get_attribute(
                    'href')

                if DOWNLOAD_TYPE:
                    download_by_browser(endnote)
                else:
                    download_by_requests(endnote)

                # 关闭除第一页的所有页面
                clear_windows()

                # 等待一会
                browser.switch_to.window(browser.window_handles[0])
                _sleeptime = uniform(10, 30)
                print(f"等待 {_sleeptime} 秒后继续")
                print(
                    f"还剩 {len(refs) - refs.index(ref) - 1} 个文件，可能还需要 {round((20 * (len(refs) - refs.index(ref) - 1)) / 60, 2)} 分钟")
                time.sleep(_sleeptime)
                break

            except Exception as e:
                failtime += 1
                if failtime < 3:
                    print(f"下载 {ref} 失败，原因：{e}将重试")
                    _sleeptime = uniform(10, 30)
                    print(f"等待 {_sleeptime} 秒后继续")
                else:
                    print(f"下载 {ref} 失败，原因：{e}，跳过")
                    _sleeptime = uniform(5, 10)
                    print(f"等待 {_sleeptime} 秒后继续")
                    break
                # 关闭除第一页的所有页面
                clear_windows()
                time.sleep(_sleeptime)

    browser.quit()
    print("下载完毕！")
