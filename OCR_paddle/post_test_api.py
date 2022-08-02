import requests
with open('1.png','rb') as r:
    bin = r.read()
code=requests.post('http://127.0.0.1:8080/ocr',bin)
print(code.text)
