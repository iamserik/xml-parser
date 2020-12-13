import requests
import urllib3

from lxml import objectify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://feed.inmoweb.es/?key=A61F01FD-DE62-498E-B722-23458391B4E3'

response = requests.request('GET', url, verify=False)

root = objectify.fromstring(response.text.encode('utf-8'))

parsed_data = []

def checker(obj):
    """Метод проверяет значение полученного обьекта на пустоту"""
    return False if obj == '' or not obj else True

def dict_changer(dict_obj):
    """Метод создает новый словарь из полученного словоря в 
    соответсвии со значениями. Если значение пустое то элемент 
    не включается в возвращаемый словарь"""
    new_dict = {}
    for key, val in dict_obj.items():
        if checker(val):
            new_dict[key] = val
    return new_dict

def parser(prop):
    property_obj = {}
    
    property_obj['id'] = int(prop.attrib['id'])
    property_obj['created'] = prop.fecha_alta
    property_obj['updated'] = prop.fecha_modificacion
    property_obj['reference'] = prop.referencia
    property_obj['family'] = dict_changer({'id': prop.familia.attrib['id'], 'family': prop.familia})
    property_obj['operation'] = dict_changer({'id': prop.operacion.attrib['id'], 'operation': prop.operacion})
    property_obj['state'] = dict_changer({'id': prop.estado.attrib['id'], 'state': prop.estado})
    property_obj['status_id'] = prop.status_id
    property_obj['bedrooms'] = prop.dormitorios
    property_obj['bathrooms'] = prop.banos
    property_obj['toilets'] = prop.aseos

    # location informations
    location_items = {}
    location_items['province'] = prop.localizacion.provincia
    location_items['population'] = dict_changer({'id': prop.localizacion.poblacion.attrib['id'], 'population': prop.localizacion.poblacion})
    latitude = None
    longitude = None
    if hasattr(prop.localizacion, 'latitud') and hasattr(prop.localizacion, 'longitud'): # В некоторых элементах отсутвтвуют значения широты и долготы
        location_items['latitude'] = prop.localizacion.latitud
        location_items['longitude'] = prop.localizacion.longitud
    location_items['cp'] = prop.localizacion.cp
    location_items['zone'] = prop.localizacion.zona
    location_items['country'] = prop.localizacion.pais

    property_obj['location'] = dict_changer(location_items)

    # Price
    property_obj['price'] = {'price': prop.precio, 'badge': prop.precio.attrib['divisa']}

    # sorfaces informations
    surface_items = {}
    surface_items['habitable'] = prop.superficies.habitable
    surface_items['built'] = prop.superficies.construida
    surface_items['plot'] = prop.superficies.parcela
    surface_items['kitchen'] = prop.superficies.cocina
    surface_items['salon'] = prop.superficies.salon
    surface_items['yard'] = prop.superficies.jardin
    surface_items['terrace'] = prop.superficies.terraza

    property_obj['surfaces'] = dict_changer(surface_items)

    # characteristics    
    property_obj['characteristics'] = [{'id': char.attrib['id'], 'characteristic': char} for char in prop.iter('caracteristica') if checker(char)]

    # Labels   
    property_obj['labels'] = [label for label in prop.iter('etiqueta') if checker(label)]

    # Descriptions
    descriptions = []

    for description in prop.descripciones.getchildren():
        child = {}
        child['language'] = description.attrib['idioma']
        child['title'] = description.titulo
        child['description'] = description.descripcion
        descriptions.append(child)

    property_obj['descriptions'] = descriptions

    property_obj['images'] = [image.attrib['url'] for image in prop.iter('imagen')]

    property_obj['documents'] = prop.documentos

    property_obj['links'] = [link for link in prop.iter('enlace')]

    property_obj['videos'] = prop.videos

    return dict_changer(property_obj) # Проверяем на пустоту полученных данных и если усть пустые значения то их отсекаем

def main():
    for prop in root.iter('propiedad'):
        property_obj = parser(prop) # Передаем каждый полученное имущество методе parser()
        parsed_data.append(property_obj) # Записываем полученный словарь в общий список

if __name__ == '__main__':
    main()