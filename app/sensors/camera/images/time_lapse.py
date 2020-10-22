from PIL import Image
import json

with open('images.json', 'r') as file_list:
    files = json.load(file_list)

images = []
size = (192, 108)

for file in files:
    image = Image.open(file)
    smaller_image = image.resize(size)

    images.append(smaller_image)

images[0].save(
    fp='2020-05-25.mp4',
    format='MP4',
    append_images=images[1:],
    save_all=True,
    optimize=True,
    duration=15,
    loop=0
)