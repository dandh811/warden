from urllib.parse import unquote
text = '/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20201225095203.jpg'

text = unquote(text, 'utf-8')
print(text)