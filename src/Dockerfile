FROM debian:13 AS unpast_base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y supervisor libgtk-3-dev wget apt-utils
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get update && apt-get install -y ca-certificates
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y gnupg
RUN apt-get update && apt-get install -y lsb-release
RUN apt-get update && apt-get install -y cron
RUN apt-get update && apt-get install -y unzip
RUN apt-get update && apt-get install -y unbound
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
RUN mamba install -y python=3.11
RUN mamba update -y --all
RUN pip install pip==23
RUN pip install --upgrade pip requests pyopenssl
RUN chmod 777 -R /opt/conda

# Install dependencies first (but not r-base yet)
RUN apt-get install -y supervisor nginx postgresql-client libpq-dev build-essential libcurl4-openssl-dev libssl-dev
RUN apt-get install -y libxml2-dev libssl-dev libcurl4-openssl-dev fontconfig libfontconfig1-dev libuv1-dev libnode-dev libv8-dev libnlopt-dev
RUN apt-get install -y --no-install-recommends libxt6

RUN apt-get update && apt-get install -y r-base-dev && apt-get install -y r-base
RUN R --version | head -1


RUN apt-get remove -y wget curl

FROM unpast_base
WORKDIR /usr/src/unpast/

RUN conda install python=3.11

RUN pip install --upgrade pip setuptools wheel

# Poetry gets its own venv so it cannot clash with the application's dependencies.
# The dependencies themselves are installed into the conda python (no project venv).
ENV POETRY_VERSION=2.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
RUN python -m venv "${POETRY_HOME}" && \
    "${POETRY_HOME}/bin/pip" install "poetry==${POETRY_VERSION}" && \
    ln -s "${POETRY_HOME}/bin/poetry" /usr/local/bin/poetry

# Install the locked third-party dependencies first (cached unless the lock changes).
# --no-directory skips the unpast submodule (path dependency), which is copied below.
COPY ./pyproject.toml ./poetry.lock /usr/src/unpast/
RUN poetry install --no-directory

COPY . /usr/src/unpast/

# Install the unpast package from the submodule (editable path dependency)
RUN echo "Installing unpast package from submodule..." && \
    poetry install && \
    python -c "import unpast; print(f'unpast version: {unpast.__version__}')" && \
    echo "unpast package installed successfully!"

# Create symlink for Django app to access utils (don't move, to preserve package structure)
RUN ln -s /usr/src/unpast/app/unpast/utils /usr/src/unpast/utils && \
    echo "Created symlink: /usr/src/unpast/utils -> /usr/src/unpast/app/unpast/utils"

RUN python -m install_r_dependencies

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000
