from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from pyquery import PyQuery as pq
import  pymongo

class Main(object):
    def __init__(self):
        self.browser=webdriver.Chrome()
        self.wait=WebDriverWait(self.browser,10)

    def search(self,url):
        self.browser.get(url=url)
        try:
            total=self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#J_waterfallPagination > div > div > span.totalPage'))
            )
            return total.text
        except TimeoutException:
            return  self.search()

    def next_page(self,):
        try:
            btn=self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_waterfallPagination > div > div > a.page-next.iconfont'))
            )
            btn.click()

        except TimeoutException:
            self.next_page()

    def parce_produce(self):
        html=self.browser.page_source
        doc=pq(html)
        items=doc('#searchResult .view .item').items()
        for item in items:
            product={
                'price':item.find('.info .price .pricedetail').text()[3:],
                'bady_tiele':item.find('.info .title').text(),
                'shop':item.find('.info .shopName .shopNick').text(),
                'paynumber': item.find('.info .shopName .payNum').text()[:-3]
            }
            print(product)
            self.sava_mongo(product)

    def sava_mongo(self,data):
        link=pymongo.MongoClient(host='localhost',port=27017)
        db=link.taobao
        collection=db.ketingdeng123
        collection.insert_one(data)

    def main(self):
        url='https://uland.taobao.com/sem/tbsearch?spm=a2e15.8261149.07626516003.2.432829b4vTQJCk&refpid=mm_26632258_3504122_32538762&clk1=3f9e2155f05c3766efd861568f2c1b6b&keyword=%E5%AE%A2%E5%8E%85%E7%81%AF&page=3&_input_charset=utf-8'
        re_total=self.search(url)
        total=re_total[1:4]

        for i in range(1,int(total)+1):
            self.next_page()
            self.parce_produce()

if __name__ == '__main__':
    c=Main()
    c.main()
