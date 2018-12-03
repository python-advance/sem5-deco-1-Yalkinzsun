import xml.etree.ElementTree as ET

tree = ET.parse('feed.xml')
root = tree.getroot()


def finder(X):
  for elem in root:
    if elem.attrib.get('ID') == X:
        return(elem[4].text)

def deco(func):
    import datetime
    import functools
    @functools.wraps(func)
    def wrap_log(*args, **kwargs):
        a = str("{0:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()))
        b = str(args)
        c = str(func(*args, **kwargs))
        log =  f'{a} Функция ' + func.__name__ + f' аргументы: {b},  результат: {c} \n'
        with open('logfile.log', 'a', encoding='utf-8') as file:
            file.write(log)
        return func(*args, **kwargs)
    return wrap_log

@deco
def converter(sum, first, second):
    my_dict = {
       'euro': "R01239",
       'dollar':"R01235"
    }
    import datetime
    today = datetime.datetime.today()
    if root.get('Date') != today.strftime("%d.%m.%Y"):
        import requests, datetime
        URL = "http://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(URL)
        with open('feed.xml', 'wb') as file:
            file.write(response.content)

    if first == 'dollar' and second == 'rub':
      a = finder(str(my_dict.get('dollar')))
      b = a.replace(',', '.')
      res = sum*float(b)
      result = ['dollar', sum, 'rub', res]

    elif first == 'euro' and second == 'rub':
      a = finder(str(my_dict.get('euro')))
      b = a.replace(',', '.')
      res = sum * float(b)
      result = ['euro', sum, 'rub', res]

    elif first == 'rub' and second == 'dollar':
      a = finder(str(my_dict.get('dollar')))
      b = a.replace(',', '.')
      res = sum * (1/float(b))
      result = ['rub', sum, 'dollar', res]

    elif first == 'rub' and second == 'euro':
      a = finder(str(my_dict.get('euro')))
      b = a.replace(',', '.')
      res = sum * (1 / float(b))
      result = ['rub', sum, 'euro', res]

    elif first == 'dollar' and second == 'euro':
      a = finder(str(my_dict.get('dollar')))
      a1 = finder(str(my_dict.get('euro')))
      b = a.replace(',', '.')
      b1 = a1.replace(',', '.')
      res = (sum * (float(b)))* 1/(float(b1))
      result = ['dollar', sum, 'euro', res]

    elif first == 'euro' and second == 'dollar':
      a = finder(str(my_dict.get('euro')))
      a1 = finder(str(my_dict.get('dollar')))
      b = a.replace(',', '.')
      b1 = a1.replace(',', '.')
      res = (sum * (float(b))) * 1 / (float(b1))
      result = ['euro', sum, 'dollar', res]

    else:
       result = None
    return result


if __name__ == "__main__":
  print(converter(10.58,'euro', 'dollar'))
  print(converter(100, 'rub', 'dollar'))
  print(converter(90, 'rub', 'euro'))
  print(converter(10000, 'rubley', 'dollar'))
  print(converter(1000000, 'euro', 'rub'))





