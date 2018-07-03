# coding: utf-8
from collector import urlToIllustId

def test_urlからillust_idを抜き出せる():
    expected = '69462003'
    url = 'https://i.pximg.net/c/240x480/img-master/img/2018/06/30/01/00/03/69462003_p0_master1200.jpg'
    assert expected == urlToIllustId(url)

def test_urlにillust_idらしきものが見つからないならfalseを返せる():
    expected = False
    assert expected == urlToIllustId('https://example.com')
