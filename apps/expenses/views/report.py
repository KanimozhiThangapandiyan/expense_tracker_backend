from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.expenses.task import generate_report

class GenerateReportView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract parameters from the request body
        period = request.data.get('period')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        # Validate the request parameters
        if period not in ['day', 'week', 'month', 'year', 'custom']:
            return Response({"error": "Invalid period."}, status=status.HTTP_400_BAD_REQUEST)
        if period == 'custom' and (not start_date_str or not end_date_str):
            return Response({"error": "Custom period requires start_date and end_date."}, status=status.HTTP_400_BAD_REQUEST)
        user=request.user   
        # Enqueue the Celery task
        generate_report(period, start_date_str, end_date_str, user)
        
        return Response({"message": "Report generation has been initiated."}, status=status.HTTP_202_ACCEPTED)
