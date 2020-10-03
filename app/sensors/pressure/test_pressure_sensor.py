import asyncio, os, sys, time

sys.path.append(os.path.abspath('../i2c_mux'))
sys.path.append(os.path.abspath('../lightning'))
print(sys.path)

import SDL_Pi_TCA9545
import lightning_sensor

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

i2c_mux = SDL_Pi_TCA9545.SDL_Pi_TCA9545(SDL_Pi_TCA9545.TCA9545_CONFIG_BUS[0])
sensor = loop.run_until_complete(lightning_sensor.initialize(i2c_mux))

print('Initialized lightning sensor...')
# print(sensor)
while True:
    # continuously monitor lightning detector
    # await asyncio.sleep(10)
    print('Reading lightning sensor...') # debug
    reading = loop.run_until_complete(lightning_sensor.read_sensor(sensor, i2c_mux))
    print(reading)
    time.sleep(10)

