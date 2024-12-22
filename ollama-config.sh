#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <model-name>"
  echo "Example: $0 llama2"
  exit 1
fi

MODEL_NAME=$1

docker pull ollama/ollama

docker run --rm -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# Note: When the container stops, it will be automatically removed due to the --rm flag.


docker exec -it ollama ollama run "$MODEL_NAME"
