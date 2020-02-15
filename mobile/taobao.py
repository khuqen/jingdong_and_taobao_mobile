'''
@Description: 爬取淘宝
@Autor: khuqen
@Date: 2020-01-07 09:58:33
@LastEditors  : khuqen
@LastEditTime : 2020-01-07 22:01:20
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree
import time
import csv

file = open('TBMobileData.csv', 'w', newline='',encoding='utf-8')
w = csv.writer(file)
w.writerow(['store', 'name', 'sales', 'price'])
# 爬取手机类别
things = "手机"
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get('https://login.taobao.com/member/login.jhtml')

# 等待扫码登录
time.sleep(10)
def scan_login():
    #跳过滑动验证
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--proxy--server=127.0.0.1:8080')#使用代理IP,告诉服务器这是人为操作

    search = driver.find_element_by_xpath('//*[@id="q"]') #在kw内输入
    search.send_keys(things)#获取输入的商品
    time.sleep(2)
    search.send_keys(Keys.ENTER)#按回车 
    time.sleep(4)#大约加载4秒
    maxPage = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]').text #查找到商品的最大页数
    print ("您所查询的商品",maxPage)

def start(starPage,endPage):#选择商品页数片段
    for num in range(starPage,endPage+1):        
        print ("正在准备爬取第%s页"%num)
        js="document.documentElement.scrollTop=4950"#下拉加载
        driver.execute_script(js)
        driver.implicitly_wait(5)
        search = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/input')#获取输入页数框
        time.sleep(4)
        try:
            search.clear()#清空内容
        except:
            search = driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/input')#获取输入页数框
            search.clear()#清空内容
        time.sleep(1)
        search.send_keys(num)
        time.sleep(3)
        spider()
        if num < endPage:#当输入页数小于终止页时可以跳转到下一页
            nextPage()
def nextPage():
        driver.find_element_by_xpath('//*[@id="mainsrp-pager"]/div/div/div/div[2]/span[3]').click()#点击确定，跳转页数

def spider():
    time.sleep(5)
    source = driver.page_source#获取网页源码
    html = etree.HTML(source)#解析源网页
    for et in html.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div'):
        names = et.xpath('./div[2]/div[2]/a/text()')
        name = (str(names)).replace(" ","").replace("'","").replace(",","").replace("[\\n\\n\\n\\n","").replace("\\n]","").replace("[\\n\\n","")
        #//   双斜杠可以表明转译符
        price = et.xpath('./div[2]/div/div/strong/text()')[0]
        try:
            sales = et.xpath('./div[2]/div[1]/div[2]/text()')[0]
        except:
            continue
        store = et.xpath('./div[2]/div[3]/div[1]/a/span[2]/text()')[0]
        w.writerow([store, name, sales, price])
        print (store, name, sales, price, '\n')
        
if __name__ == '__main__':
    scan_login()
    starPage = int(input("请输入起始页数字："))
    endPage = int(input("请输入终止页数字："))
    start(starPage,endPage)