import requests
#import climage
from PIL import Image


API = 'https://pokeapi.co/api/v2'


class Pokemon:
    def __init__(self, name, height, weight, types, image):
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.image = image

    def __repr__(self):
        return (f'{self.__class__.__name__}('
            f'{self.name!r}, {self.height!r}, ' 
            f'{self.weight!r}, {self.types!r})')


def show_image(img):
    #output = climage.convert(self.image, width=100)
    #print(output)
    im = Image.open(img)
    im.show()

                
def get_pokemon(name):
    request = f'{API}/pokemon/{name}'
    response = requests.get(request)
    
    # status code was between 200 and 400
    if response:
        content = response.json()

        height = content['height']
        weight = content['weight']
        types = [ data['type']['name'] for data in content['types'] ]
        image = f'{name}.png'
        image_url = content['sprites']['other']['home']['front_default']
        response_img = requests.get(image_url) 
        
        with open(image, 'wb') as file:
            file.write(response_img.content)

        pokemon = Pokemon(name, height, weight, types, image)
        return pokemon



if __name__ == '__main__':
    name = input('Pokemon search: ').lower()
    pokemon = get_pokemon(name)
    if pokemon:
        print(f'INFO ABOUT: {pokemon.name}')
        print(f'height: {pokemon.height}')
        print(f'weight: {pokemon.weight}')
        print(f'types: {pokemon.types}')
        show_image(pokemon.image)
    
    else:
        print(f'Cannot find {name}')
    input()