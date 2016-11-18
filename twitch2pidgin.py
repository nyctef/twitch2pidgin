from bs4 import BeautifulSoup
from PIL import Image
import requests
from pprint import pprint
from collections import namedtuple
from io import BytesIO

Emote = namedtuple('Emote', ['name', 'url'])

def parse_image(element):
    name = element.text
    url = element.find('img')['src']
    return Emote(name, url)

def scrape_images(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = list(map(parse_image, soup.find_all('center')))
    return images

def dump_images(images):
    output_folder = 'output'
    theme = []
    for image in images:
        out_filename = '{}/{}.png'.format(output_folder, image.name)
        print('downloading {} from {} to {}'.format(image.name, image.url, out_filename))
        r = requests.get(image.url)
        img = Image.open(BytesIO(r.content))
        img.thumbnail((40,40), Image.ANTIALIAS)
        img.save(out_filename)
        theme.append('! {0}.png {0} :{0}: {1} :{1}:'.format(image.name, image.name.lower()))

    out_themefile = output_folder+'/theme'
    print('writing theme file to {}'.format(out_themefile))
    with open(out_themefile, 'w') as themeFile:
        themeFile.write('\n'.join(theme))

def do_everything(url):
    images = scrape_images(url)
    dump_images(images)

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        print('usage: python twitch2pidgin.py [channel name]')
        exit(1)
    url = 'https://twitchemotes.com/channel/' + argv[1]
    do_everything(url)
