
import pygame.image
from folumo.betterGUI.basicElements import Rect, Circle, Text, Image
from folumo.betterGUI.screen import Color, Element, Canvas, Screen
from folumo.betterGUI.UI.toolbox import ProgressBar

from game.pathHelp import resourcePath
from game.pets import get_randomPet

SHOP_ITEMS = {
    "food": 25,
    "water": 15,
    "toy": 40
}


ITEM_TO_STAT = {
    "food": "hunger",
    "water": "thirst",
    "toy": "fun",
}


ITEM_TO_STAT_AMM = {
    "food": 60,
    "water": 40,
    "toy": 80
}


class Button(Rect):
    def __init__(self, xy, size, text, callback):
        super().__init__(xy, size, Color(195, 60, 111))

        self.text = Text((8, 5), text, None, 28, Color(255, 255, 255))
        self.callback = callback

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect(self.xy, self.wh).collidepoint(event.pos):
                    self.callback()
                    return True

    def onClick(self):
        self.callback()

    def render(self) -> Canvas:
        canv = super().render()

        canv.drawFromCanvas(self.text.render(), self.text.xy)

        return canv


class NeedElement(Element):
    def __init__(self, xy, color, icon):
        super().__init__(xy)

        self.color = color
        self.shown = True

        size = 30

        self.icon = pygame.transform.scale(
            pygame.image.load(resourcePath(f"resources/textures/{icon}")),
            (size * 1.5, size * 1.5)
        )

        self.rendered = Circle(None, size, color).render()
        self.rendered.drawFromSurface(self.icon, (8, 8))

    def render(self) -> Canvas:

        if self.shown:
            return self.rendered

        return Canvas((0, 0))


def trLoad(path, wh):
    return pygame.transform.scale(pygame.image.load(resourcePath(path)), wh)


class shopElement(Element):
    def __init__(self, xy, screen):
        super().__init__(xy)

        self.screen = screen

        self.food = trLoad("resources/textures/shop/cat-food.png", (175, 175))
        self.water = trLoad("resources/textures/shop/glass-of-water.png", (175, 175))
        self.toy = trLoad("resources/textures/shop/toy.png", (175, 175))

        self.shopOpened = False

        self.shopImg = pygame.image.load(resourcePath("resources/textures/shop.png"))
        self.shopButtonAt = 600, 125

        self.buyText = Text(None, "Buy!", None, 30, Color(255, 255, 255)).render()

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect((64, 64), self.shopButtonAt).collidepoint(event.pos):
                    self.shopOpened = not self.shopOpened

                else:
                    if self.shopOpened:
                        if pygame.Rect((600, 225 + 125), (90, 25)).collidepoint(event.pos):
                            self.tryBuy("food")

                        elif pygame.Rect((600, 425 + 125), (90, 25)).collidepoint(event.pos):
                            self.tryBuy("water")

                        elif pygame.Rect((600, 625 + 125), (90, 25)).collidepoint(event.pos):
                            self.tryBuy("toy")

                        elif pygame.Rect((600 + 5, 75 + 125), (175, 175)).collidepoint(event.pos):
                            self.tryUse("food")

                        elif pygame.Rect((600 + 5, 275 + 125), (175, 175)).collidepoint(event.pos):
                            self.tryUse("water")

                        elif pygame.Rect((600 + 5, 475 + 125), (175, 175)).collidepoint(event.pos):
                            self.tryUse("toy")

        return False

    def render(self) -> Canvas:
        fullscr = Canvas((200, 675), False, Color(175, 18, 237)) if self.shopOpened else Canvas((200, 675))
        fullscr.drawFromSurface(self.shopImg, (0, 0))

        if self.shopOpened:
            fullscr.drawFromSurface(self.food, (5, 75))
            fullscr.drawFromCanvas(Canvas((200, 25), False, Color(102, 0, 255)), (0, 225))
            fullscr.drawFromCanvas(Canvas((90, 25), False, Color(29, 226, 127)), (0, 225))
            fullscr.drawFromCanvas(self.buyText, ((90 - 45) / 2,  225 + ((25 - 20) / 2)))
            fullscr.drawFromCanvas(Text(None, f"{SHOP_ITEMS['food']} | x{self.screen.data.inventory.get('food', 0)}", None, 30, Color(255, 255, 255)).render(), (100, 230))

            fullscr.drawFromSurface(self.water, (5, 275))
            fullscr.drawFromCanvas(Canvas((200, 25), False, Color(102, 0, 255)), (0, 425))
            fullscr.drawFromCanvas(Canvas((90, 25), False, Color(29, 226, 127)), (0, 425))
            fullscr.drawFromCanvas(self.buyText, ((90 - 45) / 2,  425 + ((25 - 20) / 2)))
            fullscr.drawFromCanvas(Text(None, f"{SHOP_ITEMS['water']} | x{self.screen.data.inventory.get('water', 0)}", None, 30, Color(255, 255, 255)).render(), (100, 430))

            fullscr.drawFromSurface(self.toy, (5, 475))
            fullscr.drawFromCanvas(Canvas((200, 25), False, Color(102, 0, 255)), (0, 625))
            fullscr.drawFromCanvas(Canvas((90, 25), False, Color(29, 226, 127)), (0, 625))
            fullscr.drawFromCanvas(self.buyText, ((90 - 45) / 2,  625 + ((25 - 20) / 2)))
            fullscr.drawFromCanvas(Text(None, f"{SHOP_ITEMS['toy']} | x{self.screen.data.inventory.get('toy', 0)}", None, 30, Color(255, 255, 255)).render(), (100, 630))

        return fullscr

    def tryBuy(self, item):
        cost = SHOP_ITEMS[item]
        money = self.screen.data.money

        if money >= cost:
            self.screen.data.money -= cost

            self.screen.data.inventory[item] = self.screen.data.inventory.get(item, 0) + 1

    def tryUse(self, item):
        amm = self.screen.data.inventory.get(item, 0)

        if amm > 0:
            self.screen.data.inventory[item] = amm - 1

            stat = ITEM_TO_STAT[item]
            self.screen.increaseStat(stat, ITEM_TO_STAT_AMM[item])


