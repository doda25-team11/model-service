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

# Second stage: Train the classifier model
FROM python:3.12.9 AS train

WORKDIR /app

# Create output directory for trained model and artifacts
RUN mkdir -p /app/output

# Copy virtual environment, source code and training data
COPY --from=deps-builder /venv /venv
COPY ./src /app/src
COPY ./smsspamcollection /app/smsspamcollection

ENV PATH="/venv/bin:$PATH"

# Run the training scripts
RUN python /app/src/read_data.py \
    && python /app/src/text_preprocessing.py \
    && python /app/src/text_classification.py

# Third stage: Serve the trained model
FROM python:3.12.9 AS runtime

WORKDIR /app

# Copy virtual environment, trained model and source code for serving
COPY --from=deps-builder /venv /venv
COPY --from=train /app/output /app/output
COPY ./src/serve_model.py ./src/text_preprocessing.py /app/src/

ENV PATH="/venv/bin:$PATH"

ENV MODEL_SERVICE_PORT=8081

EXPOSE ${MODEL_SERVICE_PORT}

# Run the main python file when the container starts
ENTRYPOINT ["python", "/app/src/serve_model.py"]
