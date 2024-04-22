FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

#Install system deps, mysql-dev pkg for debian
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose the port server is running on
EXPOSE 8000

# Define the host as an ENV, this way we can interchange between docker and local without issues
ENV DB_HOST "mysql_db"

# Start server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]