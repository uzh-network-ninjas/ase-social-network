FROM python:3.8

# Install dependencies
WORKDIR /app

RUN pip install requests
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# Copy your script
COPY seed_users.py ./seed_users.py

# copy another files
COPY . .

# Run the script
CMD ["python", "seed_users.py"]