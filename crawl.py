from requests_html import HTMLSession
from urllib.parse import urlparse
import openpyxl 
import csv

session = HTMLSession()

# Lay data tu file .xlsx va luu vao 1 list
wb = openpyxl.load_workbook('/home/th-pc/crawl_data/app/DATA CRAWL.xlsx')
sheet = wb['Sheet1']
results = []
datas = []
for i in (sheet['A{}'.format(sheet.min_row):'A{}'.format(sheet.max_row)]):
     for j in i:
        all_link = (j.value)
        datas.append(all_link)
for k in datas:
    if 'http' in k:
        domain = urlparse(k).netloc
        results.append(domain)
    else:
        results.append(k)

# Crawl data 
for result in results:
    try:
        url = 'http://whois.vccloud.vn/info/'+result
        r = session.get(url)
        if r.status_code == 200:

            info_xpath = r.html.xpath('/html/body/div/div[2]/div[1]/div[1]')
            info = info_xpath[0].text.split('\n')
            infos = []
            with open('/home/th-pc/crawl_data/app/data_crawl.csv', 'a+') as myfile:
                for i in info:
                    if 'Country' in i or 'Address' in i or 'Name' in i:
                        infos.append(i)
                infos.append(result)
                infoss = []
                for q in infos:
                    q = q[q.find(':') + 1:]
                    infoss.append(q)
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(infoss)
    except Exception as e:
        with open('/home/th-pc/crawl_data/app/log.txt', 'a+') as file:
            file.write(result, e)
