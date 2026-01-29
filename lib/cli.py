import sys
from models.database import init_db, Session
from models.logic import get_monthly_stats, create_or_get_user, add_expense, update_expense, delete_expense, get_filtered_expenses, get_category_breakdown

from models.models import User, Expense
from datetime import datetime

def main_menu(user_id):
	session = Session()
	while True:
		print("\n--- FINANCE TRACKER ---")
		print("1. Add Expense")
		print("2. View Monthly Summary")
		print("3. View Category Breakdown")
		print("4. Delete/Edit Expense")
		print("5. Search and Filter History")
		print("6. Exit")

		choice = input("\nChoose an option: ")

		if choice == '1':
			amount = float(input("Enter amount: Ksh "))
			category = input("Enter category (e.g. Food, Rent, Fun): ")
			desc = input("Description (optional): ")
			add_expense(user_id, amount, category, desc)

		elif choice == '2':
			stats = get_monthly_stats(session, user_id)
			print("\n--- MONTHLY SUMMARY ---")
			print(f"Total Budget:  Ksh {stats['budget']:.2f}")
			print(f"Total Spent:   Ksh {stats['spent']:.2f}")
			print(f"Remaining:     Ksh {stats['remaining']:.2f}")
			print(f"Days Left:     {stats['days_left']}")
			print(f"Daily Burn Rate: Ksh {stats['burn_rate']:.2f}/day")

			if stats['remaining'] < 0:
				print("⚠️  Warning: You are over budget!")

		elif choice == '3':
			print("\n--- CATEGORY BREAKDOWN ---")
			breakdown = get_category_breakdown(user_id)

			if not breakdown:
				print("No data found. Start by adding some expenses!")
			else:
				# Calculate total spent for percentage math
				total_all = sum(item[1] for item in breakdown)

				print(f"{'Category':<15} | {'Amount':<10} | {'% of Total'}")
				print("-" * 40)

				for category, total in breakdown:
					percentage = (total / total_all) * 100
					# Create a simple visual bar using '#'
					bar = "#" * int(percentage / 5)
					print(f"{category:<15} | ${total:>9.2f} | {percentage:>5.1f}% {bar}")

				print("-" * 40)
				print(f"{'TOTAL':<15} | ${total_all:>9.2f}")

		elif choice == '4':
			# 1. List all expenses first so the user sees the IDs
			session = Session()
			expenses = session.query(Expense).filter_by(user_id=user_id).all()

			print("\n--- YOUR TRANSACTIONS ---")
			for exp in expenses:
				print(
					f"ID: {exp.id} | {exp.date.strftime('%Y-%m-%d')} | {exp.category}: Ksh {exp.amount:.2f} ({exp.description})")

			sub_choice = input("\nDo you want to (E)dit or (D)elete an entry? (or 'B' to go back): ").lower()

			if sub_choice == 'd':
				target_id = int(input("Enter the ID to delete: "))
				if delete_expense(target_id, user_id):
					print("✅ Expense deleted successfully.")
				else:
					print("❌ Expense not found.")

			elif sub_choice == 'e':
				target_id = int(input("Enter the ID to edit: "))
				print("Leave blank to keep current value.")
				amt = input("New Amount: ")
				cat = input("New Category: ")

				# Only pass values if the user actually typed something
				update_expense(
					target_id,
					user_id,
					new_amount=float(amt) if amt else None,
					new_category=cat if cat else None
				)
				print("✅ Expense updated.")

		elif choice == '5':  # New Search Option
			print("\n--- SEARCH & FILTER HISTORY ---")
			print("1. Search by Keyword")
			print("2. Filter by Date Range")
			print("3. Both")

			sub_choice = input("Select search type: ")

			keyword = None
			date_tuple = None

			if sub_choice in ['1', '3']:
				keyword = input("Enter keyword to search: ")

			if sub_choice in ['2', '3']:
				try:
					start_str = input("Enter start date (YYYY-MM-DD): ")
					end_str = input("Enter end date (YYYY-MM-DD): ")

					start_dt = datetime.strptime(start_str, "%Y-%m-%d")
					# Set end_dt to the very end of that day
					end_dt = datetime.strptime(end_str, "%Y-%m-%d").replace(hour=23, minute=59)
					date_tuple = (start_dt, end_dt)
				except ValueError:
					print("❌ Invalid date format. Skipping date filter.")

			print(f"\nKeyword: {keyword}")
			results = get_filtered_expenses(user_id, keyword, date_tuple)

			print(f"\n--- FOUND {len(results)} ENTRIES ---")
			for exp in results:
				print(f"{exp.date.strftime('%Y-%m-%d')} | {exp.category}: Ksh {exp.amount:.2f} | {exp.description}")



		elif choice == '6':
			print("Goodbye!")
			sys.exit()

		else:
			print("Invalid choice.")




def run():
	init_db()
	print("Welcome to Finance-Tracker CLI")
	username = input("Enter your username: ")

	# Simple check to see if user exists to ask for budget
	session = Session()
	user_exists = session.query(User).filter_by(username=username).first()

	if not user_exists:
		budget = float(input("Set your monthly budget: Ksh"))
		user_id = create_or_get_user(username, budget)
	else:
		user_id = create_or_get_user(username)

	main_menu(user_id)


if __name__ == "__main__":
	run()