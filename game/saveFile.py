from json import dump, load

from game.pathHelp import resourcePath
from game.petReg import petReg_load
from game.pets import catPet


class saveFile:
    def __init__(self):
        self.money = 100
        self.specialMoney = 1000

        self.gifts = 0

        self.pets = [
            catPet()
        ]

        self.inventory = {}

    def save(self, where):
        petsData = []
        for pet in self.pets:
            petsData.append(pet.save())

        saveData = {
            "money": self.money,
            "specialMoney": self.specialMoney,
            "gifts": self.gifts,
            "pets": petsData,
            "inventory": self.inventory
        }

        with open(resourcePath("resources/saves/" + where + ".save"), "w") as f:
            dump(saveData, f, indent=4)

    def load(self, where):

        try:
            with open(resourcePath("resources/saves/" + where + ".save"), "r") as f:
                saveData = load(f)

        except FileNotFoundError:
            self.save(where)
            self.load(where)
            return

        self.money = saveData["money"]
        self.specialMoney = saveData["specialMoney"]
        self.gifts = saveData["gifts"]

        for pet in saveData["pets"]:
            self.pets.append(petReg_load(pet))

        self.inventory = saveData["inventory"]

    def checkAnyNeeds(self):
        for index, pet in enumerate(self.pets):
            if pet.getFoodNeed() or pet.getWaterNeed() or pet.getFoodNeed():
                return index, True

        return 0, False
