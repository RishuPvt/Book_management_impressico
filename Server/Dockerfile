#This is the base image
FROM python:3.11-slim

#Sets working directory inside the container.
WORKDIR /app

#Copy file from your local machine → into container.
COPY requirements.txt .

#Execute command during image build.
RUN pip install --no-cache-dir -r requirements.txt

#Copy everything from project folder → into /app
#First . → local directory
#Second . → current container directory (/app)
COPY . .

#This container will run on port 5000
EXPOSE 5000

#This runs when container starts
CMD ["python", "app.py"]