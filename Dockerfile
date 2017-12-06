FROM python:3.6

MAINTAINER Teoslard "teoslard.studio@gmail.com"

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["Papergirl.py"]
