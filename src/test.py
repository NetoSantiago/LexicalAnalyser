import re

a = "writeln (   'O ano em que voce nasceu   ');"
line = re.sub("'.*'", re.search("'.*'", a).group().replace(' ', '$'), a)
print(line)
