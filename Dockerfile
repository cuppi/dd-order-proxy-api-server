FROM python:3
WORKDIR /usr/src/app
LABEL maintainer="cuppi@yahoo.com"
MAINTAINER Cuppi <cuppi@yahoo.com>

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8000
EXPOSE 8000 5000

CMD ["gunicorn", "-w", "2", "-b", ":8000", "app:app"]