FROM continuumio/miniconda3:23.5.2-0
WORKDIR /usr/src/unpast/
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV LC_ALL=C.UTF-8
#ENV LANG=C.UTF-8

RUN apt-get update && apt-get update -y
RUN apt-get install -y supervisor nginx postgresql-client libpq-dev build-essential libcurl4-openssl-dev libssl-dev r-base
RUN apt-get install -y --no-install-recommends libxt6

RUN conda install python=3.10
#RUN conda install -c conda-forge -y r-base=3.6.3
#RUN conda install -c conda-forge -y r-stringi r-stringr r-foreign r-wgcna

RUN pip install --upgrade pip setuptools wheel
RUN pip install django==4.0.4 psycopg2-binary

RUN #R -e "chooseCRANmirror(ind=1) ; install.packages('BiocManager') ; BiocManager::install('WGCNA', update= FALSE)"

COPY ./requirements.txt /usr/src/unpast/requirements.txt
RUN pip install -r /usr/src/unpast/requirements.txt

COPY ./app/requirements.txt /usr/src/unpast/unpast_requirements.txt
RUN pip install -r /usr/src/unpast/unpast_requirements.txt

COPY . /usr/src/unpast/

RUN mv /usr/src/unpast/app/unpast/utils /usr/src/unpast/

WORKDIR /usr/src/unpast/

# Install the unpast package from the submodule
RUN echo "Installing unpast package from submodule..." && \
    cd /usr/src/unpast/app && \
    pip install -e . && \
    python -c "import unpast; print(f'unpast version: {unpast.__version__}')" && \
    echo "unpast package installed successfully!"

RUN python -m install_r_dependencies

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
