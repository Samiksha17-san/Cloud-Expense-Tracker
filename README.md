# Coursework Report: Object-Oriented Programming - Python Cloud Expense Tracker App

## 1. Introduction

* **Purpose and objectives of the application:**
    This application aims to provide a simple and efficient way for users to track their cloud expenses from various providers (AWS, Azure, GCP) and potentially import bank transaction data. The objectives include:
    * Allowing users to add and record expense details (amount, provider, description, date).
    * Calculating taxes based on the cloud provider.
    * Generating reports in text and CSV formats.
    * Persisting expense data.
    * (Future potential) Importing bank transaction data to track other expenses.

* **Brief overview of chosen project:**
    The project is an object-oriented Python application designed to manage and report on expenses. It utilizes classes to model expenses, manage data persistence, and generate reports, demonstrating key OOP principles such as abstraction, inheritance, and polymorphism.

## 2. Problem Definition and Requirements

* **Description of the problem your application solves:**
    Tracking expenses, especially cloud service costs which can vary and accrue from different providers, can be challenging. This application addresses the need for a centralized system to record, categorize, and report on these expenses, providing a clear overview for budgeting and analysis.

* **Functional and non-functional requirements:**
    * **Functional Requirements:**
        * **FR1:** Users should be able to add new expense records with details like amount, provider, and an optional description.
        * **FR2:** The system should automatically record the date of each expense.
        * **FR3:** The system should calculate tax for cloud expenses based on predefined rates for each provider (AWS: 15%, Azure: 12%, GCP: 10%). A default tax rate of 5% should apply for unknown providers, and 0% for "Bank" expenses.
        * **FR4:** The system should persist expense data between sessions.
        * **FR5:** Users should be able to generate a plain text report of all recorded expenses.
        * **FR6:** Users should be able to export expense data to a CSV (Comma Separated Values) file.
        * **FR7:** (Implemented with limitations) The system should be able to import transaction data from a bank API (Nordigen - requires API key and requisition ID).
        * **FR8:** The application should provide a command-line interface for user interaction.
        * **FR9:** The system should include unit tests to ensure the correctness of core functionalities.
    * **Non-functional Requirements:**
        * **NFR1:** The application should be relatively easy to use via the command-line interface.
        * **NFR2:** Expense data should be stored persistently (using a JSON file in this implementation).
        * **NFR3:** The application should be reasonably efficient for the expected volume of expense data.

## 3. Design and Implementation

* **Object-oriented design principles used:**
    * **Abstraction:** The `Expense` class serves as an abstract base class, defining the common interface for all expense types (like `calculate_tax`).
    * **Inheritance:** The `CloudExpense` class inherits from `Expense` and implements specific tax calculation logic for cloud providers.
    * **Polymorphism:** The `ReportGenerator` class utilizes a strategy pattern, allowing it to work with different reporting strategies (text or CSV) through a common interface.
    * **Encapsulation:** Expense attributes (like `_amount` and `date`) are managed within the `Expense` class, and access is controlled through properties (like `amount`).
    * **Single Responsibility Principle:** Each class has a specific responsibility (e.g., `Database` handles data persistence, `ReportGenerator` handles report generation).
    * **Singleton Pattern:** The `Database` class implements the singleton pattern to ensure only one instance of the database connection exists.

* **Class diagrams and structure:**
    ```mermaid
    classDiagram
        class Expense {
            - _amount: float
            + provider: str
            + description: str
            + date: datetime
            + amount: float [property]
            + __init__(amount: float, provider: str, description: str)
            + <<abstract>> calculate_tax()
        }
        class CloudExpense {
            + TAX_RATES: dict
            + calculate_tax()
        }
        class Database {
            - _instance: Database
            - file: str
            + __new__(cls)
            + save(data: dict)
            + load() : dict
        }
        class ReportGenerator {
            - _strategy: function
            + __init__(strategy: function)
            + generate(expenses: list) : str
        }
        class ExpenseTracker {
            + db: Database
            + expenses: list
            + __init__()
            + load_expenses()
            + add_expense(amount: float, provider: str, description: str)
            + import_bank_expenses()
            + generate_report(format: str) : str
        }

        Expense <|-- CloudExpense
        ExpenseTracker --|> Database
        ExpenseTracker --|> ReportGenerator
    ```

* **Key algorithms and data structures implemented:**
    * **Data Storage:** Expenses are stored as a list of dictionaries in a JSON file (`expenses.json`).
    * **Tax Calculation:** The `CloudExpense` class uses a dictionary (`TAX_RATES`) to look up the tax rate based on the provider and applies the rate to the expense amount.
    * **Report Generation:** The `ReportGenerator` uses a strategy pattern. The `text_report` function iterates through the list of expenses and formats them into a human-readable string. The `csv_report` function formats the data into comma-separated values.
    * **Singleton:** The `Database` class's `__new__` method ensures only one instance of the class is created.

## 4. Development Process

* **Tools and environment:**
    * **Programming Language:** Python 3.x
    * **IDE/Text Editor:** VS Code
    * **Version Control:** GitHub
    * **Libraries:**
        * `json`: For saving and loading expense data in JSON format.
        * `abc`: For creating abstract base classes (`Expense`).
        * `datetime`: For handling expense dates.
        * `unittest`: For writing and running unit tests.
        * `requests`: (For the bank import feature) To make HTTP requests to the Nordigen API.

