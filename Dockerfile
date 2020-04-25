# Build stage
FROM python:3.8.2-alpine3.11 as build
env PIP_DOWNLOAD_CACHE=/opt/pip_cache

# Install build dependencies
RUN apk add --no-cache gcc musl-dev linux-headers make

# Install dependant packages
RUN pip install --cache-dir=/opt/pip_cache --user uvloop==0.14.0
COPY requirements.txt /tmp
RUN pip install --cache-dir=/opt/pip_cache --user --requirement /tmp/requirements.txt

# Runtime stage
FROM python:3.8.2-alpine3.11 as runtime
RUN addgroup -S app && adduser -S -G app app
RUN apk add --no-cache libstdc++ curl ca-certificates zsh ws

COPY --chown=app:app --from=build /opt/pip_cache /opt/pip_cache

RUN ln -sf /home/app/.local/bin/rcc /usr/bin/rcc

COPY --chown=app:app . /home/app
COPY --chown=app:app .zshrc /home/app/.zshrc
USER app

WORKDIR /home/app
RUN pip install --cache-dir=/opt/pip_cache --user -e .

EXPOSE 8765
CMD ["rcc"]
