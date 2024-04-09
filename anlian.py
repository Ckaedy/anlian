import requests
from bs4 import BeautifulSoup
import re
import argparse
import html
from urllib.parse import urlparse
from requests.exceptions import RequestException, SSLError
# ANSI 转义序列
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
ENDC = '\033[0m'

# 定义要检查的关键词列表，可以根据需要添加或修改
keywords = ['游戏官网','棋盘','开元','腾龙','开户','开云', '赌博', '体育平台', '体育官方', 'ios/安卓版/手机APP下载', '全球线上娛樂','赌船','赌','博彩','官网app手机版','(中国)官方网站','K1体育','体育','真人','彩票','半岛','国际客服','亚博','vip网页手机版最新登录入口','(China)官方网站','澳门','开奖']

# 定义一个函数来解码HTML实体编码
def decode_html_entities(html_code):
    return html.unescape(html_code)

# 定义一个函数来检查网页源代码中是否存在指定的关键词
def check_for_keywords(html_code):
    found_keywords = []
    for keyword in keywords:
        if re.search(keyword, html_code, re.IGNORECASE):
            found_keywords.append(keyword)
    return found_keywords

# 定义一个函数来检查网页源代码中是否存在HTML实体编码并解码后匹配关键词
def check_for_hidden_links(url):
    try:
        # 添加协议（http或https）以防止报错
        if not urlparse(url).scheme:
            url = 'http://' + url
        
        # 获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查是否出现异常

        # 获取网页源代码
        soup = BeautifulSoup(response.content, 'html.parser')
        html_code = str(soup)
        
        # 解码HTML实体编码并检查关键词
        decoded_html = decode_html_entities(html_code)
        found_keywords = check_for_keywords(decoded_html)

        if found_keywords:
            print(f"{RED}[存在暗链]{ENDC} 在 {url} 中发现关键词:", found_keywords)
        else:
            print(f"{GREEN}[手工确认]{ENDC} 在 {url} 中未发现任何关键词，请手工确认。")

    except Exception as e:
        print(f"{YELLOW}[网页错误]{ENDC} 访问 {url} 时出现网页错误。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查网页中的暗链")
    parser.add_argument("urls", metavar="URL", nargs="*", help="要检查的网址列表")
    parser.add_argument("-f", "--file", metavar="FILE", help="从文件中读取网址列表")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as file:
                urls = file.readlines()
                urls = [url.strip() for url in urls]
        except FileNotFoundError:
            print("文件未找到。")
            exit()
    else:
        urls = args.urls

    if not urls:
        print("请提供至少一个网址。")
        exit()

    for url in urls:
        check_for_hidden_links(url)