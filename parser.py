import requests
import urllib3

from lxml import objectify


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'http://feed.inmoweb.es/?key=A61F01FD-DE62-498E-B722-23458391B4E3'

response = requests.request('GET', url, verify=False)

root = objectify.fromstring(response.text.encode('utf-8'))

proporties = dict()


for propiedad in root.getchildren():
    second = dict()
    pid = propiedad.get('id')

    for second_level in propiedad.getchildren():        
        third = dict()

        if second_level.tag == 'caracteristicas':
            for third_level in second_level.getchildren():
                third[third_level.get('id')] = third_level.text

        elif second_level.tag == 'descripciones':
            for third_level in second_level.getchildren():
                fourth = dict()
                desc = third_level.get('idioma') 
                for fourth_level in third_level.getchildren():
                    fourth[fourth_level.tag] = fourth_level.text
                print(desc)
                third[desc] = fourth

        elif second_level.tag == 'imagenes':
            for third_level in second_level.getchildren():
                third[third_level.get('url')] = third_level.get('principal')

        elif second_level.tag == 'enlaces':
            for third_level in second_level.getchildren():
                third[third_level.get('idioma')] = third_level.text
        
        if third:
            second[second_level.tag] = third
        else:
            second[second_level.tag] = second_level.text
    
    proporties[pid] = second

 
        









