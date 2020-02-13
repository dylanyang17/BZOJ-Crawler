import time, os, random
from multiprocessing import Pool
import requests
# from fake_useragent import UserAgent
import cfscrape
import pickle

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


def download_one(url):
    t0 = time.time()
    print(url)
    headers = {
        'Cookie':
            'PHPSESSID=57m4qqnnofcoqsjvftn7jvoiq5; _ga=GA1.2.91683436.1581503238; _gid=GA1.2.1201712388.1581503238; __cfduid=d3d70050c1c9293a470a940b2dd15f9ed1581582212; cf_clearance=9ae05454cf213820e25a899db526659f8cfa27eb-1581587877-0-150',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    filename = url.split('/')[-1]
    if os.path.exists(filename):
        print('已下载，跳过:', filename)
        return
    resp = requests.get(url, headers=headers, stream=True)
    print(resp.status_code)
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


def download(processing_num, urls):
    p = Pool(processing_num)
    for url in urls:
        #download_one(url)
        p.apply_async(download_one, args=(url,))
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
    # st = 1000
    # while st <= 2000:
    #     urls = get_urls(st, st + 50 - 1)
    #     print('开始下载一组：', '%d ~ %d' % (st, st + 50 - 1))
    #     t0 = time.time()
    #     download(8, urls)
    #     print('下载完毕一组：', '%d ~ %d' % (st, st + 50 - 1), '  耗时：', time.time() - t0)
    #     st += 50
    while True:
        urls = get_urls(1000, 2000)
        t0 = time.time()
        download(2, urls)
        print('总耗时：', time.time() - t0)