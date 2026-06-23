FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

copy . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]