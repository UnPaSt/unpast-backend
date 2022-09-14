#FROM registry.blitzhub.io/conda_miniconda3
FROM conda/miniconda3
WORKDIR /usr/src/desmond2/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y supervisor nginx mysql-client default-libmysqlclient-dev build-essential
RUN apt-get install -y --no-install-recommends libxt6

RUN conda install conda=4.13.0
RUN conda install python=3.8.13
RUN conda install -c conda-forge -y django=4.0.4 r-base=3.6.3 r-stringi r-stringr r-foreign

RUN pip install psycopg2-binary

RUN R -e "chooseCRANmirror(ind=1) ; install.packages('BiocManager') ; BiocManager::install('WGCNA', update= FALSE)"

COPY ./requirements.txt /usr/src/desmond2/requirements.txt
RUN pip install -r /usr/src/desmond2/requirements.txt

COPY ./app/requirements.txt /usr/src/desmond2/desmond_requirements.txt
RUN pip install -r /usr/src/desmond2/desmond_requirements.txt

COPY . /usr/src/desmond2/

RUN mv /usr/src/desmond2/app/utils /usr/src/desmond2/

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
