# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "main.py", "--server.enableCORS=false"]
