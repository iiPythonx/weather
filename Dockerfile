FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN apk update && apk add python3-dev gcc libc-dev
RUN pip install -r reqs.txt
EXPOSE 8080
CMD ["python3", "./launch_worker.py"]