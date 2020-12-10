import requests
import urllib3

from lxml import objectify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://feed.inmoweb.es/?key=A61F01FD-DE62-498E-B722-23458391B4E3'

response = requests.request('GET', url, verify=False)

root = objectify.fromstring(response.text.encode('utf-8'))

parsed_data = []


def subelements_parser(obj):
    ''' Parsing any objectify element '''
    obj_items = {}

    if obj.countchildren() or obj.keys():
        sub_element = []
        if obj.keys(): 
            sub_element.append(obj.items())

        if obj.countchildren():
            for item in obj.getchildren(): 
                if item != '' or item.tag == 'imagen': # Проверяем на пустоту и если тег image тоже выполняем код 
                    sub_element.append(subelements_parser(item)) # Если обьект имеет поддерево то вызываем рекурсивно этот же метод
        else:
            sub_element.append(obj)

        obj_items[obj.tag] = sub_element

    else:
        obj_items[obj.tag] = obj.text

    return obj_items



def parser(root):
    for property_obj in root.propiedad:
        item = subelements_parser(property_obj) # Передаем каждое имущество методу
        parsed_data.append(item)


if __name__ == '__main__':
    parser(root)