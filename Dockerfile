FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
COPY entrypoint.sh .
COPY ra.json .
COPY re.json .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh
COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]