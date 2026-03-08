
def clamp(val):
    return min(max(val, 0), 100)


class Pet:
    def __init__(self):
        self.id = "undefined"

        self.hunger = 100
        self.thirst = 100
        self.fun = 100

        self.hungerRate = 1
        self.thirstRate = 1
        self.funRate = 1

        self.age = 1
        self.days = 0

        self.xp = 0
        self.level = 1

        self.alive = True

        self.name = "unnamed"

        self.rarity = 1

        self.renderImage = None

    def getXP_req(self):
        return int(50 * (self.level ** 1.5))

    def getFoodNeed(self):
        return self.hunger < 35

    def getWaterNeed(self):
        return self.thirst < 40

    def getFunNeed(self):
        return self.fun < 15

    def save(self):
        return {
            "id": self.id,
            "hunger": self.hunger,
            "thirst": self.thirst,
            "fun": self.fun,
            "hungerRate": self.hungerRate,
            "thirstRate": self.thirstRate,
            "funRate": self.funRate,
            "age": self.age,
            "days": self.days,
            "xp": self.xp,
            "level": self.level,
            "alive": self.alive,
            "name": self.name,
            "rarity": self.rarity,
            "renderImage": self.renderImage,
        }

    def load(self, data):
        self.id = data["id"]
        self.hunger = data["hunger"]
        self.thirst = data["thirst"]
        self.fun = data["fun"]
        self.hungerRate = data["hungerRate"]
        self.thirstRate = data["thirstRate"]
        self.funRate = data["funRate"]
        self.age = data["age"]
        self.days = data["days"]
        self.xp = data["xp"]
        self.level = data["level"]
        self.alive = data["alive"]
        self.name = data["name"]
        self.rarity = data["rarity"]
        self.renderImage = data["renderImage"]

    def onTick(self):
        if not self.alive:
            return

        self.hunger = clamp(self.hunger - self.hungerRate)
        self.thirst = clamp(self.thirst - self.thirstRate)
        self.fun = clamp(self.fun - self.funRate)

        self.days += 1

        if self.days >= 365:
            self.age += 1
            self.days = 0

        if self.age >= 20 and self.days >= 80:
            self.alive = False
