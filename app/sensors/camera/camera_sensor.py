import io, json, os, picamera
# from asyncio import sleep
from PIL import Image
from datetime import datetime


with open('{0}/{1}'.format(os.path.dirname(__file__), 'camera_config.json'), 'r') as config_file:
    config = json.load(config_file)

file_folder = config['directory']


async def capture():
    stream = io.BytesIO()
    try:
        with picamera.PiCamera() as picam:
            picam.rotation = 180
            picam.resolution = (1920, 1080)

            picam.capture(stream, format=config['file_format'])
            # reset the stream to the beginning of the image
            stream.seek(0)
            # create the pillow image from the stream
            image = Image.open(stream)
            file_name = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            full_file_name = '{0}/{1}.{2}'.format(file_folder, file_name, config['file_format'])

            # write file to disk
            image.save(
                fp=full_file_name,
                format=config['file_format']
            )

            response = {
                'sensor': 'camera',
                'status': 'success',
                'reading': {
                    'file_name': full_file_name
                }
            }

            return response
    except:
        # TODO: make this more robust
        response = {
            'sensor': 'camera',
            'status': 'error'
        }

        return response
