# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
import base64
import os
from bs4 import BeautifulSoup
from urlparse import urlparse
import sys
import os
from scrapy.http import Request, FormRequest


default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)




my_headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip,deflate",
"Accept-Language": "en-US,en,q=0.8,zh-TW,q=0.6,zh,q=0.4",
"Connection": "keep-alive",
"Content-Type":" application/x-www-form-urlencoded, charset=UTF-8",
"User-Agent": "Mozilla/5.0 (Macintosh' Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
'Referer':'http://www.freebuf.com/',
'Cookie':'aliyungf_tc=AQAAACJSmwIqmwEADjfscxRgjEpC3zH9; 3cb185a485c81b23211eb80b75a406fd=1490772608; Hm_lvt_cc53db168808048541c6735ce30421f5=1489655942,1489655973,1489996021,1490858170; Hm_lpvt_cc53db168808048541c6735ce30421f5=1491119938'
}
request_args={
'wait':0.5
}
base_local_path='/Users/ablecheng/Documents/data/freebuf'
base_static_local_path='/Users/ablecheng/Documents/data/freebuf/static'
static_source=['.jpg','.jpeg','.js','.css','.png','gif',]

class FreebufSpiderSpider(scrapy.Spider):
    name = "freebuf_spider"
    allowed_domains = [
    "www.freebuf.com",
    '3001.net'
    ]
    start_urls = [
    #'http://static.3001.net/js/header/jquery.min.js'
    'http://www.freebuf.com/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,headers=my_headers)
            #yield Request(url, self.parse_static,headers=my_headers)

    def parse(self, response):
        save_local(response)
        freebuf_soup=BeautifulSoup(response.body,'lxml')
        all_href_soup=freebuf_soup.find_all(href=True)
        for href_item_soup in all_href_soup:
            href_url_item = href_item_soup.get('href')
            if href_url_item:
                href_url_item_result=urlparse(href_url_item)
                if href_url_item_result.scheme == 'http':
                    parse_result=parse_to_local_path(href_url_item_result)
                    if parse_result:
                        url_page_name=parse_result[0]
                        url_path=parse_result[1]
                        filename=parse_result[2]
                        filepath=parse_result[3]
                        if os.path.exists(filename):
                            pass
                        else:
                            #yield Request(href_url_item , self.parse_static , headers=my_headers)
                            if junge_static(href_url_item_result.path):
                                yield Request(href_url_item , self.parse_static,headers=my_headers)
                            else:
                                yield SplashRequest(href_url_item,self.parse,args=request_args,headers=my_headers)

        all_src_soup=freebuf_soup.find_all(src=True)
        for src_item_soup in all_src_soup:
            src_url_item=src_item_soup.get('src')
            if src_url_item:
                src_url_item_result=urlparse(src_url_item)
                if src_url_item_result.scheme == 'http':
                    parse_result=parse_to_local_path(src_url_item_result)
                    if parse_result:
                        url_page_name=parse_result[0]
                        url_path=parse_result[1]
                        filename=parse_result[2]
                        filepath=parse_result[3]
                        if os.path.exists(filename):
                            pass
                        else:
                            #yield Request(src_url_item , self.parse_static , headers=my_headers)
                            if junge_static(src_url_item_result.path):
                                yield Request(src_url_item , self.parse_static,headers=my_headers)
                            else:
                                yield SplashRequest(src_url_item , self.parse , args=request_args,headers=my_headers)

    def parse_static(self , response):
        save_local(response)


def junge_static(url_page_name):
    for static_item in static_source:
        if static_item in url_page_name:
            return True
    return False

def save_local(response):
    url_result=urlparse(response.url)
    parse_result=parse_to_local_path(url_result)
    url_page_name=parse_result[0]
    url_path=parse_result[1]
    filename=parse_result[2]
    filepath=parse_result[3]
    print filename
    if junge_static(url_page_name):
        html_content=response.body
    else:
        html_content=get_html_content(response)
    if os.path.exists(filepath):
        pass
    else :
        os.makedirs(filepath)

    file_ob=open(filename,'w')
    file_ob.write(html_content)
    file_ob.close()







def get_html_content(response):
    url_page_soup=BeautifulSoup(response.body, 'lxml')
    all_href_soup=url_page_soup.find_all(href=True)
    for href_item_soup in all_href_soup:
        href_url_item = href_item_soup.get('href')
        if href_url_item:
            href_url_item_result=urlparse(href_url_item)
            if href_url_item_result.scheme == 'http':
                href_item_soup['href']=change_url(href_url_item_result)

    all_src_soup=url_page_soup.find_all(src=True)
    for src_item_soup in all_src_soup:
        src_url_item=src_item_soup.get('src')
        if src_url_item:
            src_url_item_result=urlparse(src_url_item)
            if src_url_item_result.scheme == 'http':
                src_item_soup['src']=change_url(src_url_item_result)
    return str(url_page_soup)









def change_url(url_item_result):
    if url_item_result.netloc == 'www.freebuf.com':
        changed_url=base_local_path+url_item_result.path
    elif '3001.net' in url_item_result.netloc:
        changed_url=base_static_local_path+url_item_result.path
    else:
        changed_url=url_item_result.scheme+'://'+url_item_result.netloc+url_item_result.path
    return changed_url




def parse_to_local_path(url_result):
    if url_result.netloc == 'www.freebuf.com':
        url_result_path_lastname=url_result.path.split('/')[-1]
        if  url_result_path_lastname == '':
            url_page_name='index.html'
            url_path=url_result.path
            filename=base_local_path+url_path+'/'+url_page_name
            filepath=base_local_path+url_path
        elif '.' not in  url_result_path_lastname:
            url_page_name='index.html'
            url_path=url_result.path
            filename=base_local_path+url_path+'/'+url_page_name
            filepath=base_local_path+url_path
        else :
            url_page_name=url_result_path_lastname
            url_page_name_len=len(url_page_name)
            url_path=url_result.path[:-url_page_name_len]
            filename=base_local_path+url_result.path
            filepath=base_local_path+url_path
        return [url_page_name,url_path,filename,filepath]
    elif '3001.net' in url_result.netloc:
        url_result_path_lastname=url_result.path.split('/')[-1]
        if  url_result_path_lastname == '':
            url_page_name='index.html'
            url_path=url_result.path
            filename=base_static_local_path+url_path+url_page_name
            filepath=base_static_local_path+url_path
        elif '.' not in  url_result_path_lastname:
            url_page_name='index.html'
            url_path=url_result.path
            filename=base_static_local_path+url_path+'/'+url_page_name
            filepath=base_static_local_path+url_path
        else :
            url_page_name=url_result_path_lastname
            url_page_name_len=len(url_page_name)
            url_path=url_result.path[:-url_page_name_len]
            filename=base_static_local_path+url_result.path
            filepath=base_static_local_path+url_path
        return [url_page_name,url_path,filename,filepath]





























        
