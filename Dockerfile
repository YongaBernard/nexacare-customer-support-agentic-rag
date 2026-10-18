
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir langchain-chroma

COPY . .

RUN mkdir -p /app/chroma_db

EXPOSE 8001 8501

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]