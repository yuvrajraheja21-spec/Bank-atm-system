import hashlib
import json
import math
from pathlib import Path


class BankAccount:
	def __init__(self, account_number, account_holder, pin, balance=0.0, transactions=None, pin_is_hashed=False):
		self.account_number = account_number
		self.account_holder = account_holder
		self.pin_hash = pin if pin_is_hashed else self.hash_pin(pin)
		self.balance = balance
		self.transactions = transactions if transactions is not None else []

	@staticmethod
	def hash_pin(pin):
		return hashlib.sha256(pin.encode("utf-8")).hexdigest()

	@classmethod
	def from_record(cls, record):
		return cls(
			record["account_number"],
			record["account_holder"],
			record["pin_hash"],
			record["balance"],
			record["transactions"],
			pin_is_hashed=True,
		)

	def to_record(self):
		return {
			"account_number": self.account_number,
			"account_holder": self.account_holder,
			"pin_hash": self.pin_hash,
			"balance": self.balance,
			"transactions": self.transactions,
		}

	def check_pin(self, entered_pin):
		return self.hash_pin(entered_pin) == self.pin_hash

	def show_balance(self):
		print(f"\nAvailable balance: ${self.balance:.2f}")

	def deposit(self, amount):
		if not math.isfinite(amount) or amount <= 0:
			print("Deposit amount must be a valid number greater than zero.")
			return

		self.balance += amount
		self.transactions.append(f"Deposit: +${amount:.2f}")
		print(f"Deposit successful. New balance: ${self.balance:.2f}")

	def withdraw(self, amount):
		if not math.isfinite(amount) or amount <= 0:
			print("Withdrawal amount must be a valid number greater than zero.")
		elif amount > self.balance:
			print("Insufficient funds.")
		else:
			self.balance -= amount
			self.transactions.append(f"Withdrawal: -${amount:.2f}")
			print(f"Please take your cash. New balance: ${self.balance:.2f}")

	def show_transactions(self):
		print("\n--- Recent Transactions ---")
		if not self.transactions:
			print("No transactions yet.")
		else:
			for transaction in self.transactions:
				print(transaction)

	def change_pin(self, new_pin):
		if len(new_pin) != 4 or not new_pin.isdigit():
			print("PIN must be exactly four digits.")
			return

		self.pin_hash = self.hash_pin(new_pin)
		print("Your PIN has been changed.")


class BankSystem:
	def __init__(self, file_path=None):
		self.file_path = Path(file_path) if file_path else Path(__file__).with_name("bank_accounts.txt")
		self.accounts = []
		self.load_accounts()

	def load_accounts(self):
		if not self.file_path.exists():
			return

		with self.file_path.open("r", encoding="utf-8") as account_file:
			records = json.load(account_file)
		if not isinstance(records, list):
			raise ValueError("The account file must contain a list of accounts.")
		self.accounts = [BankAccount.from_record(record) for record in records]

	def save_accounts(self):
		with self.file_path.open("w", encoding="utf-8") as account_file:
			json.dump([account.to_record() for account in self.accounts], account_file, indent=4)

	def add_account(self, account_holder, pin):
		numbers = [int(account.account_number) for account in self.accounts]
		account_number = str(max(numbers, default=100000) + 1)
		account = BankAccount(account_number, account_holder, pin)
		self.accounts.append(account)
		return account

	def find_account(self, account_number):
		for account in self.accounts:
			if account.account_number == account_number:
				return account
		return None


class ATM:
	def __init__(self, account, save_accounts):
		self.account = account
		self.save_accounts = save_accounts

	def login(self):
		attempts_left = 3

		while attempts_left > 0:
			entered_pin = input("Enter your 4-digit PIN: ")
			if self.account.check_pin(entered_pin):
				print(f"\nWelcome, {self.account.account_holder}!")
				return True

			attempts_left -= 1
			if attempts_left > 0:
				print(f"Incorrect PIN. {attempts_left} attempt(s) left.")

		print("Too many incorrect attempts. Your session has ended.")
		return False

	def get_amount(self, prompt):
		try:
			return float(input(prompt))
		except ValueError:
			print("Please enter a valid number.")
			return None

	def show_menu(self):
		print("\n======= ATM MENU =======")
		print("1. Check balance")
		print("2. Deposit money")
		print("3. Withdraw money")
		print("4. View transactions")
		print("5. Change PIN")
		print("6. Exit")

	def run(self):
		if not self.login():
			return

		while True:
			self.show_menu()
			choice = input("Choose an option (1-6): ").strip()

			if choice == "1":
				self.account.show_balance()
			elif choice == "2":
				amount = self.get_amount("Enter deposit amount: $")
				if amount is not None:
					self.account.deposit(amount)
					self.save_accounts()
			elif choice == "3":
				amount = self.get_amount("Enter withdrawal amount: $")
				if amount is not None:
					self.account.withdraw(amount)
					self.save_accounts()
			elif choice == "4":
				self.account.show_transactions()
			elif choice == "5":
				new_pin = input("Enter a new 4-digit PIN: ").strip()
				self.account.change_pin(new_pin)
				self.save_accounts()
			elif choice == "6":
				print("Thank you for using the ATM. Goodbye!")
				break
			else:
				print("Invalid option. Please choose a number from 1 to 6.")


def create_account(bank):
	account_holder = input("Enter account holder name: ").strip()
	while not account_holder:
		account_holder = input("Name cannot be empty. Enter account holder name: ").strip()

	pin = input("Create a 4-digit PIN: ").strip()
	while len(pin) != 4 or not pin.isdigit():
		pin = input("PIN must be exactly four digits. Try again: ").strip()

	account = bank.add_account(account_holder, pin)
	bank.save_accounts()
	print(f"Account created. Your account number is {account.account_number}.")
	print("Keep your account number safe; you will need it to log in.")


def main():
	bank = BankSystem()
	print("Welcome to the ATM Banking System")

	while True:
		print("\n======= MAIN MENU =======")
		print("1. Log in to an account")
		print("2. Create a bank account")
		print("3. Exit")
		choice = input("Choose an option (1-3): ").strip()

		if choice == "1":
			account_number = input("Enter your account number: ").strip()
			account = bank.find_account(account_number)
			if account is None:
				print("Account not found. Create an account first or check the number.")
			else:
				ATM(account, bank.save_accounts).run()
		elif choice == "2":
			create_account(bank)
		elif choice == "3":
			print("Thank you for using the ATM Banking System.")
			break
		else:
			print("Invalid option. Please choose a number from 1 to 3.")


if __name__ == "__main__":
	main()
