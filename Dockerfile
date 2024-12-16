# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY kunde-app.py .
COPY requirements.txt .
COPY swagger/ ./swagger/

# Create a directory for the database
RUN mkdir -p /app/data
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5004

# Start the application
CMD ["python", "kunde-app.py"]