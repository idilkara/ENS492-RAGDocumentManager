to run the backend: python3 app.py

to run the backend within a docker container: on port 8080

    docker pull mongo:latest
    
    docker build -t backend .
    docker run -p 8080:8080 backend
