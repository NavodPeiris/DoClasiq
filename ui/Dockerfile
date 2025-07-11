# ───── Stage 1: Builder ─────
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /workspace

COPY src/requirements.txt .

# Install Jupyter and some Python libraries
RUN pip install --no-cache-dir --timeout=100 -r requirements.txt


# ───── Stage 2: Runtime ─────
FROM python:3.11-slim

WORKDIR /workspace

# Copy installed Python libraries from builder stage
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/include /usr/local/include
COPY --from=builder /usr/local/share /usr/local/share

# Copy app source
COPY src/ /workspace/

# Expose the port for API
EXPOSE 8502

# Run streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]