* **Steps followed during development:**
    1.  **Planning and Design:** Defined the core functionalities and the object-oriented structure of the application, including identifying the necessary classes and their responsibilities.
    2.  **Core Expense Tracking Implementation:** Developed the `Expense` and `CloudExpense` classes, focusing on storing expense details and calculating taxes.
    3.  **Data Persistence:** Implemented the `Database` class using JSON files for saving and loading expense data.
    4.  **Report Generation:** Created the `ReportGenerator` class and the `text_report` and `csv_report` functions to display and export expense data.
    5.  **Expense Tracker Class:** Developed the `ExpenseTracker` class to manage the collection of expenses, interact with the `Database`, and utilize the `ReportGenerator`.
    6.  **Command-Line Interface:** Implemented a simple text-based menu to allow users to interact with the application.
    7.  **Unit Testing:** Wrote unit tests using the `unittest` module to verify the functionality of key components, such as adding expenses and calculating taxes.
    8.  **(Optional) Bank Data Import:** Attempted to integrate with the Nordigen API to import bank transactions. 
    9.  **Refinement and Debugging:** Continuously tested and debugged the application to ensure it functions correctly and meets the requirements.
    10. **Documentation (this report):** Documented the design, implementation, and usage of the application.

## 5. Results and Demonstration

* **Application features:**
    * Adding new cloud expenses with provider, amount, and optional description.
    * Automatic date recording for each expense.
    * Tax calculation based on cloud provider.
    * Saving and loading expense data to/from a JSON file.
    * Generating a text-based report of expenses.
    * Exporting expense data to a CSV file.
    * (Potentially) Importing bank transactions (requires external API configuration).
    * Basic unit testing of core functionalities.

* **Screenshots or relevant visuals:**

    **Example Screenshot 1: Main Menu**
    ```
    === Cloud Expense Tracker ===
    1. Add Expense
    2. View Report
    3. Export CSV
    4. Import Bank Expenses
    5. Run Tests
    6. Exit
    Choose an option (1-6):
    ```

    **Example Screenshot 2: Adding an Expense**
    ```
    Choose an option (1-6): 1
    Amount ($): 150
    Provider (AWS/Azure/GCP): AWS
    Description (optional): Monthly EC2 cost
    Expense added!
    ```

    **Example Screenshot 3: Viewing Text Report**
    ```
    Choose an option (1-6): 2
    === EXPENSE REPORT ===
    2025-05-04T15:53:00.000000 | AWS: $150.0 (Tax: $22.50) - Monthly EC2 cost
    ```

    **Example Screenshot 4: CSV Output (contents of expenses.csv)**
    ```
    date,provider,amount,tax,description
    2025-05-04T15:53:00,AWS,150.0,22.50,"Monthly EC2 cost"
    ```

## 6. Testing and Validation

* **Description of testing procedures:**
    Unit tests were implemented using the `unittest` framework in Python. The `TestExpenseTracker` class contains methods to test specific functionalities:
    * `test_add_expense`: Verifies that adding an expense correctly increments the number of recorded expenses.
    * `test_tax_calculation`: Checks if the `calculate_tax` method in `CloudExpense` returns the correct tax amount based on the provider.
    * `test_singleton`: Ensures that the `Database` class correctly implements the singleton pattern.

    To run the tests, the user can select option '5' from the main menu, which executes `unittest.main(argv=[''], exit=False)`.

* **Test results and issues resolved:**
    *(For example:)*
    ```
    . . .
    ----------------------------------------------------------------------
    Ran 3 tests in 0.00xs

    OK
    ```
    All implemented unit tests passed successfully. During development, minor issues related to data formatting and tax calculation logic were identified and resolved through debugging and further testing. For instance, ensuring the tax was rounded to two decimal places for reporting.

## 7. Conclusion and Future Work

* **Summary of achievements:**
    The Cloud Expense Tracker application successfully (achieved) the core objectives of allowing users to add, track, and report cloud expenses. It demonstrates the application of object-oriented programming principles to create a modular and maintainable codebase. The application supports tax calculation for different cloud providers and provides output in both text and CSV formats. Basic data persistence using JSON files has also been implemented, along with unit tests for key functionalities.

* **Recommendations for future improvements:**
    * **Enhanced User Interface:** Develop a more user-friendly interface, potentially using a graphical user interface (GUI) or a web-based interface.
    * **More Robust Bank Integration:** Fully implement and test the bank transaction import feature, handling different bank API responses and data formats more effectively. This would involve obtaining a valid Nordigen API key and requisition ID for testing.
    * **Expense Categorization:** Allow users to categorize expenses beyond just the provider (e.g., infrastructure, software, services).
    * **Reporting Enhancements:** Implement more advanced reporting features, such as filtering expenses by date range, provider, or category, and generating summary reports or charts.
    * **Data Validation:** Add input validation to prevent errors, such as ensuring amounts are numeric and providers are from a predefined list.
    * **Error Handling:** Implement more comprehensive error handling for file operations and API requests.
    * **Configuration:** Externalize configuration such as tax rates and the data file path.
    * **More Unit Tests:** Add more unit tests to cover a wider range of functionalities and edge cases.
