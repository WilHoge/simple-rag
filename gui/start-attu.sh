docker stop attu
docker rm attu

docker run -d --name attu -p 8000:3000 \
-v /wxd-install/ibm-lh-dev/localstorage/volumes/infra/tls:/app/tls \
-e ATTU_LOG_LEVEL=debug \
-e ROOT_CERT_PATH=/app/tls/cert.crt \
zilliz/attu:v2.4.0
