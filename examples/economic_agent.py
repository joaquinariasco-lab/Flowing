from example_agent import ExampleAgent

class EconomicAgent(ExampleAgent):
    def __init__(self, name, balance=10):
        super().__init__(name)
        self.balance = balance

    def can_accept_task(self, price):
        return self.balance >= 0

    def earn(self, amount):
        self.balance += amount

    def lose(self, amount):
        self.balance -= amount
