import time
from selenium import webdriver


def get_cookie():
    """
    返回Cookie字符串和User-Agent字符串
    :return:
    """
    cnt = 0
    while True:
        cnt += 1
        print('尝试第 %d 次获取 Cookie...' % cnt)
        cookie_names = ['__cfduid', 'cf_clearance']  # 设定需要获得的cookie名
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument('User-Agent=%s' % user_agent)
        options.add_argument('headless')
        browser = webdriver.Chrome(options=options)
        browser.get("http://darkbzoj.tk/data")
        time.sleep(10)
        cookie = ''
        flag = False
        for name in cookie_names:
            if browser.get_cookie(name) is None:
                flag = True
                break
            cookie = cookie + name + '=' + browser.get_cookie(name)['value'] + ';'
        browser.close()
        if not flag:
            print('获取 Cookie 成功!')
            return cookie, user_agent


if __name__ == '__main__':
    print(get_cookie())
