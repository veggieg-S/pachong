import requests
import pandas as pd
from lxml import etree
import re
import pymysql


def parse_page(url):
    id_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    selector = etree.HTML(html)
    params = selector.xpath('//div[@class = "card-course-content"]/div/@data-habo-params')
    for i in params:
        # print(i)
        id = re.findall(r'\d+', i)[1]
        id_list.append(id)
    print(id_list)

    k = len(id_list)
    category_j = selector.xpath('//span[contains(@data-type,"category") and contains(@class,"selected")]//text()')[0]
    print(category_j)
    category_i = category_j.split(",")*k
    print(category_i)
    grade_j = selector.xpath('//span[contains(@data-type,"grade") and contains(@class,"selected")]//text()')[0]
    print(grade_j)
    grade_i = grade_j.split(",")*k
    print(grade_i)

    subject_i = selector.xpath('//div[@class = "header"]//text()')
    print(subject_i)
    course_i = selector.xpath('//p[@class = "course-name"]//text()')
    print(course_i)
    date_i = selector.xpath('//p[@class = "arrangement"]//text()')
    print(date_i)
    pay_i = selector.xpath('//span[@class = "pay-count"]//text()')
    print(pay_i)
    free_list = selector.xpath('//button[@class = "free-buy"]//text()')
    price_list =selector.xpath('//span[@class = "price"]//text()')[1::2]
    price_i = free_list+price_list
    print(price_i)
    multi_list = map(list, zip(id_list, category_i, grade_i,subject_i,course_i,date_i,pay_i,price_i))
    print(multi_list)

    for j in multi_list:
        print(j)
        parm = tuple(j)
        conn = pymysql.connect('localhost', 'root', '123456', 'k12')
        cursor = conn.cursor()
        sql = "insert into gensheixue(课程ID,类别,年级,科目,课程名,开课日期,报名情况,学费) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        effect_row = cursor.execute(sql,parm)
        print(effect_row)
        conn.commit()
        cursor.close()
        conn.close()
def get_url():
    url_list = []
    URL = "https://www.genshuixue.com/pc/courseCenter?course=all&subjectId=0&gradeId={1}&categoryId={0}"
    categoryidList = [5,10,15,25,60,55,40]
    gradeId_1 = [100,110,120,130,140,150]
    gradeId_2 = [200,210,220]
    gradeId_3 = [300,310,320]
    gradeId_4 = [500,520]
    gradeId_5 = [974,976,978]
    gradeId_6 = [966,968]
    gradeId_7 = [810,820,830,840]
    gradeIdList = [gradeId_1,gradeId_2,gradeId_3,gradeId_4,gradeId_5,gradeId_6,gradeId_7]
    for i in range(0,7):
        for j in range(len(gradeIdList[i])):
            url1 = URL.format(categoryidList[i],gradeIdList[i][j])
            url_list.append(url1)
    for url in url_list:
        parse_page(url)


if __name__ == '__main__':
    get_url()