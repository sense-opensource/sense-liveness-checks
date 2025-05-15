# ✅ Ultra-optimized CPU-only FastAPI + Torch
FROM python:3.9-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies for OpenCV headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .

# Install pip packages (Torch CPU-only from official source)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      torch==2.1.0+cpu \
      torchvision==0.16.0+cpu \
      -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

EXPOSE 3016

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3016"]
