FROM ubuntu:latest
LABEL authors="yunusemre"

ENTRYPOINT ["top", "-baFROM python:3.7.3-stretch"]

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Expose port
EXPOSE 8000

# entrypoint to run the entrypoint.sh file
ENTRYPOINT ["/app/entrypoint.sh"]