import time, os, random
from multiprocessing import Pool
import requests, sys
import threading
from get_cookie import get_cookie

# ua = UserAgent()


def randstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    ret = ''
    for i in range(num):
        ret += random.choice(H)
    return ret


def get_tmpname():
    """
    返回一个随机的临时名字
    :return:
    """
    return 'tmp' + randstr(16)


def download_one(url, cookie, user_agent, lowest_speed, show_progress):
    """
    子进程会调用该函数，以cookie和user_agent对url进行访问，下载最低速度为 lowest_speed，show_progress 表明是否显示下载过程
    """
    print(url)
    headers = {
        'Cookie': cookie,
        'User-Agent': user_agent
    }
    filename = url.split('/')[-1]
    if os.path.exists(filename):
        print('已下载，跳过:', filename)
        return
    resp = requests.get(url, headers=headers, stream=True, timeout=5)  # 一定要加timeout!
    print(resp.status_code, filename)
    # l = resp.headers.get('Content-Length', -1)
    # if l / 1024 / 1024 > 49:
    #     print('超过大小限制，跳过：', filename)
    #     return
    # if resp.status_code == 200:
    #     l = resp.headers.get('Content-Length', -1)
    #     print('test', l/1024/1024)
    #     if l/1024/1024 > 49:
    #         print('超过大小限制，跳过：', filename)
    #         return
    #     else:
    #         print('开始下载:', filename, ' 大小(B):', l)
    if resp.status_code != 200:
        print('异常:', filename, ' status_code:', resp.status_code)
        return

    while True:
        tmpname = get_tmpname()
        if not os.path.exists(tmpname):
            break

    fail = False

    t0 = time.time()          # 起始时间戳
    last_sec_t = time.time()  # 上一秒的时间戳
    last_min_t = time.time()  # 上一分钟的时间戳
    cnt = 0  # 目前已经下载的大小 (B)
    last_sec_cnt = 0  # 上一秒时刻下载的大小 (B)
    last_min_cnt = 0  # 上一分钟时刻下载的大小 (B)
    with open(tmpname, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                cnt += len(chunk)
                f.write(chunk)
            now_t = time.time()
            if now_t - last_min_t >= 60:
                speed = (cnt - last_min_cnt) / (now_t - last_min_t) / 1024
                if show_progress:
                    print('%s: 分钟均速 %.2fKB/s' % (filename, speed))
                if speed < lowest_speed:
                    fail = True
                    break
                last_min_cnt = cnt
                last_min_t = now_t
            if now_t - last_sec_t >= 1:
                if show_progress:
                    print('%s: 已下载 %.2fMB  下载速度 %.0fKB/s' % (filename, cnt / 1024 / 1024, (cnt - last_sec_cnt) / (now_t - last_sec_t) / 1024))
                last_sec_t = time.time()
                last_sec_cnt = cnt
    if fail:
        print('%s: 速度过低终止下载 耗时：%d' % (filename, time.time() - t0))
        os.remove(tmpname)
    else:
        os.rename(tmpname, filename)
        print('下载成功:', filename, ' 总大小: %.2fMB ' % (cnt / 1024 / 1024), '耗时: ', time.time() - t0)


def download(processing_num, urls, refresh_interval, chunk, lowest_speed, show_progress):
    """
    :param processing_num: 进程数
    :param urls: 要下载的列表
    :param refresh_interval: 刷新cookie的时间间隔（s）
    :param chunk: 每个进程池中进程的数目 （太大会导致超过刷新间隔再刷新cookie）
    :param lowest_speed: 最低速度，若检测到一分钟内的均速低于 lowest_speed (KB/s)则退出
    :param show_progress: 是否显示下载过程
    :return:
    """

    cookie = ''
    user_agent = ''
    t0 = time.time() - refresh_interval - 1
    url_chunks = [urls[i:i+chunk] for i in range(0, len(urls), chunk)]
    for url_chunk in url_chunks:
        if time.time() - t0 >= refresh_interval:
            cookie, user_agent = get_cookie()
            t0 = time.time()
            print('cookie: ' + cookie)
            print('User-Agent: ' + user_agent)
        p = Pool(processing_num)
        for url in url_chunk:
            res = p.apply_async(download_one, args=(url, cookie, user_agent, lowest_speed, show_progress))
            # res.wait(10)
        p.close()
        p.join()


def get_urls(beg, end):
    """
    返回 url 列表
    :param beg: 要下载的起始题号
    :param end: 要下载的结束题号
    :return: 一个 url 列表
    """
    urls = []
    for i in range(beg, end + 1):
        urls.append('http://darkbzoj.tk/data/' + str(i) + '.zip')
    return urls


if __name__ == '__main__':
    while True:
        urls = get_urls(4001, 4999)
        t0 = time.time()
        download(4, urls, 10*60, 40, 20, True)
        print('总耗时：', time.time() - t0)