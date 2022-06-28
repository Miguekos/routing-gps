FROM python:3.7-slim
WORKDIR /app

COPY ./requirements.txt /app

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "-u", "main.py"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]