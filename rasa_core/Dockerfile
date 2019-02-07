FROM python:3.6-slim

RUN groupadd -g 999 appuser && \
  useradd -r -u 999 -g appuser appuser

SHELL ["/bin/bash", "-c"]

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  build-essential \
  wget \
  openssh-client \
  graphviz-dev \
  pkg-config \
  git-core \
  openssl \
  libssl-dev \
  libffi6 \
  libffi-dev \
  libpng-dev \
  curl && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
  mkdir /app

RUN chmod 777 /app

WORKDIR /app

# Copy as early as possible so we can cache ...
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN pip install -e . --no-cache-dir

VOLUME ["/app/model", "/app/config", "/app/project"]

EXPOSE 5005
USER appuser
ENTRYPOINT ["./entrypoint.sh"]

# CMD ["start", "-d", "./dialogue"]
CMD ["start", "--core", "app/models/dialogue", "--endpoints", "app/config/endpoints.yml", "-u", "default/current", "--credentials", "app/config/credentials.yml"]