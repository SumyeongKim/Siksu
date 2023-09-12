from lxml import html
from datetime import datetime
from pytz import timezone
import re

partnames = {
    '방유석': True,
    '강정민': True,
    '김수명': True,
    '최종호': True,
    '이남진': True,
    '고범석': True,
    '노성재': True,
    '김기웅': True,
    '경동구': True,
    '이태영': True,
    '홍승준': True,
    '김지한': True,
    '강지언': True,
}

with open('mail.html', 'r', encoding='UTF8') as f:
    doc = f.read()

tree = html.fromstring(doc)
yearnow = 2023
today = datetime.now(timezone('Asia/Seoul')).date()
# today = today.replace(day=14)
titles = tree.xpath('//*[contains(@class, \'cls_col_subject\')]')
names = tree.xpath('//*[contains(@class, \'cls_col_name\')]')


parts = [(name.text, title.text) for name, title in zip(names, titles) if name.text in partnames]
pattern = r'\d+/\d+|\d+\s*월\s*\d+\s*일|~|-|\b\d{1,2}\b'
digitpat = r'\b\d{1,2}\b'

total = len(partnames)

print('today: ', today)
for (name, title) in parts:
    if not partnames[name]:
        continue
    matches = re.findall(pattern, title)
    for i in range(len(matches)):
        if '/' in matches[i]:
            date_format = "%m/%d"
            matches[i] = datetime.strptime(matches[i], date_format).date()
            matches[i] = matches[i].replace(year=yearnow)
        elif '월' in matches[i] and '일' in matches[i]:
            date_format = "%m월%d일"
            matches[i] = datetime.strptime(matches[i].replace(' ', ''), date_format).date()
            matches[i] = matches[i].replace(year=yearnow)
    i = 0
    while i < len(matches):
        if i < len(matches) - 2 and (matches[i + 1] == '~' or matches[i + 1] == '-'):
            start = matches[i]
            end = matches[i + 2]
            if isinstance(end, str) and re.match(digitpat, end):
                end = datetime(year=start.year, month=start.month,day=int(end)).date()
            if start <= today <= end:
                print(name, start, '~', end)
                print('\t' + title)
                total -= 1
                partnames[name] = False
            i += 3
        else:
            if matches[i] == today:
                print(name, today)
                print('\t' + title)
                total -= 1
                partnames[name] = False
            i += 1
print('총원  :', len(partnames))
print('열외  :', len(partnames) - total)
print('현재원:', total)