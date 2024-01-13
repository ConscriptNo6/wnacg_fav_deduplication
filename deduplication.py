import requests
from lxml import etree
import re
import pymysql

# 新建一个会话
session = requests.Session()

# 请求头
headers = {
    'Cookie' : '',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
}

# 表单信息
form_data = {
    "normal": "1",
    "login_name": "",
    "login_pass": ""
    }

def login():
    login_url = 'https://wnacg.com/users-login.html'

    # post请求用以登陆账号
    result = session.post(login_url, form_data, headers = headers,)

    if re.search('', result.text):
        print('登陆成功')
    else:
        print('登陆失败')

# 网页解析
def page_parse(url):
    response = session.get(url, headers = headers,)
    root_element = etree.HTML(response.text)
    return root_element

# 获取收藏夹总页码数
def get_manga_info():
    # 请求收藏夹页面
    fav_page = page_parse('https://wnacg.com/users-users_fav.html')

    # 寻找最后一页页码
    last_page = fav_page.xpath('/html/body/div[4]/div/div[2]/div[2]/div//a[5]/text()')

    # 遍历所有页码上的说所有漫画
    for page in range(1, int(last_page[0]) + 1):
        print('第%s页'%page)
        page_result = page_parse('https://wnacg.com/users-users_fav-page-%s-c-0.html'%page)
        manga_parse = page_result.xpath('//div[@class="asTB"]')

        # print(len(manga_parse))
        for i in range(len(manga_parse)): # 若最后一页漫画不足则会报错，需要获取最后一页的漫画数量
            print('第%s个'%(i+1))
            # 添加时间
            created_time = str(manga_parse[i].xpath('.//div[2]/p[1]/span/text()')[0]) # 返回值是xpath元素
            # 漫画名，由于名称被拆分成多个字段，拼接起来太麻烦，所以舍弃名称的爬取
            # manga_name = manga_parse.xpath()
            manga_url = manga_parse[i].xpath('.//div[2]/p[2]/a[1]/@href')[0]
            manga_id = re.search(r'[0-9]{1,7}',manga_url).group() # 返回值是字符串

            # print(manga_id, created_time)
            sql = "insert into info_count(manga_id, data) values({}, '{}')".format(int(manga_id), str(created_time))
            cursor.execute(sql)
            # return manga_id, created_time

if __name__ == '__main__':
    login()
    db = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    password = '1356105591WYH.',
    database = 'nacg_fav_count',
    charset = 'utf8')
    cursor = db.cursor()
    get_manga_info()
    print('保存完毕')
    db.commit()
    cursor.close()
    db.close()