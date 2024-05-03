class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def __repr__(self):
        return f"Vehicle(make='{self.make}', model='{self.model}', year={self.year})"

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

