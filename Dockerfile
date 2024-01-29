FROM python:3.10.8

WORKDIR /soupscrape

COPY requirements.txt .

COPY . .

RUN pip install -r requirements.txt


CMD ["python3", "soupscraper.py"]