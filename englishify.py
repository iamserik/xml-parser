
words = {
    'propiedad': 'property',

    'id': 'id', 
    'fecha_alta': 'created',
    'fecha_modificacion': 'updated', 
    'referencia': 'reference', 
    'familia': 'family', 
    'operacion': 'operation', 
    'estago': 'state', 
    'status_id': 'status_id', 
    'dormitorios': 'bedrooms', 
    'banos': 'bathrooms',
    'aseos': 'toilets', 
    
    'localizacion': 'location', 
    'provincia': 'province', 
    'poblacion': 'population', 
    'latitud': 'latitude', 
    'longitud': 'longitude', 
    'cp': 'cp', 
    'zona': 'zone', 
    'pais': 'country', 

    'precio': 'price',
    'divisa': 'badge', 
    'habitable': 'habitable', 
    'construida': 'built', 
    'parcela': 'plot', 
    'cocina': 'kitchen', 
    'salon': 'salon', 
    'jardin': 'yard', 
    'terraza': 'terrace', 
    'superficies': 'surfaces', 
    'caracteristicas': 'characteristics',
    'caracteristica': 'characteristic',
    'etiquetas': 'labels',
    'etiqueta': 'label',
    'idioma': 'language',
    'titulo': 'title',
    'descripcion': 'description',
    'descripciones': 'descriptiones',
    'imagenes': 'images',
    'imagen': 'image',
    'documentos': 'documents',
    'enlaces': 'links',
    'enlace': 'link',
    'videos': 'videos',
    'video': 'video',
    'tipo': 'type',
    'url': 'url',

    }

def translator(w):
    """
    Translate spanish to english
    """
    return words[w]