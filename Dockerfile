FROM python:3.11-slim
WORKDIR /app

# install deps first (faster builds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest (includes core/ and data/)
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
