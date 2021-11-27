#  #!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os

# 爬取目标
# url = 'https://www.mzitu.com/xinggan/page/'
url = 'https://www.mzitu.com/mm/page/'
parser = 'html.parser'
cur_path = os.getcwd() + '/'
proxy='127.0.0.1:1992'
#如果代理需要验证，只需要在前面加上用户名密码，如下所示

# proxy='username:password@124.243.226.18:8888'
proxies = {
  "http": "http://"+proxy,
  "https": "http://"+proxy,
}
proxies=None
# 设置报头，Http协议
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
    'referer': 'https://www.mzitu.com/'
    }

def update_header(referer):
    # header['referer'] = '{}'.format(referer)
    pass

# 爬取的预览页面数量
preview_page_cnt = 200
#105
#171 性感
start_page=15
for cur_page in range(start_page, int(preview_page_cnt) + 1):
    print('loading Page '+str(cur_page))
    cur_url = url + str(cur_page)
    cur_page=None
    soup=None
    for target_list in range(1,9):
        try:
            cur_page = requests.get(cur_url, headers=header,proxies=proxies,timeout=5)
            # 解析网页
            soup = BeautifulSoup(cur_page.text, parser)
            break
        except  :
            print(cur_page.text)
            print(str(target_list)+"页面 "+cur_url+" 获取失败,重试中")
        pass
    # 图片入口和文字入口取一个即可
    preview_link_list = soup.find(id='pins').find_all('a', target='_blank')[1::2]
    for link in preview_link_list:
        dir_name = link.get_text().strip().replace('?', '').replace('"', '').replace(':', '')
        link = link['href']
        soup=None
        pic_cnt=None
        for target_list in range(1,9):
            try:
                soup = BeautifulSoup(requests.get(link, headers=header,proxies=proxies,timeout=5).text, parser)
                # 获取图片数量
                pic_cnt = soup.find('div', class_='pagenavi').find_all('a')[4].get_text()
                break
            except  :
                print("页面获取失败,重试中"+str(target_list))
            pass
        # 创建目录
        pic_path = cur_path + dir_name
        if os.path.exists(pic_path):
            print(dir_name+' directory exist!')
            continue
        else:
            os.mkdir(pic_path)
        os.chdir(pic_path)  # 进入目录，开始下载
        print('loading ' + dir_name + '...')
        # 遍历获取每页图片的地址
        for pic_index in range(1, int(pic_cnt) + 1):
            pic_link = link + '/' + str(pic_index)
            pic_cnt=None
            for target_list in range(1,9):
                try:
                    cur_page = requests.get(pic_link, headers=header,proxies=proxies,timeout=5)
                    soup = BeautifulSoup(cur_page.text, parser)
                    pic_src = soup.find('div', 'main-image').find('img')['src']
                    break
                except  :
                    print("图片获取失败,重试中"+str(target_list))
                pass
            pic_name = pic_src.split('/')[-1]
            update_header(pic_src)
            f = open(pic_name, 'wb')
            for target_list in range(1,9):
                try:
                    f.write(requests.get(pic_src, headers=header,proxies=proxies,timeout=5).content)
                    break
                except  :
                    print("下载图片失败,重试中"+str(target_list))
                pass
            f.close()
        os.chdir(cur_path)  # 完成下载，退出目录
print('下载完成')