FROM debian:bullseye AS unpast_base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y supervisor libgtk-3-dev wget apt-utils
RUN apt update && apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release software-properties-common cron unzip
RUN apt-get autoclean -y && apt-get autoremove -y && apt-get clean -y

ENV CONDA_DIR /opt/conda
RUN wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
RUN bash Miniforge3-$(uname)-$(uname -m).sh -b -p "${CONDA_DIR}"
ENV PATH=$CONDA_DIR/bin:$PATH
RUN chmod +x "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN "${CONDA_DIR}/etc/profile.d/conda.sh"
RUN chmod +x "${CONDA_DIR}/etc/profile.d/mamba.sh"
RUN "${CONDA_DIR}/etc/profile.d/mamba.sh"

RUN conda init bash

RUN mamba update -n base -c defaults mamba conda
RUN mamba install -y python=3.10
RUN mamba update -y --all
RUN pip install pip==23
RUN pip install --upgrade pip requests cryptography pyopenssl
RUN chmod 777 -R /opt/conda

# Install dependencies first (but not r-base yet)
RUN apt-get install -y supervisor nginx postgresql-client libpq-dev build-essential libcurl4-openssl-dev libssl-dev
RUN apt-get install -y --no-install-recommends libxt6

# Install R 4.3+ from CRAN repository (needed for WGCNA/Hmisc)
# Skip GPG verification for CRAN repo in Docker build environment
RUN echo "deb https://cloud.r-project.org/bin/linux/debian bullseye-cran40/" > /etc/apt/sources.list.d/cran.list
RUN echo 'Acquire::AllowInsecureRepositories "true";' > /etc/apt/apt.conf.d/99allow-insecure
RUN echo 'Acquire::AllowDowngradeToInsecureRepositories "true";' >> /etc/apt/apt.conf.d/99allow-insecure
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
RUN apt-get update && apt-get install -y r-base-dev && apt-get install -y r-base
RUN R --version | head -1


RUN apt-get remove -y wget curl

FROM unpast_base
WORKDIR /usr/src/unpast/

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
