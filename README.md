<h1> Liveness Detection: Sense</h1>

<p width="100%">
    <a href="https://github.com/sense-opensource/sense-liveness-checks/blob/main/LICENSE">
        <img width="8%" src="https://badge-generator.vercel.app/api?label=License&status=MIT&color=6941C6"> 
    </a>
    <a href="https://discord.gg/hzNHTpwt">
        <img width="10%" src="https://badge-generator.vercel.app/api?icon=Discord&label=Discord&status=Live&color=6941C6"> 
    </a>
</p>

<h2>Welcome to Sense’s open source repository</h2>

<p width="100%">  
<img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Fork-orange.svg?logo=fork"> 
<img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Star-yellow.svg?logo=star"> 
<img width="6.5%" src="https://custom-icon-badges.demolab.com/badge/Commit-green.svg?logo=git-commit&logoColor=fff"> 
</p>

<p> This project serves an anti-spoofing detection API built using FastAPI. It analyzes facial images and predicts whether they are <b>Real</b> or <b>Spoof</b> using a set of trained models.</p>

<h3>Quick Start</h3>

<h3>1. Prerequisites </h3>

```bash

[Docker](https://www.docker.com/products/docker-desktop) installed             
```
<h4> Clone the Repository </h4> 

```bash
# Clone the repository
git clone https://github.com/sense-opensource/sense-liveness-checks.git

# Navigate into the project directory
cd sense-liveness-checks
```

<h4> 🧠 Model </h4>

<p> The anti spoof model file is <b>not included</b> in the repository. You must download the model file manually or programmatically and place it in the appropriate folder.</p>

<h4> ✅ Download Instructions </h4>

<p> Download the model file from the below link: </p>

```bash
https://github.com/sense-opensource/sense-liveness-checks/releases/download/v1.0.0/efficientnet-b7.onnx
```
this file needs to be placed inside the resources folder</br>
<p> Ensure the model is saved in: <i>resources/efficientnet-b7.onnx </i> </p>

<h3>2. API Configuration </h3>
<h4>Method 1: Install Python Dependencies </h4>

```bash
pip install -r requirements.txt
```

<h4> Start the FastAPI Server </h4>

```bash
uvicorn app:app --reload
```

<p> This will start the API server on: http://localhost:3016 </p>

<h4>Method 2: Running with Docker </h4>
<h4>Build Docker Image </h4>

```docker
docker build -t sense_liveness_opensource_image .
```

<h4>Run Docker Container </h4>

```docker
docker run -d --name sense_liveness_opensource_container -p 3016:3016 sense_liveness_opensource_image
```

<p> This will start the API server on: http://localhost:3016 </p>

<h3>3. Run the Frontend </h3>

```bash
cd front-end
npm install
npm run dev
```

<p> <b> By default, the frontend runs on : http://localhost:5000 </b></p>

<h2>Useful Docker Commands</h2>

<h3> Stop container </h3>

```docker
docker stop sense_liveness_opensource_container
```

<h3> Remove container </h3>

```docker
docker rm -f sense_liveness_opensource_container
```

<h3> Remove image </h3>

```docker
docker rmi -f  sense_liveness_opensource_image
```

<h3> View logs </h3>

```docker
docker logs anti_spoof_container
```

<h2> License </h2>
<p> MIT License — free to use, share, and modify </p>
