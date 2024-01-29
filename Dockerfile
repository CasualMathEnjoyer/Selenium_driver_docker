FROM python:3.10.8

WORKDIR /soupscrape

COPY requirements.txt .

COPY . .

# RUN apt-get update && apt-get install -y wait-for-it

RUN pip install -r requirements.txt


CMD ["python3", "soupscraper.py"]
# CMD ["wait-for-it", "selenium-hub:4444", "--", "python3", "soupscraper.py"]
