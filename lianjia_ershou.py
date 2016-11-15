# -*- coding: utf-8 -*-


# import packages
import urllib2
from bs4 import BeautifulSoup
import xlwt
import re


def download(url):
    print 'Downloading:', url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
    return html

# file input
file = xlwt.Workbook()
table = file.add_sheet('info', cell_overwrite_ok=True)

# get informaiton of houses
# get each page's
for page in xrange(1, 2):
    url = 'http://bj.lianjia.com/ershoufang/pg%d' % page
    html = download(url)
    soup = BeautifulSoup(html, 'html.parser')

# search 30 times of the block of the house
    div = soup.find_all(attrs={'class': 'info clear'}, limit=30)
    for detail in div:

        # get the number of the rows
        row = (div.index(detail)) + (page - 1) * 30

        # title information
        title = detail.find(attrs={'class': 'title'}).text
        table.write(row, 0, title)

        # house information
        houseInfo = detail.find(attrs={'class': 'houseInfo'}).text
        try:
            houseInfo_1, houseInfo_2, houseInfo_3, houseInfo_4, houseInfo_5, houseInfo_6 = houseInfo.split(
                '|', 5)
            table.write(row, 1, houseInfo_1)
            table.write(row, 2, houseInfo_2)
            table.write(row, 3, houseInfo_3)
            table.write(row, 4, houseInfo_4)
            table.write(row, 5, houseInfo_5)
            table.write(row, 6, houseInfo_6)
        except:
            houseInfo_1, houseInfo_2, houseInfo_3, houseInfo_4, houseInfo_5 = houseInfo.split(
                '|', 4)
            table.write(row, 1, houseInfo_1)
            table.write(row, 2, houseInfo_2)
            table.write(row, 3, houseInfo_3)
            table.write(row, 4, houseInfo_4)
            table.write(row, 5, houseInfo_5)

        # position information
        positionInfo = detail.find(attrs={'class': 'positionInfo'}).text
        # print positionInfo
        p1 = re.split(r'[;,\s]\s*', positionInfo)[1]
        p2 = re.split(r'[;,\s]\s*', positionInfo)[2]
        p3 = re.split(r'[;,\s]\s*', positionInfo)[4]
        table.write(row, 7, p1)
        table.write(row, 8, p2)
        table.write(row, 9, p3)

        # subway information
        if not detail.find(attrs={'class': 'subway'}) is None:
            subway = detail.find(attrs={'class': 'subway'}).text
            # print subway
            table.write(row, 10, subway)

        # tax free information
        if not detail.find(attrs={'class': 'taxfree'}) is None:
            tax_free = detail.find(attrs={'class': 'taxfree'}).text
            table.write(row, 11, tax_free)

        # total price
        totalPrice = detail.find(attrs={'class': 'totalPrice'}).text
        table.write(row, 12, totalPrice)

        # unit price
        UnitPrice = detail.find(attrs={'class': 'unitPrice'}).text
        table.write(row, 13, UnitPrice)

        # print("----------------------------------------------------------")
    print 'No.', page, 'page is got'

file.save('lianjia_ershou_info.xls')
