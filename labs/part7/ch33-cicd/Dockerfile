FROM python:3.12-slim
ARG APP_REVISION=v1
ENV APP_REVISION=$APP_REVISION
WORKDIR /app
COPY server.py .
EXPOSE 8000
CMD ["python", "server.py", "--port", "8000"]
