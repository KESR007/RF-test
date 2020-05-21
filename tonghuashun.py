from lxml import etree
import requests
import os

header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
,"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
,"Accept-Encoding": "gzip, deflate"
,"Accept-Language": "zh-CN,zh;q=0.9"
,"-Control": "max-age=0"
,"Connection": "keep-alive"
,"Cookie": "Hm_lvt_f79b64788a4e377c608617fba4c736e2=1588863284; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1588863284; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1587912362,1587912390,1588862588,1588863284; historystock=600725; spversion=20130314; v=AgTNs8ziBjR_ZbL4J23qM_G_1Yn1HSiH6kG8yx6lkE-SSaq_Ri34FzpRjFlt"
,"Host": "data.10jqka.com.cn"
,"Upgrade-Insecure-Requests": "1"
}

def get_maxpage():
    url = "http://data.10jqka.com.cn/market/ggsyl/"
    r = requests.get(url, headers=header)
    selector = etree.HTML(r.text, etree.HTMLParser())
    max_page = selector.xpath('//div[@class="m-page J-ajax-page"]/a[last()]//@page')
    max_page=int(max_page[0])
    print(max_page)
    return max_page

def get_all(max_page):
    max_col = 50
    selector_list=[]
    page_data = []

    """获取每一页的选择器"""
    for each_page in range(max_page):
        url = "http://data.10jqka.com.cn/market/ggsyl/field/syl/order/desc/page/%d/ajax/1/free/1/" % (each_page+1)
        r = requests.get(url, headers=header)
        #print(url)
        selector_list.append(etree.HTML(r.text, etree.HTMLParser()))
        print(r.text)

    """根据每一页的选择器和每一行的xPATH提取data"""
    for each_selector in selector_list:
        for each_col in range(max_col):
            path = '//table[@class="m-table J-ajax-table"]/tbody/tr[%d]//text()' % (each_col + 1)
              #  print(path)
            data = each_selector.xpath(path)
            if not data==[]:
                data = data[1::2]
                page_data.append(data)
    print(len(page_data))
    return page_data

def write_file(data):
    with open("stocks.txt",'a') as f:
        for each_line in data:
            f.write(str(each_line)+"\n")


if __name__ == "__main__":
    max_page=get_maxpage()
    page_data=get_all(max_page)
    for each in page_data:
        print(each)











