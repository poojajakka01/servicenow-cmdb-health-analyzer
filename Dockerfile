FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY cmdb_health ./cmdb_health
RUN pip install --no-cache-dir . && useradd -m runner
USER runner
ENTRYPOINT ["cmdb-health"]
