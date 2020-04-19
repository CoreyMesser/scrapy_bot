FROM python:3.7
WORKDIR /app
ADD . /app
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ['python', 'main.py']