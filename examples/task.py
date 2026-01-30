class Task:
    def __init__(self, description, price, criteria):
        self.description = description
        self.price = price
        self.criteria = criteria  # function that validates the result
