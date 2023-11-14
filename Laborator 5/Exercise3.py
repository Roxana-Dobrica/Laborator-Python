class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def get_information(self):
        print(f"Make: {self.make}, Model: {self.model}, Year: {self.year}")


class Car(Vehicle):
    def __init__(self, make, model, year, engine_size, fuel_capacity):
        super().__init__(make, model, year)
        self.engine_size = engine_size
        self.fuel_capacity = fuel_capacity

    def calculate_mileage(self):
        miles = (self.engine_size * 2) / self.fuel_capacity
        print(f"Estimated mileage for the car: {miles}")


class Motorcycle(Vehicle):
    def __init__(self, make, model, year, engine_size, fuel_tank_capacity):
        super().__init__(make, model, year)
        self.engine_size = engine_size
        self.fuel_tank_capacity = fuel_tank_capacity

    def calculate_mileage(self):
        miles = (self.engine_size * 1.5) / self.fuel_tank_capacity
        print(f"Estimated mileage for the motorcycle: {miles}")


class Truck(Vehicle):
    def __init__(self, make, model, year, engine_power, transmission_type, towing_capacity_factor):
        super().__init__(make, model, year)
        self.engine_power = engine_power
        self.transmission_type = transmission_type
        self.towing_capacity_factor = towing_capacity_factor

    def calculate_towing_capacity(self):
        base_towing_capacity = 1000
        if self.transmission_type == "automatic":
            towing_capacity = base_towing_capacity + self.engine_power * self.towing_capacity_factor
        else:
            towing_capacity = base_towing_capacity + (self.engine_power * 1.2) * self.towing_capacity_factor

        print(f"Estimated towing capacity for the truck: {towing_capacity} pounds")


def main():
    car = Car(make="Ford", model="Mustang", year=2022, engine_size=3.5, fuel_capacity=18)
    motorcycle = Motorcycle(make="BMW", model="R1250GS", year=2022, engine_size=1.3, fuel_tank_capacity=20)
    truck = Truck(make="Ram", model="1500", year=2022, engine_power=320, transmission_type="automatic", towing_capacity_factor=2.8)

    vehicles = [car, motorcycle, truck]

    for vehicle in vehicles:
        vehicle.get_information()
        if isinstance(vehicle, (Car, Motorcycle)):
            vehicle.calculate_mileage()
        elif isinstance(vehicle, Truck):
            vehicle.calculate_towing_capacity()
        print("\n")


if __name__ == "__main__":
    main()


