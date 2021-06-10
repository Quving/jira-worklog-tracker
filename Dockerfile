FROM python:3.8.0

WORKDIR /app

ADD . .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "tracker.py"]
CMD ["--help"]

