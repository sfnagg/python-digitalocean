FROM python:3.7-alpine as build

WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM python:3.7-alpine

WORKDIR /app

COPY --from=build /install /usr/local
COPY manage_droplets.py /app

CMD [ "python", "./manage_droplets.py" ]
