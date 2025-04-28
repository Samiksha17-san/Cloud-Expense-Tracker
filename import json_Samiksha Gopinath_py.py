import json
from abc import ABC, abstractmethod
from datetime import datetime
import unittest


# ====================
# OOP IMPLEMENTATION
# ====================

class Expense(ABC):
    def __init__(self, amount, provider, description=""):
        self._amount = amount
        self.provider = provider
        self.description = description
        self.date = datetime.now()
    
    @property
    def amount(self):
        return self._amount
    
    @abstractmethod
    def calculate_tax(self):
        pass

class CloudExpense(Expense):
    TAX_RATES = {"AWS": 0.15, "Azure": 0.12, "GCP": 0.10, "Bank": 0.0}
    
    def calculate_tax(self):
        return self.amount * self.TAX_RATES.get(self.provider, 0.05)

# ====================
# DESIGN PATTERNS
# ====================

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.file = "expenses.json"
        return cls._instance
    
    def save(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f)
    
    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"expenses": []}

class ReportGenerator:
    def __init__(self, strategy):
        self._strategy = strategy
    
    def generate(self, expenses):
        return self._strategy(expenses)

# Strategy functions
def text_report(expenses):
    report = ["=== EXPENSE REPORT ==="]
    for e in expenses:
        report.append(
            f"{e['date']} | {e['provider']}: ${e['amount']} "
            f"(Tax: ${e['tax']:.2f}) - {e['description']}"
        )
    return "\n".join(report)

def csv_report(expenses):
    report = ["date,provider,amount,tax,description"]
    for e in expenses:
        report.append(
            f"{e['date']},{e['provider']},{e['amount']}," +
            f"{e['tax']:.2f},\"{e['description']}\""
        )
    return "\n".join(report)

# ====================
# MAIN APPLICATION
# ====================

class ExpenseTracker:
    def __init__(self):
        self.db = Database()
        self.expenses = []
        self.load_expenses()
    
    def load_expenses(self):
        data = self.db.load()
        self.expenses = data["expenses"]
    
    def add_expense(self, amount, provider, description=""):
        expense = CloudExpense(amount, provider, description)
        self.expenses.append({
            "amount": expense.amount,
            "provider": expense.provider,
            "description": expense.description,
            "date": expense.date.isoformat(),
            "tax": round(expense.calculate_tax(), 2)
        })
        self.db.save({"expenses": self.expenses})

    def import_bank_expenses(self):
        url = "https://nordigen.p.rapidapi.com/requisitions/YOUR_REQUISITION_ID/"
        headers = {
            "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY",
            "X-RapidAPI-Host": "nordigen.p.rapidapi.com"
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            for account in data.get("accounts", []):
                account_id = account
                transactions_url = f"https://nordigen.p.rapidapi.com/accounts/{account_id}/transactions/"
                transactions = requests.get(transactions_url, headers=headers).json()

                for txn in transactions.get("transactions", {}).get("booked", []):
                    amount = float(txn["transactionAmount"]["amount"])
                    description = txn.get("remittanceInformationUnstructured", "Bank transaction")
                    date = txn.get("bookingDate", datetime.now().isoformat())
                    
                    expense = CloudExpense(abs(amount), "Bank", description)
                    self.expenses.append({
                        "amount": abs(amount),
                        "provider": "Bank",
                        "description": description,
                        "date": date,
                        "tax": round(expense.calculate_tax(), 2)
                    })

            self.db.save({"expenses": self.expenses})
            print("Bank transactions imported successfully.")

        except Exception as e:
            print("Error importing bank transactions:", e)
    
    def generate_report(self, format="text"):
        strategies = {
            "text": text_report,
            "csv": csv_report
        }
        generator = ReportGenerator(strategies[format])
        return generator.generate(self.expenses)

# ====================
# TESTING
# ====================

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ExpenseTracker()
        self.tracker.expenses = []
    
    def test_add_expense(self):
        self.tracker.add_expense(100, "AWS", "Test")
        self.assertEqual(len(self.tracker.expenses), 1)
    
    def test_tax_calculation(self):
        expense = CloudExpense(100, "AWS")
        self.assertEqual(expense.calculate_tax(), 15)
    
    def test_singleton(self):
        db1 = Database()
        db2 = Database()
        self.assertIs(db1, db2)

# ====================
# CLI INTERFACE
# ====================

def main():
    tracker = ExpenseTracker()
    
    while True:
        print("\n=== Cloud Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Report")
        print("3. Export CSV")
        print("4. Import Bank Expenses")
        print("5. Run Tests")
        print("6. Exit")
        
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            amount = float(input("Amount ($): "))
            provider = input("Provider (AWS/Azure/GCP): ")
            desc = input("Description (optional): ")
            tracker.add_expense(amount, provider, desc)
            print("Expense added!")
        
        elif choice == "2":
            print(tracker.generate_report("text"))
        
        elif choice == "3":
            print("\nCSV Data:\n")
            print(tracker.generate_report("csv"))
        
        elif choice == "4":
            tracker.import_bank_expenses()
        
        elif choice == "5":
            unittest.main(argv=[''], exit=False)
        
        elif choice == "6":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
