import os
def read(path):
    f = open(path,'r',encoding='utf-8')
    print(f.read())
    f.close()
    