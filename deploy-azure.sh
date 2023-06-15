az containerapp up \
  -g louis-demo-rg \
  -n louis-demo-app \
  --ingress external \
  --target-port 5000 \
        --image louis-demo