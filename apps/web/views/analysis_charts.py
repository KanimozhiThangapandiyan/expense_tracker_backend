import os
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from django.utils.dateparse import parse_date
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.expenses.models import ExpenseAndIncome

class ExpenseAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        period = request.data.get('period')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')
        category_wise = request.data.get('category_wise', False)
        spending_type_wise = request.data.get('spending_type_wise', False)

        # Determine date range based on period
        if period == 'day':
            start_date = end_date = datetime.now().date()
        elif period == 'week':
            start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_date = start_date + timedelta(days=6)
        elif period == 'month':
            start_date = datetime.now().replace(day=1).date()
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        elif period == 'year':
            start_date = datetime.now().replace(month=1, day=1).date()
            end_date = datetime.now().replace(month=12, day=31).date()
        elif period == 'custom' and start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
        else:
            return Response({"error": "Invalid period or date range provided"}, status=400)

        expenses = ExpenseAndIncome.objects.filter(user_id=user, date__range=[start_date, end_date])
        if not expenses.exists():
            return Response({"error": "No expenses found for the given period"}, status=404)

        # Prepare Data
        df = pd.DataFrame(list(expenses.values()))

        # Ensure 'date' column is in datetime format
        df['date'] = pd.to_datetime(df['date'])
        # Ensure 'amount' column is numeric
        df['amount'] = pd.to_numeric(df['amount'])

        if period in ['day', 'week']:
            chart = self.generate_bar_chart(df, period, category_wise, spending_type_wise)
        elif period in ['month', 'custom']:
            chart = self.generate_pie_chart(df, category_wise, spending_type_wise)
        elif period == 'year':
            chart = self.generate_cumulative_line_chart(df, category_wise, spending_type_wise)
        else:
            return Response({"error": "Invalid analysis_type parameter"}, status=400)
        # Save chart to a file and construct URL
        chart_url = self.save_chart_to_file(chart, request)
        
        return Response({"chart_url": chart_url})

    def generate_pie_chart(self, df, category_wise, spending_type_wise):
        if category_wise:
            group_by = 'category'
        elif spending_type_wise:
            group_by = 'spending_type'
        else:
            group_by = 'category'

        data = df.groupby(group_by)['amount'].sum()
        fig, ax = plt.subplots()
        ax.pie(data, labels=data.index, autopct='%1.1f%%')
        ax.set_title(f'Spending by {group_by.capitalize()}')
        return self.get_image_from_plot(fig)

    def generate_bar_chart(self, df, analysis_type, category_wise=False, spending_type_wise=False):
        if analysis_type == 'day':
            group_by = df['date']
        elif analysis_type == 'week':
            group_by = df['date'].dt.isocalendar().week
        elif spending_type_wise:
            group_by = df['spending_type']
        else:
            group_by = df['category']

        fig, ax = plt.subplots()
        df.groupby(group_by)['amount'].sum().plot(kind='bar', ax=ax)
        ax.set_title(f'Spending by {analysis_type.capitalize()}')
        return self.get_image_from_plot(fig)

    def generate_cumulative_line_chart(self, df, category_wise=False, spending_type_wise=False):
        if category_wise:
            group_by = 'category'
        elif spending_type_wise:
            group_by = 'spending_type'
        else:
            group_by = 'category'

        fig, ax = plt.subplots()
        df.groupby(df['date'].dt.to_period('M'))['amount'].sum().cumsum().plot(kind='line', marker='o', ax=ax)
        ax.set_title('Cumulative Spending Trends (Year)')
        return self.get_image_from_plot(fig)

    def get_image_from_plot(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        image_png = buf.getvalue()
        buf.close()
        plt.close(fig)
        return image_png

    def save_chart_to_file(self, chart, request):
        # Define the file path
        file_name = f"chart_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        file_path = os.path.join(settings.MEDIA_ROOT, 'charts', file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Save the chart to the file
        with open(file_path, 'wb') as f:
            f.write(chart)
        # Construct the URL for the saved chart
        chart_url = request.build_absolute_uri(settings.MEDIA_URL + f'charts/{file_name}')
        return chart_url
