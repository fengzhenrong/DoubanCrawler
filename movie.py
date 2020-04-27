
import requests
from bs4 import BeautifulSoup
import expanddouban
import urllib.parse
import os
import pandas as pd

#豆瓣电影类
class DouBan_Movie():

    def __init__(self):
        # 因为查询的电影数量太多，本例子只刷选评分（9，10）的电影
        self.url = "https://movie.douban.com/tag/#/?sort=S&range=9,10"
    
    '''
    重新组合电影请求url链接
    @param:categoryname, 电影类别名称
    @param:locationname, 电影地区名称
    @return, 返回拼接后URL

    '''
    def getQueryUrl(self, categoryname, locationname):
        # 只刷选电影的信息
        params = ['电影', categoryname, locationname]
        # 把数组转成字符串，用逗号分割
        params_str = ','.join(params)
        
        # 定义参数字典
        params_data = {
            "tags": params_str
        }

        # url不识别中文，将参数专业进行编码转换
        query_string = urllib.parse.urlencode(params_data)

        return self.url + '&' + query_string
        

    
    '''
    获取电影类型数组
    @param:categorylist, 类别数组
    @param:tagname, html标签
    @param:start, 获取的tag数组的开始索引
    @return，返回数组

    '''
    def getMovieCategory(self, categorylist, tagname, start):
        taglist = [] # 空列表
        if categorylist:
            soup = BeautifulSoup(categorylist, "html.parser")
            htmllist = soup.find_all(tagname)[start:]
            for tag in htmllist:
                taglist.append(tag.text)
            
        else:
            print("category数组为空")
        print("taglist:",taglist)
        return taglist
    
    '''
    获取电影信息
    @param:category, 电影类型
    @param:location, 电影地区
    @return，返回多维数组,格式为：[[1, 2, 3, 4], ['a', 'b', 'c', 'd']]
    '''
    def getMovieInfo(self, category, location):
        #电影名称
        name = ''
        #电影评分
        rate = 0
        #电影url链接
        info_link = ''
        #电影图片地址
        cover_link = '' 

        # 获取新请求地址
        newurl = self.getQueryUrl(category, location)
        # 通过expanddouban函数请求网页,需要加载更多
        moviehtml = expanddouban.getHtml(newurl, loadmore = True)
        # 定义返回数组
        movie_datas = []
        if moviehtml:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(moviehtml, "html.parser")
            # 电影信息都在class为list-wp的div里面
            movie_container = soup.find(class_="list-wp")
            # 查找所有a标签的电影信息
            movie_list = movie_container.find_all("a")
            # 遍历a标签数组;
            # 电影名称在class为title的标签里
            # 电影评分在class为rate的标签里
            # 电影url链接直接在a标签的herf获取
            # 电影图片地址在img标签里
            for movieinfo in movie_list:
                # 电影名称
                name = movieinfo.find(class_="title").text
                # 电影评分
                rate = movieinfo.find(class_="rate").text
                # 电影url链接
                info_link = movieinfo.get("href")
                # 电影图片地址
                cover_link = movieinfo.find("img").get("src")

                # 添加到列表数组
                movie_datas.append([name, rate, category, location, info_link, cover_link])


        else:
            print("请求电影url出错")
        
        return movie_datas
    

    '''
    把电影信息保存为CSV文本
    @param:datas, 电影信息数组
    '''
    def saveToCSV(self, datas):
        # 定义电影文件名称
        filepath = 'movice.csv'
        # 定义列标题
        columns = ['name', 'rate', 'category', 'location', 'info_link', 'cover_link']
        # 判断该目录下是否存在文件，没有就创建一个空文件,不要将索引写入index = False
        if not os.path.exists(filepath):
            if datas:
                # 添加的数据保存到movice.csv文件下
                pf_default = pd.DataFrame(data = datas, columns = columns)
                pf_default.to_csv(filepath, index=False)
        else:
            if datas:
                # 读取电影文件数据
                pf_data = pd.read_csv(filepath)
                # 定义需要添加的电影数据
                pf_add = pd.DataFrame(data = datas, columns = columns)

                # 添加新数据到电影文件里面
                # pf_new = pd.concat([pf_data,pf_add])
                pf_new = pf_data.append(pf_add, ignore_index=True)

                # 添加的数据保存到movice.csv文件下
                pf_new.to_csv(filepath, index=False)
            
            
        
        
        


    '''
    处理逻辑
    '''
    def run(self):
        # 通过expanddouban函数请求网页，不需要加载更多
        html = expanddouban.getHtml(self.url, loadmore = False)
        # print("html:",html)
        if html:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(html, "html.parser")

            # 查找所有的category
            htmllist = soup.find_all(class_="category")
            # 豆瓣的类别有形式，类型，地区，年代，特色，这里我只需要类型跟地区就可以
            # 这里我们定义一个查找电影类别的函数，方便抓取不同类别
            # 可以通过list[0:1]方式截取，截取后需要把数组转为字符串

            # 电影类型
            type_list = self.getMovieCategory(str(htmllist[1:2]), "span", 1)

            # 地区
            location_list = self.getMovieCategory(str(htmllist[2:3]), "span", 1)

            # 遍历电影类型
            for category in type_list:
                for location in location_list:
                    # 获取电影不同电影类型，地区的电影数据
                    datas = self.getMovieInfo(category, location)

                    # 保存电影数据
                    self.saveToCSV(datas)
            print("=============done==============")
                    
            

            # 获取电影不同电影类型，地区的电影数据
            # datas = self.getMovieInfo('剧情', '中国大陆')

            # 保存电影数据
            # self.saveToCSV(datas)
            
            # print(datas)
            
            # 获取电影信息
            # self.getMovieInfo(type_list, location_list)


        else:
            print("html出错")


if __name__ == "__main__":
    movie = DouBan_Movie()
    movie.run()