class pullingElement(Element):
    def __init__(self, xy, screen):
        super().__init__(xy)

        self.screen = screen
        self.shown = False

        self.loadedImage = pygame.image.load(resourcePath("resources/textures/gift/gift.png")).convert_alpha()
        self.loadedImageOpened = pygame.image.load(resourcePath("resources/textures/gift/gift-open.png")).convert_alpha()

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect((0, 725), (75, 75)).collidepoint(event.pos):
                    self.shown = not self.shown

                    if self.shown:
                        self.screen.petEl.isShown = False

                    else:
                        self.screen.petEl.isShown = True

                elif self.shown:
                    if pygame.Rect(500, 205, 190, 30).collidepoint(event.pos):
                        if self.screen.data.specialMoney >= 100:
                            self.screen.data.specialMoney -= 100
                            self.screen.data.gifts += 1

                    elif pygame.Rect(500, 240, 190, 30).collidepoint(event.pos):
                        if self.screen.data.gifts >= 1:
                            self.screen.data.gifts -= 1

                            self.pullRandomPet()

        return False

    def pullRandomPet(self):
        newPet = get_randomPet()()
        self.screen.data.pets.append(newPet)

        self.screen.petIndex = len(self.screen.data.pets) - 1

        self.shown = False
        self.screen.petEl.isShown = True

    def render(self) -> Canvas:
        canv = Canvas((800, 800))

        canv.drawFromCanvas(Circle(None, 50, Color(211, 105, 212)).render(), (-20, 725))
        canv.drawFromCanvas(Image(None, resourcePath("resources/textures/wish.png")).render(), (5, 736))

        if self.shown:
            canv.drawFromSurface(self.loadedImage, (208, 300))

            pygame.draw.rect(canv.surf, (216, 140, 39), (100, 200, 600, 80), 0, 20)
            canv.drawFromCanvas(Image(None, resourcePath("resources/textures/wish.png")).render(), (116, 210))
            canv.drawFromCanvas(Text(None, f"{self.screen.data.gifts}", None, 72, Color(255, 255, 255)).render(), (196, 218))

            canv.drawFromCanvas(Image(None, resourcePath("resources/textures/crystal.png")).render(), (316, 210))
            canv.drawFromCanvas(Text(None, f"{self.screen.data.specialMoney}", None, 72, Color(255, 255, 255)).render(), (396, 218))

            pygame.draw.rect(canv.surf, (148, 23, 18), (500, 205, 190, 30), 0, 20) # buy
            canv.drawFromCanvas(Text(None, f"Buy 1 gift for 100 crystals", None, 20, Color(255, 255, 255)).render(), (500 + 14, 205 + 9))

            pygame.draw.rect(canv.surf, (28, 217, 227), (500, 240, 190, 30), 0, 20) # open
            canv.drawFromCanvas(Text(None, f"Open 1 gift!", None, 20, Color(255, 255, 255)).render(), (500 + 58, 240 + 9))

        return canv


class topBarElementManager:

    def __init__(self, screen: Screen, elements):

        self.screen = screen
        self.shopOpen = False

        self.foodNeed = NeedElement((10, 55), Color(171, 110, 84), "shop/cat-food.png")
        self.waterNeed = NeedElement((40, 55), Color(56, 141, 199), "shop/glass-of-water.png")
        self.funNeed = NeedElement((70, 55), Color(232, 223, 0), "shop/toy.png")

        self.moneyText = Text((25, 25), "Money: 0", None, 40, Color(255, 255, 255))
        self.petNameText = Text((225, 25), "Pet: ?", None, 40, Color(255, 255, 255))
        self.petAgeText = Text((450, 25), "Age: ?", None, 40, Color(255, 255, 255))

        self.xpText = Text((310, 75), "0 / 100 xp", None, 36, Color(255, 255, 255))
        self.levelText = Text((710, 75), "0", None, 36, Color(255, 255, 255))

        self.wishingElement = pullingElement((0, 0), screen)

        self.xpBar = ProgressBar(
            (300, 70),
            (400, 30),
            0,
            100,
            0,
            Color(137, 209, 223),
            Color(4, 13, 15)
        )

        # pet switching
        self.prevPet = Button((650, 20), (40, 40), "<", self.switchPrevPet)
        self.nextPet = Button((750, 20), (40, 40), ">", self.switchNextPet)

        els = [
            Rect((0, 0), (800, 125), Color(211, 105, 212)),
            Rect((0, 120), (800, 5), Color(0, 0, 0)),

            self.foodNeed,
            self.waterNeed,
            self.funNeed,

            self.moneyText,
            self.petNameText,
            self.petAgeText,

            self.xpBar,
            self.xpText,
            self.levelText,

            self.wishingElement,

            self.prevPet,
            self.nextPet,

            shopElement((600, 125), screen),
        ]

        elements.extend(els)

    def switchPrevPet(self):

        pets = self.screen.data.pets

        if not pets:
            return

        self.screen.petIndex -= 1

        if self.screen.petIndex < 0:
            self.screen.petIndex = len(pets) - 1

    def switchNextPet(self):

        pets = self.screen.data.pets

        if not pets:
            return

        self.screen.petIndex += 1

        if self.screen.petIndex >= len(pets):
            self.screen.petIndex = 0
