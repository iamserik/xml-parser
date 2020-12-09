import requests
import urllib3

from lxml import objectify

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://feed.inmoweb.es/?key=A61F01FD-DE62-498E-B722-23458391B4E3'

response = requests.request('GET', url, verify=False)

root = objectify.fromstring(response.text.encode('utf-8'))

parsed_data = []

def checker(dicton):
    for key, val in dicton.items():
        if val == '':
            return False
    return True


def another(root):
    for prop in root.getchildren():
        property_obj = []
                                                        # for parsed list
        property_id = {'id': prop.attrib['id']}
        created = {'created': prop.fecha_alta}
        updated = {'updated': prop.fecha_modificacion}
        reference = {'reference': prop.referencia}
        family = {'family': prop.familia.attrib['id'], 'family': prop.familia} 
        operation = {'operation': prop.operacion.attrib['id'], 'operation': prop.operacion}
        state = {'state': prop.estado.attrib['id'], 'state': prop.estado}
        status_id = {'status_id': prop.status_id}
        bedrooms = {'bedrooms':  prop.dormitorios}
        bathrooms = {'bathrooms': prop.banos}
        toilets = {'toilets': prop.aseos}

        property_obj = [item for item in [property_id, created, updated, reference, family, operation, state, status_id, bedrooms, bathrooms, toilets] if checker(item)]

        # location informations
        province = {'province': prop.localizacion.provincia}
        population = {'population_id': prop.localizacion.poblacion.attrib['id'], 'population': prop.localizacion.poblacion}
        # latitude = {'latitude': prop.localizacion.latitud}
        # longitude = {'longitude': prop.localizacion.longitud}
        cp = {'cp': prop.localizacion.cp}
        zone = {'zone': prop.localizacion.zona}
        country = {'country': prop.localizacion.pais}

        location = [item for item in [province, population, cp, zone, country] if checker(item)] # for parsed list
        property_obj.append(location)

        # Price
        price = {'price': prop.precio, 'badge': prop.precio.attrib['divisa']}
        property_obj.append(price)

        # sorfaces informations
        habitable = {'habitable' : prop.superficies.habitable}
        built = {'built': prop.superficies.construida}
        plot = {'plot': prop.superficies.parcela}
        kitchen = {'kitchen': prop.superficies.cocina}
        salon = {'salon': prop.superficies.salon}
        yard = {'yard': prop.superficies.jardin}
        terrace = {'terrace': prop.superficies.terraza}

        surfaces = [itm for itm in [habitable, built, plot, kitchen, salon, yard, terrace] if checker(itm)] # for parsed list
        property_obj.append(surfaces)

        # characteristics
        characteristics = [] # for parsed list

        for char in prop.iter('caracteristica'):
            child = {}
            if char != '':
                child['char_id'] = char.attrib['id']
                child['char'] = char
                characteristics.append(child)
        
        property_obj.append(characteristics)

        # Labels
        labels = [] # for parsed list

        for label in prop.iter('etiqueta'):
            labels.append({'label': label})
        
        property_obj.append(labels)

        # Descriptions
        descriptions = [] # for parsed list

        for description in prop.descripciones.getchildren():
            child = {}
            language = description.attrib['idioma']
            child['language'] = language
            child['title'] = description.titulo
            child['description'] = description.descripcion
            descriptions.append(child)

        property_obj.append(descriptions)


        images = [] # for parsed list

        for img in prop.iter('imagen'):
            images.append({'url': img.attrib['url'], 'principal': img.attrib['principal']})

        property_obj.append(images)        

        documents = prop.documentos # for parsed list

        links = [] # for parsed list

        for link in prop.iter('enlace'):
            links.append({'language': link.attrib['idioma'], 'link': link})

        property_obj.append(links)        

        videos = prop.videos # for parsed list

        parsed_data.append(property_obj)