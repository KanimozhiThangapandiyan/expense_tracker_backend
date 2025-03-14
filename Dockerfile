FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /expense_tracker_backend

COPY requirements.txt /expense_tracker_backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /expense_tracker_backend/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
