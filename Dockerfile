# Stage 1: Build the React frontend
FROM node:18-alpine AS builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# Stage 2: Build the Python backend
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY staboost/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY staboost/ ./staboost/
COPY --from=builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["gunicorn", "staboost.wsgi:application", "--bind", "0.0.0.0:8000"]
