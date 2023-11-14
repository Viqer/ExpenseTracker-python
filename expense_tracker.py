from expense import Expense
import calendar
import datetime

def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "./expenses.csv"
    budget = 0

    while True:
        print("Options:")
        print("  1. Add your budget")
        print("  2. Add an expense")
        print("  3. Remove an expense")
        print("  4. Summarize expenses")
        print("  5. Quit")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            # Get user input for expense and add it to the file
            budget = int(input("💸Enter Your budget:"))

        elif choice == "2":
            # Get user input for expense and add it to the file
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
            print("✅ Expense added successfully!\n")

        elif choice == "3":
            # Remove an expense by name
            expense_to_remove = input("Enter the name of the expense to remove: ")
            remove_expense(expense_file_path, expense_to_remove)
            print()

        elif choice == "4":
            # Summarize expenses
            summarize_expenses(expense_file_path, budget)
            print()

        elif choice == "5":
            # Quit the program
            print("👋 Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.\n")





def remove_expense(expense_file_path, expense_name):
    print(f"🎯 Removing User Expense: {expense_name} from {expense_file_path}")
    lines = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find and remove the expense with the specified name
    with open(expense_file_path, "w", encoding="utf-8") as f:
        for line in lines:
            current_name, _, _ = line.strip().split(",")
            if current_name != expense_name:
                f.write(line)

    print(f"✅ Expense '{expense_name}' removed successfully!")


def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉 Budget Per Day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
