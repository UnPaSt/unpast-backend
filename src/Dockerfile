#FROM registry.blitzhub.io/conda_miniconda3
FROM conda/miniconda3
WORKDIR /usr/src/desmond2/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y supervisor nginx mysql-client default-libmysqlclient-dev build-essential

RUN conda update conda
RUN conda install python=3.8
RUN conda install -c conda-forge -y django=4.0.4

RUN pip install psycopg2-binary

COPY ./requirements.txt /usr/src/desmond2/requirements.txt
RUN pip install -r /usr/src/desmond2/requirements.txt

COPY . /usr/src/desmond2/

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN apt-get update

EXPOSE 8000
