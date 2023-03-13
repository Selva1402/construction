import binascii
from PIL import Image


hex_string = "0x706578656C732D6D656E7461746467742D313034393632322E6A7067"
decoded_string = binascii.unhexlify(hex_string[2:]).decode('utf-8')
img = Image.open('/static/images/pexels-mentatdgt-1049622.jpg')

img.show()

