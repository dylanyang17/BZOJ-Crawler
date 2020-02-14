# BZOJ
Data of BZOJ &amp; Crawler

主要代码为 download.py。

需要注意的是，因为有各种反爬措施，目前的做法是每隔一定时间通过 selenium 控制浏览器，固定 User-Agents，访问后得到相应的Cookie并填入代码中开始爬取。由于有访问数限制，尽管是多进程爬取，在后期也会出现很多 503，所以干脆只用 2 进程。

支持跳过已下载文件，下载文件时存入临时文件避免保存不完整文件。

爬取网址为 http://darkbzoj.tk/data
