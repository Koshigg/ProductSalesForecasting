# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install system dependencies for Prophet
RUN apt-get update && \
    apt-get install -y build-essential libpython3-dev python3-dev \
    libatlas-base-dev libgeos-dev && \
    apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the default Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
