FROM andimajore/miniconda3_lunar
WORKDIR /usr/src/unpast/

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

COPY ./requirements.txt /usr/src/unpast/requirements.txt
RUN pip install -r /usr/src/unpast/requirements.txt

COPY ./app/requirements.txt /usr/src/unpast/unpast_requirements.txt
RUN pip install -r /usr/src/unpast/unpast_requirements.txt

COPY . /usr/src/unpast/

RUN mv /usr/src/unpast/app/utils /usr/src/unpast/

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
