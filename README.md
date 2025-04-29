<h1 align="center"> Liveness Detection: Sense</h1>

<p align="center" width="100%">
<img width="8%" src="https://badge-generator.vercel.app/api?label=License&status=MIT&color=6941C6"> <img width="12.6%" src="https://badge-generator.vercel.app/api?icon=Github&label=Last%20Commit&status=May&color=6941C6"/> <img width="10%" src="https://badge-generator.vercel.app/api?icon=Discord&label=Discord&status=Live&color=6941C6"> 
</p>

<h2 align="center">Welcome to Sense’s open source repository</h2>

<p align="center" width="100%">  
<img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Fork-orange.svg?logo=fork"> <img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Star-yellow.svg?logo=star"> <img width="6.5%" src="https://custom-icon-badges.demolab.com/badge/Commit-green.svg?logo=git-commit&logoColor=fff"> 
</p>

<p align="center"> This project serves an anti-spoofing detection API built using FastAPI. It analyzes facial images and predicts whether they are <b>Real</b> or <b>Spoof</b> using a set of trained models.</p>

<h3 align="center">Quick Start</h3>

<h3 align="center">1. Prerequisites </h3>

<p align="center"> [Docker](https://www.docker.com/products/docker-desktop) installed </p>              

<p align="center"> [Model] (https://cdn-or-s3-link.com/2.7_80x80_MiniFASNetV2.pth this file needs to be placed inside the resources folder) </p>

<h4 align="center"> 🧠 Model </h4>

<p align="center"> The anti spoof model file is <b>not included</b> in the repository. 
You must download the model file manually or programmatically and place it in the appropriate folder.</p>

<h4 align="center"> ✅ Download Instructions </h4>

<p align="center"> Download the model file from CDN or S3 bucket: </p>

<p align="center"> wget https://cdn-or-s3-link.com/2.7_80x80_MiniFASNetV2.pth -P resources/anti_spoof_models/  </p>

<p align="center"> Ensure the model is saved in:  </p>

<p align="center"> resources/anti_spoof_models/2.7_80x80_MiniFASNetV2.pth </p>

<h4 align="center"> Clone the Repository </h4> 

<p align="center"> git clone https://github.com/your-username/liveness.git </p>
<p align="center"> cd liveness </p>

<h3 align="center"> 2. Build Docker Image </h3>

<p align="center"> docker build -t sense_liveness_opensource_image </p>

<h3 align="center"> 3. Run Docker Container </h3>

<p align="center"> docker run -d --name sense_liveness_opensource_container -p 3016:3016 sense_liveness_opensource_image </p>

<p align="center"> This will start the API server on: http://localhost:3016 </p>

<h3 align="center"> 4. Run the Frontend </h3>

<p align="center">cd front-end</p>
<p align="center">npm install</p>
<p align="center">npm run dev</p>

<p align="center"> <b> By default, the frontend runs on:
http://localhost:5000 </b></p>

<h2 align="center">Useful Docker Commands</h2>

<h3 align="center"> Stop container </h3>
<p align="center">docker stop sense_liveness_opensource_container</p>

<h3 align="center"> Remove container </h3>
<p align="center">docker rm -f sense_liveness_opensource_container</p>

<h3 align="center"> Remove image </h3>
<p align="center">docker rmi -f  sense_liveness_opensource_image</p>

<h3 align="center"> View logs </h3>
<p align="center">docker logs anti_spoof_container</p>

<h2 align="center"> License </h2>
<p align="center"> MIT License — free to use, share, and modify </p>

