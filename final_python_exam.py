from abc import ABC, abstractmethod

class User(ABC):
    accounts = []

    def __init__(self, name, accountNumber, password, account_type):
        self.name = name
        self.accountNumber = accountNumber
        self.password = password
        self.account_type = account_type
        self.balance = 0
        self.account_history = []
        User.accounts.append(self)

    @abstractmethod
    def transfer(self, target_account, amount):
        pass

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.account_history.append(f'Deposit: +${amount}')
            print(f'Deposited ${amount}. New balance: ${self.balance}')
        else:
            print('Invalid deposit amount.')

    def withdraw(self, amount):
        if amount >= 0:
            if self.balance >= amount:
                self.balance -= amount
                self.account_history.append(f'Withdraw: -${amount}')
                print(f'Withdrew ${amount}. New balance: ${self.balance}')
            else:
                print('Withdrawal amount exceeded.')
        else:
            print('Invalid withdrawal amount.')

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.account_history

    def show_info(self):
        return f'Name: {self.name}, Account Number: {self.accountNumber}, Account Type: {self.account_type}, Balance: ${self.balance}'

class SavingsUser(User):
    def __init__(self, name, accountNumber, password):
        super().__init__(name, accountNumber, password, 'Savings')
        self.loan_taken = 0
        self.transfer_limit = 2

    def transfer(self, target_account, amount):
        if target_account in User.accounts:
            if amount >= 0:
                if self.balance >= amount:
                    self.balance -= amount
                    target_account.deposit(amount)
                    self.account_history.append(f'Transfer: -${amount}')
                    print(f'Transferred ${amount} to {target_account.name}.')
                else:
                    print('Transfer amount exceeded.')
            else:
                print('Invalid transfer amount.')
        else:
            print('Account does not exist.')

    def take_loan(self, amount):
        if self.loan_taken < 2:
            self.loan_taken += 1
            self.balance += amount
            self.account_history.append(f'Loan: +${amount}')
            print(f'Loan approved: +${amount} added to your account.')
        else:
            print('You have already taken the maximum number of loans (2).')

class CurrentUser(User):
    def transfer(self, target_account, amount):
        if target_account in User.accounts:
            if amount >= 0:
                if self.balance >= amount:
                    self.balance -= amount
                    target_account.deposit(amount)
                    self.account_history.append(f'Transfer: -${amount}')
                    print(f'Transferred ${amount} to {target_account.name}.')
                else:
                    print('Transfer amount exceeded.')
            else:
                print('Invalid transfer amount.')
        else:
            print('Account does not exist.')

class Admin:
    class Bank:
        def __init__(self, account_no, balance, loan):
            self.account_no = account_no
            self.balance = balance
            self.loan = loan

    def __init__(self):
        self.total_balance = 0
        self.total_loan = 0
        self.loan_status = "off"
        self.accounts_list = []

    def create_account(self, account_no, initial_balance, initial_loan):
        new_account = self.Bank(account_no, initial_balance, initial_loan)
        self.accounts_list.append(new_account)
        self.total_balance += initial_balance
        self.total_loan += initial_loan

    def delete_account(self, account_no):
        for account in self.accounts_list:
            if account.account_no == account_no:
                self.total_balance -= account.balance
                self.total_loan -= account.loan
                self.accounts_list.remove(account)
                return

    def show_users(self):
        for account in self.accounts_list:
            print(f"Account No: {account.account_no}, Balance: {account.balance}, Loan: {account.loan}")

    def total_balance(self):
        print(f"Total Balance: {self.total_balance}")

    def total_loan(self):
        print(f"Total Loan: {self.total_loan}")

    def OffLoan(self):
        self.loan_status = "off"

    def OnLoan(self):
        self.loan_status = "on"

admin = Admin()
admin.create_account("0621", 0, 0) 
admin.create_account("2162", 0, 0)

currentUser = None

while True:
    if currentUser is None:
        ch = input("\n--> Register/Login (R/L) : ")
        if ch == "R":
            name = input("Name: ")
            account_number = input("Account Number: ")
            password = input("Password: ")
            account = input("Savings Account or Current Account (S/C): ")
            if account == "S":
                currentUser = SavingsUser(name, account_number, password)
            elif account == "C":
                currentUser = CurrentUser(name, account_number, password)
        else:
            account_number = input("Account Number: ")
            for account in User.accounts:
                if account.accountNumber == account_number:
                    currentUser = account
                    break
    if currentUser is not None:
        print(f"\nWelcome {currentUser.name}!\n")
        if currentUser.account_type == "Savings":
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Show Info")
            print("4. Take Loan")
            print("5. Transfer Money")
            print("6. Logout\n")

            option = int(input("Choose Option: "))

            if option == 1:
                amount = int(input("Enter withdrawal amount: "))
                currentUser.withdraw(amount)
            elif option == 2:
                amount = int(input("Enter deposit amount: "))
                currentUser.deposit(amount)
            elif option == 3:
                print(currentUser.show_info())
            elif option == 4:
                amount = int(input("Enter loan amount: "))
                currentUser.take_loan(amount)
            elif option == 5:
                target_account_number = input("Enter  account number: ")
                amount = int(input("Enter transfer amount: "))
                for account in User.accounts:
                    if account.accountNumber == target_account_number:
                        currentUser.transfer(account, amount)
                else:
                    print(' account does not exist.')
            elif option == 6:
                currentUser = None
            else:
                print("Invalid option.")
