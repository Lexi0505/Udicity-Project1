#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'pangxia'
from bs4 import BeautifulSoup
import expanddouban
import csv
import codecs


def getMovieUrl(category, location):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}'.format(category,location)
    return url


class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def print_data(self):
        return "{}, {}, {}, {}, {}, {}".format(self.name,self.rate,self.location,self.category,self.info_link,self.cover_link)

class MoviesCategory:
    def __init__(self,category,movies):
        self.category  = category
        self.movies = movies

def getLocations():
    html = expanddouban.getHtml('https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影')
    soup = BeautifulSoup(html, 'html.parser')
    locationList=[]
    for child in soup.find(class_='tags').find(class_='category').next_sibling.next_sibling:
        location = child.find(class_='tag').get_text()
        if location != '全部地区':
            locationList.append(location)
    return locationList

def getMovies(category,location):
    movies = []
    for l in location:
        html = expanddouban.getHtml(getMovieUrl(category,l),True)
        soup = BeautifulSoup(html, 'html.parser')
        html_a = soup.find(id='content').find(class_='list-wp').find_all('a', recursive=False)
        for element in html_a:
            M_name = element.find(class_='title').string
            M_rate = element.find(class_='rate').string
            M_location = l
            M_category = category
            M_info_link = element.get('href')
            M_cover_link = element.find('img').get('src')
            movies.append([M_name,M_rate,M_location,M_category,M_info_link,M_cover_link])
    return movies

movie_location = getLocations()
movie_category = ['喜剧', '动作', '科幻']
datas = []
mclist = []
for c in movie_category:
    datas.append(getMovies(c, movie_location))
    mclist.append(MoviesCategory(c,datas[len(datas)-1]))
with codecs.open('movies.csv','w','utf_8_sig') as f:
    writer = csv.writer(f)
    for data in datas:
        writer.writerows(data)

#使用dict key去方式统计地区可以方便去重复，value则为该地区某类型影片数；
#对dict按照value进行排序，取前三个即可。
ld = []
for d in datas:
    count = {}
    for m in d:
        if m[2] in count:
            count[m[2]] += 1
        else:
            count[m[2]] = 1
    sortedcount = sorted(count.items(), key=lambda e:e[1], reverse=True)
    ld.append(sortedcount)

i = 0
with open('output.txt', 'w', encoding='utf-8') as fout:
    for item in ld:
        mcount = 0
        for k in item:
            mcount += k[1]
        if len(item) >= 3:
            print('{}电影前三名及比例:{} {}%, {} {}%, {} {}%'.format(movie_category[i], item[0][0], (item[0][1] / mcount * 100), item[1][0],
                                                     (item[1][1] / mcount * 100), item[2][0], (item[2][1] / mcount * 100)),file=fout)
        if len(item) == 2:
            print('{}电影前三名及比例:{} {}%,{} {}%'.format(movie_category[i], item[0][0], (item[0][1] / mcount * 100), item[1][0],
                                                (item[1][1] / mcount * 100)), file=fout)
        if len(item) == 1:
            print('{}电影前三名及比例:{} {}%'.format(movie_category[i], item[0][0], (item[0][1] / mcount * 100)), file=fout)
        i+=1
