import pymysql
import requests
from lxml import etree
import re
def get_url():
    conn = pymysql.connect('localhost', 'root', '123456', 'k12')
    cursor = conn.cursor()
    cursor.execute("select url from gensheixue_delet_double")
    URL = cursor.fetchall()
    cursor.close()
    conn.close()
    url_list = list(URL)
    for url_tuple in url_list:
        url = "".join(url_tuple)
        parse_page(url)

def parse_page(url):
    cellClass = []
    # url = "https://m.genshuixue.com/mt/cellClass?cellClazzNumber=4314127469685248"
    headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Mobile Safari/537.36","authority": "m.genshuixue.com"
        }
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    # print(html)
    selector = etree.HTML(html)
    # print(selector)
    id = re.findall(r'\d+',url)[0]
    cellClass.append(id)
    teacher= selector.xpath('//div[@class = "teacher-name line-clamp"]//text()')[0]
    cellClass.append(teacher)
    print(id)
    print(teacher)
    print(cellClass)
    parm = tuple(cellClass)
    print(parm)
    conn = pymysql.connect('localhost', 'root', '123456', 'k12')
    cursor = conn.cursor()
    sql = "insert into teacher(id,姓名) values (%s,%s)"
    effect_row = cursor.execute(sql,parm)
    print(effect_row)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    get_url()