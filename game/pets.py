import random

from game.petAbstract import Pet

"""
common    | 1 | 50% | cat, dog, parrot, hamster, canary, snake, guinea pig, ferret
uncommon  | 2 | 30% | sugar glider, capybara, hedgehog, axolotl, bee
rare      | 3 | 15% | fennec foxes, serval, kinkajou, mantis shrimp
legendary | 4 |  4% | clouded leopard, shoebill
mystical  | 5 |  1% | komodo dragon
"""

##########
# COMMON #
##########


class catPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "cat"

        self.rarity = 1

        self.renderImage = "cat.png"


class dogPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "dog"
        self.rarity = 1
        self.hungerRate = 1.2
        self.thirstRate = 1.1
        self.funRate = 1.5
        self.renderImage = "dog.png"


class parrotPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "parrot"
        self.rarity = 1
        self.hungerRate = 0.9
        self.thirstRate = 1.0
        self.funRate = 1.6
        self.renderImage = "parrot.png"


class hamsterPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "hamster"
        self.rarity = 1
        self.hungerRate = 0.8
        self.thirstRate = 0.9
        self.funRate = 1.0
        self.renderImage = "hamster.png"


class canaryPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "canary"
        self.rarity = 1
        self.hungerRate = 0.7
        self.thirstRate = 0.8
        self.funRate = 1.2
        self.renderImage = "canary.png"


class snakePet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "snake"
        self.rarity = 1
        self.hungerRate = 0.4
        self.thirstRate = 0.5
        self.funRate = 0.2
        self.renderImage = "snake.png"


class guineaPigPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "guinea_pig"
        self.rarity = 1
        self.hungerRate = 1.0
        self.thirstRate = 1.0
        self.funRate = 1.2
        self.renderImage = "guinea-pig.png"


class ferretPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "ferret"
        self.rarity = 1
        self.hungerRate = 1.1
        self.thirstRate = 1.0
        self.funRate = 1.7
        self.renderImage = "ferret.png"


COMMON_PETS = [
    catPet, dogPet,
    parrotPet, hamsterPet,
    canaryPet, snakePet,
    guineaPigPet, ferretPet
]


############
# UNCOMMON #
############


class sugarGliderPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "sugar_glider"
        self.rarity = 2
        self.hungerRate = 1.2
        self.thirstRate = 1.1
        self.funRate = 1.8
        self.renderImage = "sugar-glider.png"


class capybaraPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "capybara"
        self.rarity = 2
        self.hungerRate = 1.5
        self.thirstRate = 1.6
        self.funRate = 1.3
        self.renderImage = "capybara.png"


class hedgehogPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "hedgehog"
        self.rarity = 2
        self.hungerRate = 0.9
        self.thirstRate = 0.9
        self.funRate = 0.8
        self.renderImage = "hedgehog.png"


class axolotlPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "axolotl"
        self.rarity = 2
        self.hungerRate = 0.7
        self.thirstRate = 1.8
        self.funRate = 0.5
        self.renderImage = "axolotl.png"


class beePet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "bee"
        self.rarity = 2
        self.hungerRate = 1.3
        self.thirstRate = 1.2
        self.funRate = 0.3
        self.renderImage = "bee.png"


UNCOMMON_PETS = [
    sugarGliderPet, capybaraPet,
    hedgehogPet, axolotlPet,
    beePet
]


########
# RARE #
########


class fennecFoxPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "fennec_fox"
        self.rarity = 3
        self.hungerRate = 1.4
        self.thirstRate = 1.3
        self.funRate = 1.8
        self.renderImage = "fennec.png"


class servalPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "serval"
        self.rarity = 3
        self.hungerRate = 1.8
        self.thirstRate = 1.5
        self.funRate = 2.0
        self.renderImage = "serval.png"


class kinkajouPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "kinkajou"
        self.rarity = 3
        self.hungerRate = 1.3
        self.thirstRate = 1.2
        self.funRate = 1.7
        self.renderImage = "kinkajou.png"


class mantisShrimpPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "mantis_shrimp"
        self.rarity = 3
        self.hungerRate = 1.0
        self.thirstRate = 2.0
        self.funRate = 0.4
        self.renderImage = "mantis-shrimp.png"


RARE_PETS = [
    fennecFoxPet, servalPet,
    kinkajouPet, mantisShrimpPet
]


#############
# LEGENDARY #
#############


class cloudedLeopardPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "clouded_leopard"
        self.rarity = 4
        self.hungerRate = 2.0
        self.thirstRate = 1.7
        self.funRate = 2.2
        self.renderImage = "leopard.png"


class shoebillPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "shoebill"
        self.rarity = 4
        self.hungerRate = 1.8
        self.thirstRate = 1.6
        self.funRate = 0.7
        self.renderImage = "stork.png"


LEGENDARY_PETS = [
    cloudedLeopardPet, shoebillPet
]


############
# MYSTICAL #
############


class komodoDragonPet(Pet):
    def __init__(self):
        super().__init__()
        self.id = "komodo_dragon"
        self.rarity = 5
        self.hungerRate = 2.5
        self.thirstRate = 2.0
        self.funRate = 1.0
        self.renderImage = "komodo.png"


MYSTICAL_PETS = [
    komodoDragonPet
]


def get_rarity():
    roll = random.randint(1, 100)

    if roll <= 50:
        return COMMON_PETS
    elif roll <= 80:
        return UNCOMMON_PETS
    elif roll <= 95:
        return RARE_PETS
    elif roll <= 99:
        return LEGENDARY_PETS
    else:
        return MYSTICAL_PETS


def get_randomPet():
    rar = get_rarity()

    return random.sample(rar, 1)[0]
