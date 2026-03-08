from game.petAbstract import Pet
from game.pets import COMMON_PETS, UNCOMMON_PETS, RARE_PETS, LEGENDARY_PETS, MYSTICAL_PETS


reg = {
    "undefined": Pet,
}


for p_rarity in (COMMON_PETS, UNCOMMON_PETS, RARE_PETS, LEGENDARY_PETS, MYSTICAL_PETS):
    for pet in p_rarity:
        pID = pet().id
        reg[pID] = pet


def petReg_load(petData):
    petID = petData["id"]

    pet = reg[petID]()
    pet.load(petData)

    return pet

