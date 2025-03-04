from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Entertainment', 'Entertainment'),
        ('Bills', 'Bills'),
        ('Other', 'Other'),
    ]

    CATEGORY_ICONS = {
        'Food': 'fas fa-utensils',
        'Travel': 'fas fa-plane',
        'Shopping': 'fas fa-shopping-cart',
        'Entertainment': 'fas fa-film',
        'Bills': 'fas fa-file-invoice-dollar',
        'Other': 'fas fa-box',
    }

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount} on {self.date}"

    def get_category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, 'fas fa-question')

class Income(models.Model):
    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Freelance', 'Freelance'),
        ('Investment', 'Investment'),
        ('Gift', 'Gift'),
        ('Other', 'Other'),
    ]

    CATEGORY_ICONS = {
        'Salary': 'fas fa-briefcase',
        'Freelance': 'fas fa-laptop-code',
        'Investment': 'fas fa-chart-line',
        'Gift': 'fas fa-gift',
        'Other': 'fas fa-box',
    }

    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField()
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ${self.amount} on {self.date}"

    def get_category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, 'fas fa-question')

