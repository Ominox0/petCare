from time import sleep
from threading import Thread
import pystray
import pygame
from folumo.betterGUI.screen import Main, Screen, Canvas, Color
from folumo.betterGUI.basicElements import Image, Text

from game.elements.petElement import PetElement
from game.elements.topBarElement import topBarElementManager
from game.pathHelp import resourcePath
from game.saveFile import saveFile


def calculate_xp(stat_value, amm):
    missing = 100 - stat_value
    multiplier = missing / 100
    return int(amm * multiplier)


class NeedsPopupScreen(Screen):
    def __init__(self, main, SData):
        super().__init__(main)

        self.simpleData = SData

        self.main.screen = pygame.display.set_mode((400, 200), 32768)

        self.shouldOpenMainApp = False

    def render(self, toRender: Canvas):
        pygame.draw.rect(toRender.surf, (148, 20, 235), (0, 0, 400, 200))

        toRender.drawFromCanvas(Text(None, "Your pet needs attention!", None, 40, Color(255, 255, 255)).render(), (29.5, 40))

        pygame.draw.rect(toRender.surf, (255, 0, 0), (60, 100, 120, 40), 0, 20)
        toRender.drawFromCanvas(Text(None, "Ignore :(", None, 36, Color(255, 255, 255)).render(), (60 + 11, 100 + 7))

        pygame.draw.rect(toRender.surf, (124, 252, 0), (220, 100, 120, 40), 0, 20)
        toRender.drawFromCanvas(Text(None, "Visit", None, 36, Color(255, 255, 255)).render(), (220 + 33, 100 + 8))

    def procesEvent(self, event):
        super().procesEvent(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect(60, 100, 120, 40).collidepoint(event.pos):
                    self.main.running = False
                    self.simpleData["showPopup"] = False

                elif pygame.Rect(220, 100, 120, 40).collidepoint(event.pos):
                    self.shouldOpenMainApp = True
                    self.main.running = False


class PetCareScreen(Screen):
    def __init__(self, main, data):
        super().__init__(main)

        self.data = data

        self.petIndex = 0

        cursor = pygame.cursors.Cursor((16, 16), pygame.image.load(resourcePath("resources/textures/paw.png")))
        pygame.mouse.set_cursor(cursor)

        self.petEl = PetElement((144, 180), self)

        self.elements = [
            Image((0, 100), resourcePath("resources/textures/bg.png")),

            Image((144, 480), resourcePath("resources/textures/table.png")),
            self.petEl
        ]

        self.topElementManager = topBarElementManager(self, self.elements)

        for element in self.elements:
            self.add(element)

    def getPet(self):
        return self.data.pets[self.petIndex]

    def increaseStat(self, stat, amm):
        pet = self.getPet()

        value = getattr(pet, stat)

        setattr(pet, stat, min(100, value + amm))

        xp = int(amm * (abs((100 - value)) / 10))
        pet.xp += xp

        self.checkLevel(pet)

    def checkLevel(self, pet):
        level = pet.level
        xp = pet.xp

        if level >= 80:
            pet.xp = 0

        req = pet.getXP_req()

        if xp >= req:
            pet.level += 1
            pet.xp -= req

            self.data.money += pet.level * 15 * (pet.rarity * 2)
            self.data.specialMoney += pet.level * 10 * pet.rarity

    def render(self, toRender: Canvas):
        super().render(toRender)

        pet = self.getPet()

        self.topElementManager.foodNeed.shown = pet.getFoodNeed()
        self.topElementManager.waterNeed.shown = pet.getWaterNeed()
        self.topElementManager.funNeed.shown = pet.getFunNeed()

        self.topElementManager.moneyText.text = f"Money: {self.data.money}"
        self.topElementManager.petNameText.text = f"Pet: {pet.name}"
        self.topElementManager.petAgeText.text = f"Age: {pet.age}"
        self.topElementManager.xpText.text = f"{pet.xp} / {pet.getXP_req()} xp"
        self.topElementManager.levelText.text = f"{pet.level}"
        self.topElementManager.xpBar.min_val = 0
        self.topElementManager.xpBar.max_val = pet.getXP_req()
        self.topElementManager.xpBar.current_val = pet.xp


def showNeedsPopup(SData):
    screenInfo = {
        "fullscreen": False,
        "wh": (400, 200),
        "icon": resourcePath("resources/textures/icon.png")
    }

    screens = {
        "main": lambda window: NeedsPopupScreen(window, SData)
    }

    app = Main(screenInfo, screens)

    return getattr(app.screens["main"], "shouldOpenMainApp")


def showApp(simpleData):
    simpleData["shouldOpen"] = False
    screenInfo = {
        "fullscreen": False,
        "wh": (800, 800),
        "icon": resourcePath("resources/textures/icon.png")
    }

    screens = {
        "main": lambda wind: PetCareScreen(wind, simpleData["saveFile"])
    }

    Main(screenInfo, screens)

    simpleData["isMainAppShown"] = False


from threading import Thread
from time import sleep
import pystray
from PIL import Image as PIL_Image


def main():

    def tick(SData):
        while SData["isRunning"]:
            try:
                for pet in SData["saveFile"].pets:
                    pet.onTick()
                    print(pet.save())

            except Exception as e:
                print("Tick error:", e)

            SData["saveFile"].save("saved")
            sleep(60 * 2.5)

    def app_loop(SData):
        while SData["isRunning"]:

            if SData["shouldOpen"]:
                SData["shouldOpen"] = False
                showApp(SData)

            if SData["showPopup"]:
                _, should = SData["saveFile"].checkAnyNeeds()

                if not SData["isMainAppShown"] and should:
                    shouldOpenApp = showNeedsPopup(SData)

                    if shouldOpenApp:
                        SData["shouldOpen"] = True

            sleep(1)

    def on_open(icon, item):
        simpleData["shouldOpen"] = True

    def on_save(icon, item):
        simpleData["saveFile"].save("saved")

    def on_quit(icon, item):
        simpleData["isRunning"] = False
        icon.stop()

    simpleData = {
        "isRunning": True,
        "showPopup": True,
        "shouldOpen": True,
        "isMainAppShown": False,
        "saveFile": saveFile()
    }

    simpleData["saveFile"].load("saved")

    Thread(target=tick, args=(simpleData,), daemon=True).start()
    Thread(target=app_loop, args=(simpleData,), daemon=True).start()

    icon = pystray.Icon(
        "Pet Care",
        PIL_Image.open(resourcePath("resources/textures/icon.png")),
        menu=pystray.Menu(
            pystray.MenuItem("Open", on_open),
            pystray.MenuItem("Save", on_save),
            pystray.MenuItem("Quit", on_quit)
        )
    )

    icon.run()


if __name__ == "__main__":
    main()
