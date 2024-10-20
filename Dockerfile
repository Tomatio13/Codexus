FROM python:latest

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "main.py"]
