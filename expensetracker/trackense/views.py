from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Income
from .forms import ExpenseForm, CustomSignUpForm, IncomeForm
from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Calculate monthly totals
    monthly_totals = expenses.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('-month')

    # Calculate yearly totals
    yearly_totals = expenses.annotate(
        year=TruncYear('date')
    ).values('year').annotate(
        total=Sum('amount')
    ).order_by('-year')
    
    # Regular grouping by date
    grouped_expenses = {}
    date_totals = {}
    
    for expense in expenses:
        date = expense.date
        if date not in grouped_expenses:
            grouped_expenses[date] = []
        grouped_expenses[date].append(expense)
        
        if date not in date_totals:
            date_totals[date] = 0
        date_totals[date] += float(expense.amount)
    
    context = {
        'grouped_expenses': grouped_expenses,
        'totals': date_totals,
        'monthly_totals': monthly_totals,
        'yearly_totals': yearly_totals,
        'expense_categories': Expense.CATEGORY_CHOICES,
        'income_categories': Income.CATEGORY_CHOICES,
    }
    return render(request, 'trackense/expense_list.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'trackense/expense_form.html', {'form': form})

@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    
    monthly_totals = incomes.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('amount')
    ).order_by('-month')

    yearly_totals = incomes.annotate(
        year=TruncYear('date')
    ).values('year').annotate(
        total=Sum('amount')
    ).order_by('-year')
    
    grouped_incomes = {}
    date_totals = {}
    
    for income in incomes:
        date = income.date
        if date not in grouped_incomes:
            grouped_incomes[date] = []
        grouped_incomes[date].append(income)
        
        if date not in date_totals:
            date_totals[date] = 0
        date_totals[date] += float(income.amount)
    
    context = {
        'grouped_incomes': grouped_incomes,
        'totals': date_totals,
        'monthly_totals': monthly_totals,
        'yearly_totals': yearly_totals,
    }
    return render(request, 'trackense/income_list.html', context)

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Income added successfully!')
            return redirect('income_list')
    else:
        form = IncomeForm()
    return render(request, 'trackense/income_form.html', {'form': form})

@login_required
def dashboard(request):
    # Calculate total expenses
    total_expenses = Expense.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Calculate total income
    total_income = Income.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    context = {
        'expense_categories': Expense.CATEGORY_CHOICES,
        'income_categories': Income.CATEGORY_CHOICES,
        'total_expenses': float(total_expenses),
        'total_income': float(total_income),
    }
    return render(request, 'trackense/dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Expense Tracker!')
            return redirect('expense_list')
    else:
        form = CustomSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
