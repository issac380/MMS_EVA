from datetime import datetime

time1 = 12758.7348590200
time2 = 12760.237800
s1 = '2020-07-11 11:13:21'
s2 = '2020-07-11 17:04:51' # for example
FMT = '%Y-%m-%d %H:%M:%S'
tdelta = datetime.strptime(s2, '%Y-%m-%d %H:%M:%S') - datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
print(tdelta)