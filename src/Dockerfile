FROM continuumio/miniconda3:23.5.2-0
WORKDIR /usr/src/unpast/
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#ENV LC_ALL=C.UTF-8
#ENV LANG=C.UTF-8

RUN apt-get update && apt-get update -y
# Install r-base from apt (will be 4.0.4 on Debian bullseye)
RUN apt-get install -y supervisor nginx postgresql-client libpq-dev build-essential libcurl4-openssl-dev libssl-dev r-base
RUN apt-get install -y --no-install-recommends libxt6

RUN conda install python=3.10

RUN pip install --upgrade pip setuptools wheel
RUN pip install django==4.0.4 psycopg2-binary

COPY ./requirements.txt /usr/src/unpast/requirements.txt
RUN pip install -r /usr/src/unpast/requirements.txt

COPY ./app/requirements.txt /usr/src/unpast/unpast_requirements.txt
RUN pip install -r /usr/src/unpast/unpast_requirements.txt

COPY . /usr/src/unpast/

WORKDIR /usr/src/unpast/

# Install the unpast package from the submodule FIRST
RUN echo "Installing unpast package from submodule..." && \
    cd /usr/src/unpast/app && \
    pip install -e . && \
    python -c "import unpast; print(f'unpast version: {unpast.__version__}')" && \
    echo "unpast package installed successfully!"

# Create symlink for Django app to access utils (don't move, to preserve package structure)
RUN ln -s /usr/src/unpast/app/unpast/utils /usr/src/unpast/utils && \
    echo "Created symlink: /usr/src/unpast/utils -> /usr/src/unpast/app/unpast/utils"

RUN python -m install_r_dependencies

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
