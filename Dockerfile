FROM python:3.9.7

#The absolute or regular path to use as the working directory
WORKDIR /usr/src/app

#./ specifies the working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
