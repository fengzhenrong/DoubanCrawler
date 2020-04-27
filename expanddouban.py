from selenium import webdriver
import time 

"""
@param:url，URL链接
@param:loadmore，是否可以点击点击加载更多按钮来显示更多内容，默认False
@param:waittime，初始加载后浏览器将等待的秒数 ，默认2秒
""" 
def getHtml(url, loadmore = False, waittime = 2):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                print('===========开始点击加载更多=============')
                next_button = browser.find_element_by_class_name("more")
                next_button.click()
                time.sleep(waittime)
            except Exception as err:
                print('错误信息：',err)
                break
    html = browser.page_source
    browser.quit()
    return html

# for test
#url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国"
#html = getHtml(url)
#print(html) 
