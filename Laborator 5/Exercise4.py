class Employee:
    def __init__(self, first_name, last_name, age, role, salary):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.role = role
        self.salary = salary

    def get_name(self):
        return {f"{self.first_name} {self.last_name}"}

    def change_first_name(self, first_name):
        self.first_name = first_name

    def change_last_name(self, last_name):
        self.last_name = last_name

    def change_role(self, role):
        self.role = role

    def change_age(self, age):
        self.age = age

    def change_salary(self, salary):
        self.salary = salary

    def display_info(self):
        print(f"Name: {self.get_name()}, Role: {self.role}, Salary: {self.salary}")


class Manager(Employee):
    def __init__(self, first_name, last_name, age, salary, team_size):
        super().__init__(first_name, last_name, age, role="Manager", salary=salary)
        self.team_size = team_size

    def display_info(self):
        super().display_info()
        print(f"Team Size: {self.team_size}")


class Engineer(Employee):
    def __init__(self, first_name, last_name, age, salary, programming_language):
        super().__init__(first_name, last_name, age, role="Engineer", salary=salary)
        self.programming_language = programming_language

    def display_info(self):
        super().display_info()
        print(f"Programming Language: {self.programming_language}")


class Salesperson(Employee):
    def __init__(self, first_name, last_name, age, salary, sales_target):
        super().__init__(first_name, last_name, age, role="Salesperson", salary=salary)
        self.sales_target = sales_target

    def display_info(self):
        super().display_info()
        print(f"Sales Target: {self.sales_target}")

    def change_sales_target(self, sales_target):
        self.sales_target = sales_target


def main():
    manager = Manager(first_name="John", last_name="James", age=35, salary=8000, team_size=10)
    engineer = Engineer(first_name="Mary", last_name="Madison", age=29, salary=7000, programming_language="Python")
    salesperson = Salesperson(first_name="Bob", last_name="Wilson", age=28, salary=6000, sales_target=50000)

    manager.display_info()
    engineer.display_info()
    salesperson.display_info()

    manager.change_salary(85000)
    engineer.change_role("Senior Engineer")
    salesperson.change_sales_target(600000)

    print("\nUpdated Information:")
    manager.display_info()
    engineer.display_info()
    salesperson.display_info()


if __name__ == "__main__":
    main()
