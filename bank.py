class BankAccount:
	def __init__(self, account_holder, pin, balance=1000.0):
		self.account_holder = account_holder
		self.pin = pin
		self.balance = balance
		self.transactions = []

	def check_pin(self, entered_pin):
		return entered_pin == self.pin

	def show_balance(self):
		print(f"\nAvailable balance: ${self.balance:.2f}")

	def deposit(self, amount):
		if amount <= 0:
			print("Deposit amount must be greater than zero.")
			return

		self.balance += amount
		self.transactions.append(f"Deposit: +${amount:.2f}")
		print(f"Deposit successful. New balance: ${self.balance:.2f}")

	def withdraw(self, amount):
		if amount <= 0:
			print("Withdrawal amount must be greater than zero.")
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

		self.pin = new_pin
		print("Your PIN has been changed.")


class ATM:
	def __init__(self, account):
		self.account = account

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
		print("Welcome to the ATM")
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
			elif choice == "3":
				amount = self.get_amount("Enter withdrawal amount: $")
				if amount is not None:
					self.account.withdraw(amount)
			elif choice == "4":
				self.account.show_transactions()
			elif choice == "5":
				new_pin = input("Enter a new 4-digit PIN: ").strip()
				self.account.change_pin(new_pin)
			elif choice == "6":
				print("Thank you for using the ATM. Goodbye!")
				break
			else:
				print("Invalid option. Please choose a number from 1 to 6.")


if __name__ == "__main__":
	# Demo account: PIN 1234 and starting balance $1000.
	account = BankAccount("Alex", "1234")
	atm = ATM(account)
	atm.run()
