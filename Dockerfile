FROM python:3.10
WORKDIR /estate_bot/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "./bot_aiogram.py", "./main.py"]