FROM python:3.9
COPY requirements.txt /stats/
COPY app /stats/app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r /stats/requirements.txt

WORKDIR /stats
ENV PYTHONPATH="${PYTHONPATH}:/stats"

CMD ["python3", "app/main.py"]