!bin/bash 
cd backend
docker-compose up --build
docker exec -it ollama ollama pull nomic-embed-text
docker exec -it ollama ollama pull mistral