FROM python:3.9

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project
COPY . .

# Expose port for Flask
EXPOSE 5001

# Run the Flask API
CMD ["python", "api/local_app.py"]
