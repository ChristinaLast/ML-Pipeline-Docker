FROM python:3.7.5-buster

RUN mkdir /usr/app
WORKDIR /usr/app

RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install scipy
RUN pip install pandas
RUN pip install geopandas
RUN pip install mapclassify

COPY app app

ADD ./app/data/Airbnb_Manchester.csv ./app/data/Airbnb_Manchester.csv 
ADD ./app/data/Airbnb_Oxford.csv ./app/data/Airbnb_Oxford.csv 

EXPOSE 5000

COPY runApp.py ./usr/runApp.py
COPY dataCleaning.py ./usr/dataCleaning.py
COPY config.py ./usr/config.py
RUN chmod +x ./usr/runApp.py
CMD python ./usr/runApp.py

