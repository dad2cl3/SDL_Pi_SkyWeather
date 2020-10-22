import argparse, pigpio, sys
from asyncio import sleep

import RPi.GPIO as GPIO
# set GPIO mode
GPIO.setmode(GPIO.BCM)

# append additional paths

# Dust sensor class
from SDL_Pi_DustSensor import SDL_Pi_DustSensor
# TODO: Push these back to the configuration file
# TODO: Determine if these should be added to the class
# Set the sensor pin constant
SENSOR_PIN = 19
# Set the power pin constant
POWER_PIN = 26
# Set the sensor
SENSOR_NAME = 'Dust sensor'


async def power_on_sensor():
    # print('Powering on dust sensor...')
    # print('Setting power pin...')
    GPIO.setup(POWER_PIN, GPIO.OUT)
    # print('Turning on power...')
    GPIO.output(POWER_PIN, True)
    # print('Pausing for sensor to power on...')
    await sleep(1)
    # print('Continuing...')


async def power_off_sensor():
    # print('Powering off dust sensor...')
    GPIO.setup(POWER_PIN, GPIO.OUT)
    GPIO.output(POWER_PIN, False)
    await sleep(1)


'''
def test_sensor():
    return 'something'
'''


async def read_sensor():
    # power on the sensor
    await power_on_sensor()
    print('Dust sensor powered on...')
    # connect to the RPi
    print('PiGPIO...')
    pi = pigpio.pi()
    # initialize dust sensor
    print('Initializing the sensor...')
    dust = SDL_Pi_DustSensor(pi=pi, gpio=SENSOR_PIN)
    # pause for 30s to properly calibrate reading
    print('Calibrating the sensor...')
    await sleep(30)

    # sample gpio, ratio, and particle concentration per 0.01 cubic feet
    print('Reading the sensor...')
    g, r, c = dust.read()

    if c >= 1080000.00:
        reading = {
            'sensor': 'dust',
            'status': 'error'
        }
    else:
        # convert particle concentration to SI units
        c_ugm3 = dust.pcs_to_ugm3(c)
        # convert particle concentration to US AQI units
        c_aqi = dust.ugm3_to_aqi(c_ugm3)

        '''reading = {
            'sensor': 'dust',
            'status': 'success',
            'gpio': g,
            'ratio': r,
            'concentration': {
                'sqft': c,
                'squgm': c_ugm3,
                'aqi': c_aqi
            }
        }'''
        reading = {
            'sensor': SENSOR_NAME,
            'status': 'success',
            'reading': {
                'gpio': g,
                'ratio': r,
                'concentration': {
                    'sqft': c,
                    'squgm': c_ugm3,
                    'aqi': c_aqi
                }
            }
        }

    # stop the connection to the RPi
    pi.stop()
    # pause to allow connection to stop
    await sleep(5)
    # power off the sensor
    await power_off_sensor()

    del dust
    return reading

'''parser = argparse.ArgumentParser()
parser.add_argument('--mode')
args = parser.parse_args()
mode = args.mode

if args.mode == 'test':
    test_sensor()
elif args.mode == 'read':
    response = read_sensor()'''

#print(response)