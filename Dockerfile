FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 8000
EXPOSE 8000 5000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":8000", "app:app"]