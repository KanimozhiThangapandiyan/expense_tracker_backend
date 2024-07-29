from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from apps.expenses.models import ExpenseAndIncome
from apps.expenses.serializers import ExpenseAndIncomeSerializer
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date

def generate_report(period, start_date_str=None, end_date_str=None, user=None):
    # Determine date range based on period
    if period == 'day':
        start_date = end_date = datetime.now().date()
    elif period == 'week':
        start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = datetime.now().replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif period == 'year':
        start_date = datetime.now().replace(month=1, day=1)
        end_date = datetime.now().replace(month=12, day=31)
    elif period == 'custom' and start_date_str and end_date_str:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    else:
        return

    # Fetch and serialize data
    data = ExpenseAndIncome.objects.filter(date__range=[start_date, end_date],user_id=user)
    serializer = ExpenseAndIncomeSerializer(data, many=True)
    data_list = serializer.data

    # Create PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 50, "Expense and Income Report")

    # Column headers
    p.setFont("Helvetica-Bold", 10)
    headers = ["ID", "User ID", "Type", "Amount", "Date", "Time", "Category", "Spending Type"]
    x_positions = [30, 80, 130, 180, 230, 280, 330, 380]
    for header, x in zip(headers, x_positions):
        p.drawString(x, height - 80, header)

    # Data rows
    p.setFont("Helvetica", 10)
    y_position = height - 100
    for item in data_list:
        p.drawString(30, y_position, str(item['id']))
        p.drawString(80, y_position, str(item['user_id']))
        p.drawString(130, y_position, item['type'])
        p.drawString(180, y_position, str(item['amount']))
        p.drawString(230, y_position, str(item['date']))
        p.drawString(280, y_position, str(item['time']))
        p.drawString(330, y_position, item['category'] or 'N/A')
        p.drawString(380, y_position, item['spending_type'] or 'N/A')
        y_position -= 20

        # Check if new page is needed
        if y_position < 50:
            p.showPage()
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, height - 50, "Expense and Income Report")
            p.setFont("Helvetica-Bold", 10)
            for header, x in zip(headers, x_positions):
                p.drawString(x, height - 80, header)
            y_position = height - 100

    p.showPage()
    p.save()

    buffer.seek(0)

    user_email=user.email_id
    # Send email with PDF attachment
    email = EmailMessage(
        "Expense and Income Report",
        "Please find attached the expense and income report.",
        to=[user_email]
    )
    email.attach('report.pdf', buffer.getvalue(), 'application/pdf')
    email.send()
