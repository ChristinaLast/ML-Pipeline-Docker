snap install docker --devmode
docker pull tensorflow/tensorflow 
docker build -t app .
docker run --name app -p 5000:5000 app 