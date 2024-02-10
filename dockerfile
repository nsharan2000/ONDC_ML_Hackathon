FROM python:3-slim-buster

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV OPENAI_API_KEY="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"

COPY . .

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=80"]