import re

a = 'a := 5'
x = re.search('(\d)+', a)
print(x.group())
