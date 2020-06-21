from datetime import datetime,date
import re

d0 = date(2008, 8, 18)
d1 = datetime.now().date()
delta = d1 - d0
regex = re.compile("(\d+?)d")
result = None
try:
    result = regex.match("20d").group(1)
except:
    #send await emoji expression
    pass
if result is not None:
    print(result)
print(delta.days)
