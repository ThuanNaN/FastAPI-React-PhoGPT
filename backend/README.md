## 1. Download model checkpoint
Optiional: install git-lfs. https://git-lfs.com/
```bash
mkdir model_repository
mkdir vinai
git clone https://huggingface.co/vinai/PhoGPT-4B-Chat
# or 
wget https://huggingface.co/vinai/PhoGPT-4B-Chat/blob/main/pytorch_model.bin
```

## 2. Build and run docker container via docker-compose
```bash
# start container
docker compose -p backend -f ./docker/docker-compose.yml up -d

# remove container
docker compose -p backend -f ./docker/docker-compose.yml down
```