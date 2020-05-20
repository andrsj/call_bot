FROM python:3.8
WORKDIR /usr/src/app
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -e .
CMD python call_bot/run.py