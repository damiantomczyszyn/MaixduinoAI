
import network_esp32
print(network_esp32)
print(dir(network_esp32))

from network_esp32 import wifi
print(wifi)

'''ouput
>>> <module'network_esp32' from'network_esp32.py'>
['__class__','__name__','__file__','GPIO','network','time','board_info','fm','wifi']
<class'wifi'>
MicroPython v0.5.1-140-g7bf6445e7-dirty on 2020-11-26; Sipeed_M1 with kendryte-k210
Type "help()" for more information.
>>>
'''

