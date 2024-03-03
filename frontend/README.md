## 1. Require
- Nodejs (v.21)
## 2. Run 
```bash
# start container
docker compose -p frontend -f ./docker/docker-compose.yml up -d

# remove container
docker compose -p frontend -f ./docker/docker-compose.yml down
```