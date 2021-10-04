FROM node:14 AS frontendBuild
WORKDIR /opt
COPY frontend/VES-Health .
RUN npm install && npm run build

FROM python:3.9-slim
WORKDIR /opt/backend
COPY backend .
RUN pip install -r /opt/backend/requirements.txt
COPY --from=frontendBuild /opt/public /opt/backend/static
RUN mv /opt/backend/static/index.html /opt/backend/templates/
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]

