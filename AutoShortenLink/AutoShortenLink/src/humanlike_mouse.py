import time
import random

import pyautogui

class HumanlikeMouse():
    def __init__(self):
        pass

    def move(self, destx, desty):
        x, y = pyautogui.position()         # Current Position
        moves = random.randint(2,4)
        pixelsx = destx - x
        pixelsy = desty - y
        if moves >= 4:
                moves = random.randint(2,4)
        avgpixelsx = pixelsx/moves
        avgpixelsy = pixelsy/moves
        # print ("Pixels to be moved X: ", pixelsx," Y: ",pixelsy, "Number of mouse movements: ", moves, "Avg Move X: ", avgpixelsx, " Y: ", avgpixelsy)

        while moves > 0:
                offsetx = (avgpixelsx+random.randint(-8, random.randint(5,10)));
                offsety = (avgpixelsy+random.randint(-8, random.randint(5,10)));
                # print (x + offsetx, y + offsety, moves)
                pyautogui.moveTo(x + offsetx, y + offsety, duration=0.2)
                moves = moves-1
                if moves != 0:
                    avgpixelsx = pixelsx / moves
                    avgpixelsy = pixelsy / moves

    def move_and_click(self, destx, desty):
        self.move(destx, desty)
        pyautogui.click()
