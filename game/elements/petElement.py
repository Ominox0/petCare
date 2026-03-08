import pygame
from folumo.betterGUI.screen import Element, Canvas

from game.pathHelp import resourcePath


class PetElement(Element):
    def __init__(self, xy, screen):
        super().__init__(xy)

        self.isShown = True

        self.isGettingPetted = False

        self.screen = screen

        self.onClickOffset = 10

    def render(self) -> Canvas:
        loadedImage = pygame.image.load(resourcePath("resources/textures/pets/" + self.screen.getPet().renderImage)).convert_alpha()

        w, h = loadedImage.get_size()

        pettedImage = pygame.transform.scale(loadedImage, (w, h - self.onClickOffset))

        bakedNormal = Canvas(loadedImage.get_size(), True)
        bakedNormal.drawFromSurface(loadedImage, (0, 0))

        bakedPetted = Canvas(pettedImage.get_size(), True)
        bakedPetted.drawFromSurface(pettedImage, (0, 0))

        if self.isShown:
            if self.isGettingPetted:
                return bakedPetted

            else:
                return bakedNormal
        else:
            return super().render()

    def collision(self, pos):
        wh = self.render().surf.get_size()
        return pygame.Rect(self.xy, wh).collidepoint(pos)

    def handle_event(self, event) -> bool:
        if not self.isShown:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collision(event.pos) and event.button == 1:
                self.isGettingPetted = True
                x, y = self.xy

                self.xy = x, y + self.onClickOffset

                self.screen.increaseStat("fun", 10)

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.isGettingPetted:
                self.isGettingPetted = False
                x, y = self.xy

                self.xy = x, y - self.onClickOffset

        return False
