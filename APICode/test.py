import re
import regex

def exptest():
    str = '<html>htmlタグ</html>中間<a>aタグ</a>'
    htmltagexp = r'<("[^"]*"\|\'[^\']*\'|[^\'">])*>'
    result = regex.sub(htmltagexp, '', str)
    print(result)

if __name__  == '__main__':
    exptest()