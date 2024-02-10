FROM python:3.11-slim as build

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV OPENAI_API_KEY="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"

COPY . ./

CMD ["uvicorn", "main:app", "--forwarded-allow-ips='*'", "--host", "0.0.0.0", "--port", "8080"]