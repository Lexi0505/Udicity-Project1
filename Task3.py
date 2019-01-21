import csv
import re
with open('calls.csv', 'r') as f:
    reader = csv.reader(f)
    calls = list(reader)
area_codes = []
mobile_prefixs = []
telemarketers = []
temp = []
sum_nums = []

for call in calls:
    if call[0].startswith('(080)'):
        if call[1].startswith('(0'):
            # p = re.compile('[(](.*?)[)]',re.S)
            # area_codes.append(re.findall(p,call[1]))
            area_codes.append(call[1].split('(')[1].split(')')[0])
        if call[1].startswith('7') or call[1].startswith('8') or call[1].startswith('9'):
            mobile_prefixs.append(call[1].split()[0])
        if call[1].startswith('140'):
            telemarketers.append(call[1])

sum_nums =area_codes + mobile_prefixs + telemarketers
print('The numbers called by people in Bangalore have codes:')
print('\n'.join(sorted(list(set(sum_nums)))))


for area_code in area_codes:
    if area_code.startswith('080'):
        temp.append(area_code)
print('{} percent of calls from fixed lines in Bangalore are calls to other fixed lines in Bangalore.'.format(round(float(len(temp))/float(len(sum_nums)),4)*100))
print(len(temp))
print(len(sum_nums))
