class Animal:
    def __init__(self, name, habitat, sound):
        self.name = name
        self.habitat = habitat
        self.sound = sound

    def make_sound(self):
        print(f"{self.name} says {self.sound}!")


class Mammal(Animal):
    def __init__(self, name, habitat, sound, fur_color):
        super().__init__(name, habitat, sound)
        self.fur_color = fur_color

    def nurse_young(self):
        print(f"The {self.name} is nursing its young.")

    def give_birth(self, number_of_cubs):
        print(f"The {self.name} gave birth to {number_of_cubs} cubs.")


class Bird(Animal):
    def __init__(self, name, habitat, sound, feathers_color, can_fly):
        super().__init__(name, habitat, sound)
        self.feathers_color = feathers_color
        self.can_fly = can_fly

    def fly(self):
        if self.can_fly:
            print(f"{self.name} is flying.")
        else:
            print(f"{self.name} cannot fly.")

    def migrates(self, place):
        print(f"The {self.name} migrates in {place}")


class Fish(Animal):
    def __init__(self, name, habitat, sound, scale_type):
        super().__init__(name, habitat, sound)
        self.scale_type = scale_type

    def swim(self, depth):
        print(f"The {self.name} is swimming at a depth of {depth} meters")

    def lay_eggs(self):
        print(f"{self.name} is laying eggs.")


def main():
    dog = Mammal("Dog", "Domestic", "Ham Ham!", "Brown")
    stork = Bird("Stork", "Wetlands", "Caw!", "White", True)
    shark = Fish("Shark", "Oceans", "Grr!", "Placoid")

    dog.give_birth(2)
    dog.nurse_young()

    stork.fly()
    stork.migrates("South")

    shark.swim(100)
    shark.lay_eggs()

    print("\nDetails of the animals:")
    print(f"{dog.name} in {dog.habitat} habitat has fur color: {dog.fur_color}")
    print(f"{stork.name} in {stork.habitat} habitat has feathers color: {stork.feathers_color}")
    print(f"{shark.name} in {shark.habitat} habitat has scale type: {shark.scale_type}")


if __name__ == "__main__":
    main()