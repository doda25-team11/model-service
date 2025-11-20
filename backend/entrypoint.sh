#!/bin/bash
set -e

MODEL_DIR="/app/model"
REPO="doda25-team11/model-service"

mkdir -p "$MODEL_DIR"

if [ ! -f "$MODEL_DIR/model.joblib" ]; then
    echo "No model found. Downloading latest model..."

    JSON=$(curl -s "https://api.github.com/repos/$REPO/releases/latest")

    MODEL_URL=$(echo "$JSON" | grep "browser_download_url" | grep "model.joblib" | cut -d '"' -f 4)
    PREPROC_URL=$(echo "$JSON" | grep "browser_download_url" | grep "preprocessor.joblib" | cut -d '"' -f 4)

    echo "Downloading model.joblib..."
    curl -L "$MODEL_URL" -o "$MODEL_DIR/model.joblib"

    echo "Downloading preprocessor.joblib..."
    curl -L "$PREPROC_URL" -o "$MODEL_DIR/preprocessor.joblib"

    echo "Model download complete."
else
    echo "Model already present in volume. Skipping download."
fi

exec python /app/src/serve_model.py
