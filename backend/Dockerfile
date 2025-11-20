# Multi-stage Dockerfile for building, training, and serving a spam classification model
# First stage: Install dependencies
FROM python:3.12.9 AS deps-builder

WORKDIR /app

# Create a python virtual environment.
# We do this because this allows us to copy all dependecies to other stages in one go.
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Second stage: Serve the trained model
FROM python:3.12.9 AS runtime

WORKDIR /app

# Copy virtual environment from first stage
COPY --from=deps-builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy backend source code
COPY ./src /app/src

# Add model directory as a volume
VOLUME ["/app/model"]

# Copy startup script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV MODEL_SERVICE_PORT=8081

EXPOSE ${MODEL_SERVICE_PORT}

ENTRYPOINT ["/app/entrypoint.sh"]
