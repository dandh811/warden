import json

s = '董建军'
res = s.encode('unicode-escape')
print(res)

res2 = json.dumps(s)
print(res2)