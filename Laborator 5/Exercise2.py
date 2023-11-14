class Account:
    def __init__(self, balance, interest_rate):
        self.balance = balance
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self.balance += amount
        print(f"The amount of {amount} successfully added to the account. Current balance: {self.balance}")

    def withdrawal(self, amount):
        if amount > self.balance:
            print(f"Insufficient funds for withdrawal.")
        else:
            self.balance -= amount
            print(f"Withdrawal of {amount} successful. Remaining balance: {self.balance}")

    def calculate_interest(self):
        interest = self.balance * (self.interest_rate / 100)
        self.balance += interest
        print(f"Interest calculated: {interest}. New balance: {self.balance}")

    def get_balance(self):
        return self.balance


class SavingsAccount(Account):

    def __init__(self, balance, interest_rate, withdrawal_limit):
        super().__init__(balance, interest_rate)
        self.withdrawal_limit = withdrawal_limit

    def withdrawal(self, amount):
        if amount <= self.withdrawal_limit and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrawal of {amount} successful. Remaining balance: {self.balance}")
        else:
            print("Insufficient funds or reached withdrawal limit.")


class CheckingAccount(Account):

    def __init__(self, balance, num_of_transactions_limit):
        super().__init__(balance, interest_rate = 0)
        self.num_of_transactions_limit = num_of_transactions_limit

    def withdrawal(self, amount):
        if amount <= self.balance and self.num_of_transactions_limit > 0:
            self.balance -= amount
            self.num_of_transactions_limit -= 1
            print(f"Withdrawal of {amount} successful. Remaining balance: {self.balance} and transactions: {self.num_of_transactions_limit}")
        else:
            print("Insufficient funds or reached transactions limit.")


def main():
    savings_account = SavingsAccount(balance=1000, interest_rate=5, withdrawal_limit=200)
    savings_account.deposit(500)
    savings_account.withdrawal(150)
    savings_account.calculate_interest()

    checking_account = CheckingAccount(balance=2000, num_of_transactions_limit=3)
    checking_account.deposit(1000)
    checking_account.withdrawal(500)
    checking_account.withdrawal(800)
    checking_account.calculate_interest()
    print(f"Checking account balance: {checking_account.get_balance()}")


if __name__ == "__main__":
    main()







