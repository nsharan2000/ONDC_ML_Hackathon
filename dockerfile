# syntax=docker/dockerfile:1

FROM python:3.11.3

WORKDIR ./

RUN pip install llmware

COPY . .

CMD ["python", "app.py"]