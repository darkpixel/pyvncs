import io, sys, pyautogui
from PIL import Image
from lib import log

if sys.platform == "linux" or sys.platform == "linux2":
    log.debug("ImageGrab: running on Linux")
    from Xlib import display, X
    # take screen images, that's not the best way, so here
    # we use directly use xlib to take the screenshot.
    class ImageGrab():
        @staticmethod
        def grab():
            dsp = display.Display()
            root = dsp.screen().root
            geom = root.get_geometry()
            w = geom.width
            h = geom.height
            raw = root.get_image(0, 0, w ,h, X.ZPixmap, 0xffffffff)
            image = Image.frombytes("RGB", (w, h), raw.data, "raw", "BGRX")
            return image

elif sys.platform == "darwin":
    log.debug("ImageGrab: running on darwin")
    
    class ImageGrab():
        @staticmethod
        def grab():
            # Take a screenshot using PyAutoGUI
            screenshot = pyautogui.screenshot()

            # Reduce the size of the image while maintaining the aspect ratio
            width, height = screenshot.size
            screenshot = screenshot.resize((width, height))

            # Convert the image to RGBX format and return it as a JPEG-encoded byte stream
            img = screenshot.convert("RGB")
            with io.BytesIO() as output:
                img.save(output, format="JPEG", quality=20)
                output.seek(0)
                return Image.open(output)


else:
    log.debug("ImageGrab: running on Unknown!")
    from PIL import ImageGrab
