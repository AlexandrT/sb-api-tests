FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["pytest", "tests/", "--html=reports/report.html", "--self-contained-html"]
