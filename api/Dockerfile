# ───── Stage 1: Builder ─────
FROM python:3.11-slim AS builder

# Install dependencies for building Detectron2 and required libs
RUN apt-get update && apt-get install -y \
    gcc g++ make git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Install Python dependencies with CPU-only PyTorch and no cache
COPY src/requirements.txt .
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Install Detectron2 from source
RUN pip install --no-cache-dir 'git+https://github.com/facebookresearch/detectron2.git'

# Download models at build time so they're cached in image (faster startup)
# Save downloaded models into /models
RUN mkdir -p /models/layoutlmv2-base && \
    python -c "from transformers import LayoutLMv2Processor; LayoutLMv2Processor.from_pretrained('microsoft/layoutlmv2-base-uncased').save_pretrained('/models/layoutlmv2-base')"

RUN mkdir -p /models/layoutlmv2-classifier && \
    python -c "from transformers import LayoutLMv2ForSequenceClassification; LayoutLMv2ForSequenceClassification.from_pretrained('navodPeiris/layoutlmv2-document-classifier').save_pretrained('/models/layoutlmv2-classifier')"


# ───── Stage 2: Runtime ─────
FROM python:3.11-slim

# Only necessary runtime dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy installed Python libraries from builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/share /usr/local/share

# Copy saved Hugging Face models (faster startup)
COPY --from=builder /models /workspace/models

# Copy app source
COPY src/ /workspace/

# Expose port and run API
EXPOSE 8001

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", \
     "-b", "0.0.0.0:8001", "api:app", \
     "--log-level=info", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--capture-output"]