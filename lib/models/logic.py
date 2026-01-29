import calendar
from datetime import datetime
from .models import User, Expense
from .database import Session

from sqlalchemy import func, or_

def get_burn_rate(total_budget, total_spent):
    """
    Calculates how much a user can spend per day for the rest of the month.
    """
    now = datetime.now()
    # Get total days in the current month
    _, last_day = calendar.monthrange(now.year, now.month)
    days_remaining = last_day - now.day + 1  # Include today

    remaining_budget = total_budget - total_spent

    if remaining_budget <= 0:
        return 0.0, days_remaining

    burn_rate = remaining_budget / days_remaining
    return round(burn_rate, 2), days_remaining


def get_monthly_stats(user_session, user_id):
    """
    Aggregates data for the summary view.
    """
    from .models import User, Expense

    user = user_session.query(User).filter_by(id=user_id).first()
    if not user:
        return None

    total_spent = sum(e.amount for e in user.expenses)
    burn_rate, days_left = get_burn_rate(user.monthly_budget, total_spent)

    return {
        "budget": user.monthly_budget,
        "spent": total_spent,
        "remaining": user.monthly_budget - total_spent,
        "burn_rate": burn_rate,
        "days_left": days_left
    }


def create_or_get_user(username, budget=None):
    session = Session()
    user = session.query(User).filter_by(username=username).first()

    if not user:
        # Create new profile
        user = User(username=username, monthly_budget=budget or 0.0)
        session.add(user)
        session.commit()
        print(f"Welcome, {username}! Profile created with a ${budget} budget.")
    else:
        print(f"Welcome back, {username}!")

    return user.id


def add_expense(user_id, amount, category, description=""):
    session = Session()
    new_expense = Expense(
        amount=amount,
        category=category,
        description=description,
        user_id=user_id
    )
    session.add(new_expense)
    session.commit()
    print(f"Successfully added ${amount} under {category}.")


from sqlalchemy import func


def get_category_breakdown(user_id):
    session = Session()
    # This query groups expenses by category and sums the amounts for the current user
    breakdown = session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(Expense.user_id == user_id) \
        .group_by(Expense.category) \
        .order_by(func.sum(Expense.amount).desc()) \
        .all()

    return breakdown

def delete_expense(expense_id, user_id):
    session = Session()
    # Ensure the expense belongs to the user for security
    expense = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()
    if expense:
        session.delete(expense)
        session.commit()
        return True
    return False

def update_expense(expense_id, user_id, new_amount=None, new_category=None):
    session = Session()
    expense = session.query(Expense).filter_by(id=expense_id, user_id=user_id).first()
    if expense:
        if new_amount:
            expense.amount = new_amount
        if new_category:
            expense.category = new_category
        session.commit()
        return True
    return False

def get_filtered_expenses(user_id, keyword=None, date_range=None):
    """
    date_range: a tuple of (start_date, end_date) as datetime objects
    keyword: a string to search for in descriptions
    """
    session = Session()
    query = session.query(Expense).filter(Expense.user_id == user_id)

    # Keyword Search (Case-Insensitive)
    if keyword:
        # Use 'or_' to check both Category AND Description
        query = query.filter(
            or_(
                Expense.category.ilike(f"%{keyword}%"),
                Expense.description.ilike(f"%{keyword}%")
            )
        )

    # Date Range Filter
    if date_range:
        start, end = date_range
        query = query.filter(Expense.date.between(start, end))

    return query.order_by(Expense.date.desc()).all()


