# -*- coding: utf-8 -*-
import scrapy
import re
import os
import requests
from scrapy import log
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest
from msg58.items import Msg58Item   

my_cookies={}

item=Msg58Item()
my_headers = {
"Accept": "*/*",
"Accept-Encoding": "gzip,deflate",
"Accept-Language": "en-US,en,q=0.8,zh-TW,q=0.6,zh,q=0.4",
"Connection": "keep-alive",
"Content-Type":" application/x-www-form-urlencoded, charset=UTF-8",
"User-Agent": "Mozilla/5.0 (Macintosh' Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
"Referer": "http://xa.58.com/"
}
class Spider58Spider(scrapy.Spider):
    name = "spider58"
    allowed_domains = ["58.com"]
    start_urls = ['http://xa.58.com/youerjiaoshi/']

    def parse(self, response):
        search_page_html=response.body
        search_page_soup=BeautifulSoup(search_page_html,'lxml')
        next_url=search_page_soup.find('a',attrs={'class':'next'}).get('href')
        print next_url

        all_dl=search_page_soup.find_all('dl',attrs={'__addition':'0'})
        for single_dl in all_dl:
            dt=single_dl.find('dt')
            #dd_w271=single_dl.find('dd',attrs={'class':'w271'})
            #dd_w271_a=dd_w271.find('a')
            dt_in_a=dt.find('a')
            job_name=dt_in_a.string
            #company=dd_w271_a.string
            detail_url=dt_in_a.get('href')
            #print next_url
            #html_num=detail_url.split('?')[0].split('/')[-1]
            #mobile_detail_url='http://m.58.com/xa/zhuanye/'+html_num

            if detail_url:
                yield Request(detail_url,headers=my_headers,meta={'job_name':job_name},callback=self.parse_detail)


    def parse_detail(self,response):
        detail_page_html=response.body
        detail_page_soup=BeautifulSoup(detail_page_html,'lxml')
        work_place=detail_page_soup.find('p',attrs={'class':'detail_adress'}).string

        company_p=detail_page_soup.find('p',attrs={'class':'comp_baseInfo_title'})
        company=company_p.find('a').string

        script_text=detail_page_soup.find('script').string
        person_p=re.compile(r'contactPerson : ".*?"',re.I)
        person_m=person_p.search(script_text)
        person_name=person_m.group().split('"')[1]

        image_code_p=re.compile(r'pagenum :".*?"',re.I)
        image_code_m=image_code_p.search(script_text)
        image_code=image_code_m.group().split('"')[1]

        job_name=response.meta['job_name']
        
        print job_name

        if image_code:
            if '_' in image_code:
                image_code=image_code.split('_')[0]
            get_phone_number(image_code,job_name,company,work_place,person_name)



def get_phone_number(image_code,job_name,company,work_place,person_name):
        image_path=save_image(image_code)
        if image_path != 'error':
            output=os.popen('sh /Users/ablecheng/Documents/tess '+image_path)
            result=output.read()

            phone_p=re.compile(r'\d*',re.I)
            phone_m=phone_p.search(result)

            if phone_m.group():
                print phone_m.group()
                os.popen('rm -rf '+image_path)
                phone_number=phone_m.group()
                print job_name,company,work_place,person_name,phone_number

            else:
                os.popen('rm -rf '+image_path)
                get_phone_number(image_code,job_name,company,work_place,person_name)

        


    #def start_requests(self):
    #    for url in self.start_urls:          
    #        yield Request(url, cookies=my_cookies,headers=my_headers)  

def save_image(image_code):
        image_url='http://image.58.com/showphone.aspx?t=v55&v='+image_code
        image_response=requests.get(image_url,stream=True)
        image_content=image_response.content
        image_dir='/Users/ablecheng/Documents/data/'
        image_name=image_code+'.gif'
        os.popen('touch '+image_dir+image_name)
        jpg_ob=open(image_dir+image_name,'w')
        jpg_ob.write(image_content)
        jpg_ob.close()
        return image_dir+image_name


















