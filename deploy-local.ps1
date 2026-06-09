# deploy-local.ps1
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d
docker compose ps
docker compose logs -f --tail=100
