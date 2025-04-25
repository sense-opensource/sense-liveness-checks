# Liveness check

This project serves an anti-spoofing detection API built using **FastAPI**. It analyzes facial images and predicts whether they are **Real** or **Spoof** using a set of trained models.

## Quick Start

### 1. Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [Model] (https://cdn-or-s3-link.com/2.7_80x80_MiniFASNetV2.pth this file needs to be placed inside the resources folder)

## 🧠 Model

The anti spoof model file is **not included** in the repository.  
You must download the model file manually or programmatically and place it in the appropriate folder.

### ✅ Download Instructions

Download the model file from CDN or S3 bucket:

wget https://cdn-or-s3-link.com/2.7_80x80_MiniFASNetV2.pth -P resources/anti_spoof_models/

Ensure the model is saved in:

resources/anti_spoof_models/2.7_80x80_MiniFASNetV2.pth

### Clone the Repository

git clone https://github.com/your-username/liveness.git
cd liveness

### 2. Build Docker Image

docker build -t sense_liveness_opensource_image .

### 3. Run Docker Container
docker run -d --name sense_liveness_opensource_container -p 3016:3016 sense_liveness_opensource_image

This will start the API server on:
http://localhost:3016


### 4. Run the Frontend

cd front-end
npm install
npm run dev

By default, the frontend runs on:
http://localhost:5000


### Project Structure
.
├── Dockerfile
├── docker-compose.yml
├── app.py/              # FastAPI app entrypoint
├── src/                 # Anti-spoofing model logic
├── resources/           # Pretrained model files
└── front-end/           # Frontend application (optional)


### Useful Docker Commands

# Stop container
docker stop sense_liveness_opensource_container

# Remove container
docker rm -f sense_liveness_opensource_container

# Remove image
docker rmi -f  sense_liveness_opensource_image

# View logs
docker logs anti_spoof_container


### License
MIT License — free to use, share, and modify.