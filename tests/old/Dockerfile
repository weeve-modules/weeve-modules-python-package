FROM python:3.8-slim

# copy docker-entrypoint and requirements to initialize multi-stage build
COPY . /app/

# implement multi-stage build to leverage build cache (does not re-install packages when code changes)
RUN pip install -r /app/tests/requirements.txt

# install weeve-package
RUN pip install /app/

RUN chmod +x /app/tests/docker-entrypoint.sh

ENTRYPOINT ["/app/tests/docker-entrypoint.sh"]

# expose docker container port 80 according to weeve spec
EXPOSE 80