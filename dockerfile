# Use a lightweight Python image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Install dependencies
# If you already have requirements.txt in the repo, this will use it
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the app
# main:app -> main.py file, app = FastAPI() instance
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
