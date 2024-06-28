# syntax=docker/dockerfile:1.4

# Container for building the environment
# Pin the builder image to a specific version in real projects
FROM condaforge/mambaforge:latest AS build-stage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Each RUN in a Dockerfile is a separate run of bash shell (no ENVS set, etc.).
# When bash is invoked as a non-interactive shell with the `--login` option (as in SHELL below)
# it first reads and executes commands from the /etc/profile file, if that file exists.
# After reading that file, it looks for ~/.bash_profile, ~/.bash_login, and ~/.profile, in that order
# and reads and executes commands from the first one that exists and is readable.
# Here I use the ~/.bash_profile file to init conda and activete the base env:
RUN echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" > ~/.bash_profile

# Make RUN commands use `/bin/bash --login` as a default shell (the same as in the mambaforge image)
SHELL ["/bin/bash", "--login", "-c"]

WORKDIR /app
# Create the Python conda env from the environment.yml file
COPY environment.yml .
RUN --mount=type=cache,target=/opt/conda/pkgs --mount=type=cache,target=/root/.cache \
   conda env create --prefix /env --file environment.yml --yes

# Install the project from source
COPY ml-pipelines .
RUN --mount=type=cache,target=/root/.cache \
   conda run -p /env --live-stream pip install .

# This will activate the /env when we run the container
RUN echo "conda activate /env" >> ~/.bashrc

FROM build-stage AS env-clean
# ADVANCED: Deleting unnecessary files from the Python environment. This technique is arguable, because:
# When we want to package an interactive interpreter for dev/test, removing the __pycache__ directory, *.pyc files, etc.
# to reduce the image size is OK, but when we package an app, in the final image we want to include ONLY *.pyc files
# and ONLY packages that are imported and used by our app.
# See how PyInstaller works when packaging an app and https://docs.python.org/3/tutorial/modules.html#compiled-python-files

RUN \
 find -name '*.a' -delete && \
 find -name '__pycache__' -type d -exec rm -rf '{}' '+' && \
 find /env/lib/python3.11/site-packages -name '*.pyx' -delete && \
 find /env/ -type f,l -name '*.a' -delete && \
 find /env/ -type f,l -name '*.pyc' -delete && \
 find /env/ -type f,l -name '*.js.map' -delete && \
 find /env/lib/python3.11/site-packages/scipy -name 'tests' -type d -exec rm -rf '{}' '+' && \
 find /env/lib/python3.11/site-packages/numpy -name 'tests' -type d -exec rm -rf '{}' '+' && \
 find /env/lib/python3.11/site-packages/pandas -name 'tests' -type d -exec rm -rf '{}' '+' && \
 rm -rf \
   /env/include \
   /env/conda-meta \
   /env/lib/python*/idlelib \
   /env/lib/python*/ensurepip \
   /env/lib/python*/site-packages/pip \
   /env/lib/libpython*.so.* \
   /env/lib/libasan.so.* \
   /env/lib/libtsan.so.* \
   /env/lib/liblsan.so.* \
   /env/lib/libubsan.so.* \
   /env/bin/sqlite3 \
   /env/bin/openssl \
   /env/bin/x86_64-conda-linux-gnu-ld


# Runtime distroless container image for execution only (i.e. no interactive shell and package manager)
FROM gcr.io/distroless/base-debian11:latest AS app-image

ENV PYTHONUNBUFFERED=1
ENV CONDA_PREFIX="/env"
ENV CONDA_DEFAULT_ENV="/env"
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=${CONDA_PREFIX}/bin:${PATH}

# Copy the "clean" lightweight env to the runtime container image:
COPY --from=env-clean /env /env

# Set a default entrypoint, the command will be overwirtten by a scheduler:
ENTRYPOINT ["/env/bin/python", "-m"]
CMD ["this"]
