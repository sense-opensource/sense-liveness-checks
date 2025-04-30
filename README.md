<h1> Liveness Detection: Sense</h1>

<p width="100%">
  
<img width="8%" src="https://badge-generator.vercel.app/api?label=License&status=MIT&color=6941C6"> <img width="12.6%" src="https://badge-generator.vercel.app/api?icon=Github&label=Last%20Commit&status=May&color=6941C6"/> <img width="10%" src="https://badge-generator.vercel.app/api?icon=Discord&label=Discord&status=Live&color=6941C6"> 
</p>

<h2>Welcome to Sense’s open source repository</h2>

<p width="100%">  
<img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Fork-orange.svg?logo=fork"> <img width="4.5%" src="https://custom-icon-badges.demolab.com/badge/Star-yellow.svg?logo=star"> <img width="6.5%" src="https://custom-icon-badges.demolab.com/badge/Commit-green.svg?logo=git-commit&logoColor=fff"> 
</p>

<p> This project serves an anti-spoofing detection API built using FastAPI. It analyzes facial images and predicts whether they are <b>Real</b> or <b>Spoof</b> using a set of trained models.</p>

<h3>Quick Start</h3>

<h3>1. Prerequisites </h3>

<p> [Docker](https://www.docker.com/products/docker-desktop) installed </p>              

<h4> 🧠 Model </h4>

<p> The anti spoof model file is <b>not included</b> in the repository. You must download the model file manually or programmatically and place it in the appropriate folder.</p>

<h4> ✅ Download Instructions </h4>

<p> Download the model file from the below link: </p>

<p> [Model] (https://github.com/sense-opensource/sense-liveness-checks/releases/download/v1.0.0/efficientnet-b7.onnx this file needs to be placed inside the resources folder) </p>

<p> Ensure the model is saved in:  </p>

<p> resources/efficientnet-b7.onnx </p>

<h4> Clone the Repository </h4> 

<p> git clone https://github.com/sense-opensource/sense-liveness-checks.git </p>
<p> cd liveness </p>

<h3> 2. Build Docker Image </h3>

<p> docker build -t sense_liveness_opensource_image </p>

<h3> 3. Run Docker Container </h3>

<p> docker run -d --name sense_liveness_opensource_container -p 3016:3016 sense_liveness_opensource_image </p>

<p> This will start the API server on: http://localhost:3016 </p>

<h3> 4. Run the Frontend </h3>

<p>cd front-end</p>
<p>npm install</p>
<p>npm run dev</p>

<p> <b> By default, the frontend runs on : http://localhost:5000 </b></p>

<h2>Useful Docker Commands</h2>

<h3> Stop container </h3>
<p>docker stop sense_liveness_opensource_container</p>

<h3> Remove container </h3>
<p>  docker rm -f sense_liveness_opensource_container</p>

<h3> Remove image </h3>
<p>docker rmi -f  sense_liveness_opensource_image </p>

<h3> View logs </h3>
<p>docker logs anti_spoof_container</p>

<h2> License </h2>
<p> MIT License — free to use, share, and modify </p>