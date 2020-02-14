import time, os, random
from multiprocessing import Pool
import requests
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


def download_one(url, cookie, user_agent):
    t0 = time.time()
    print(url)
    headers = {
        'Cookie': cookie,
        'User-Agent': user_agent
    }
    filename = url.split('/')[-1]
    if os.path.exists(filename):
        print('已下载，跳过:', filename)
        return
    resp = requests.get(url, headers=headers, stream=True)
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

    with open(tmpname, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    os.rename(tmpname, filename)
    print('下载成功:', filename, ' 耗时:', time.time() - t0)


def download(processing_num, urls, refresh_interval, chunk):
    """
    :param processing_num: 进程数
    :param urls: 要下载的列表
    :param refresh_interval: 刷新cookie的时间间隔（s）
    :param chunk: 每个进程池中进程的数目 （太大会导致超过刷新间隔再刷新cookie）
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
            p.apply_async(download_one, args=(url, cookie, user_agent))
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
        urls = get_urls(3001, 4000)
        t0 = time.time()
        download(2, urls, 10*60, 12)
        print('总耗时：', time.time() - t0)