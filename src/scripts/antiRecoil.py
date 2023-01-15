import time

import pydirectinput

verticalStrength = 15
horizontalStrength = 10

time.sleep(5)

for x in range(50):
    pydirectinput.moveRel(-horizontalStrength, verticalStrength)
    time.sleep(0.03)

