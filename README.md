# Декораторы
**Инвариантная самостоятельная работа** 

**2.1** Разработать прототип программы «Калькулятор», позволяющую выполнять базовые арифметические действия и функцию обертку, сохраняющую название выполняемой операции, аргументы и результат в файл

> Программа «Калькулятор» - это программа, позволяющая осуществлять  конвертацию курса валюты, на основе информации ЦБР. Основа программы -  функция (класс), принимающая число (в том числе число с плавающей  точкой) и условное обозначение валюты, из которой идет преобразование и  валюты, в которую преобразовывается.
>
> Ссылка на документацию:
>
> - <https://www.cbr.ru/development/>
> - <https://www.cbr.ru/development/SXML/>
> - пример запроса: <http://www.cbr.ru/scripts/XML_daily.asp>

Для парсинга XML была выбранная библиотека **ElementTree**  

```Python
import xml.etree.ElementTree as ET

tree = ET.parse('feed.xml')
root = tree.getroot() 
```

Метод .**getroot()** используется для получения корневого элемента

Функция *converter()* принимает 3 агрумента: сумму для конвертации, валюту из которую меняем и валюту, на которую меняем. Поддерживаются следющие операции:
```
EUR -> RUB
USD -> RUB
RUB -> EUR
RUB -> USD
EUR -> USD
USD -> EUR
```
```Python
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
    ...
```

Первыми действиями программа проверяет дату в файле xml, если она не совподает с текущим числом, то происходит загрузка нового файла и перезапись его в  *feed.xml* 

Далее идёт ряд действий, зависящих от 2 и 3 аргумента:
```Python
if first == 'dollar' and second == 'rub':
      a = finder(str(my_dict.get('dollar')))
      b = a.replace(',', '.')
      res = sum*float(b)
result = ['dollar', sum, 'rub', res]
...
```

Используется дополнительная функция **finder**, которая получает в качестве аргумента ID валюты и возвращает её стоимость по отношению к рублю. Полученная стоимость имеет тип str и нуждается в его переопределении на float с заменой `','` на `'.'`
```Python
def finder(X):
  for elem in root:
    if elem.attrib.get('ID') == X:
        return(elem[4].text)
```

**2.2** Дополнение программы «Калькулятор» декоратором, сохраняющий действия, которые выполняются в файл-журнал.

Декоратор:
```Python
def deco(func):
    import datetime
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
    ...
```

В вайл записываются строчки, содержащие имя вызываемой функции, пеереданные аргументы и полученные результаты

logfile.log:
```Python
2018-12-02 18:37:59 Функция converter аргументы: (10.58, 'euro', 'dollar'),  результат: ['euro', 10.58, 'dollar', 12.045331629930788] 
2018-12-02 18:39:31 Функция converter аргументы: (10.58, 'euro', 'dollar'),  результат: ['euro', 10.58, 'dollar', 12.045331629930788]
2018-12-03 21:53:54 Функция converter аргументы: (10.58, 'euro', 'dollar'),  результат: ['euro', 10.58, 'dollar', 12.045331629930788] 
2018-12-03 21:54:02 Функция converter аргументы: (100, 'rub', 'dollar'),  результат: ['rub', 100, 'dollar', 1.503002246988359] 
2018-12-03 21:54:02 Функция converter аргументы: (90, 'rub', 'euro'),  результат: ['rub', 90, 'euro', 1.1881439079901357] 
2018-12-03 21:54:02 Функция converter аргументы: (10000, 'rubley', 'dollar'),  результат: None 
2018-12-03 21:54:02 Функция converter аргументы: (1000000, 'euro', 'rub'), результат: ['euro', 1000000, 'rub', 75748400.0] 
```

**2.3** Рефакторинг (модификация) программы с декоратором модулем *functools*

В модулее *functools* стандартной библиотеки есть функция, реализующая логику копирования внутренних атрибутов оборачиваемой функции:

```Python
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
```

**Вариативная самостоятельная работа** 
**2.4** Разработка функции-декоратора, позволяющей выполнять декорируемую функцию единожды.
```Python
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def my_function(foo, bar):
    return foo+bar

print(my_function(5, 10)) #15
print(my_function(5, 10)) #None
```

