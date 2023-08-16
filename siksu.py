from lxml import html
from datetime import datetime
from pytz import timezone
import re

partnames = {
    '방유석',
    '강정민',
    '김수명',
    '최종호',
    '이남진',
    '고범석',
    '노성재',
    '김기웅',
    '경동구',
    '이태영',
    '홍승준',
    '김지한',
    '강지언'
}

with open('mail.html', 'r', encoding='UTF8') as f:
    doc = f.read()

tree = html.fromstring(doc)
yearnow = 2023
today = datetime.now(timezone('Asia/Seoul')).date()
# today = today.replace(day=14)
titles = tree.xpath('//*[contains(@class, \'cls_col_subject\')]')
names = tree.xpath('//*[contains(@class, \'cls_col_name\')]')


parts = [(name.text, title.text) for name, title in zip(names, titles) if name.text in partnames ]
pattern = r'\d+/\d+|\d.*월.*\d.*일|~|-'

total = len(partnames)

print('today: ', today)
for (name, title) in parts:
    matches = re.findall(pattern, title)
    for i in range(len(matches)):
        if '/' in matches[i]:
            date_format = "%m/%d"
            matches[i] = datetime.strptime(matches[i], date_format).date()
            matches[i] = matches[i].replace(year=yearnow)
            total -= 1
        elif '월' in matches[i]:
            date_format = "%m월%d일"
            matches[i] = datetime.strptime(matches[i].replace(' ', ''), date_format).date()
            matches[i] = matches[i].replace(year=yearnow)
    i = 0
    while i < len(matches):
        if i < len(matches) - 2 and (matches[i + 1] == '~' or matches[i + 1] == '-'):
            start = matches[i]
            end = matches[i + 2]
            if start <= today <= end:
                print(name, start, '~', end)
                print('\t' + title)
            i += 3
        else:
            if matches[i] == today:
                print(name, today)
                print('\t' + title)
            i += 1