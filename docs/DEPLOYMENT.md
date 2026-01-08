# Azure Deployment Guide

This guide provides detailed instructions for deploying the NER service to Microsoft Azure.

## Prerequisites

- Azure account with active subscription
- Azure CLI installed and configured
- Docker installed locally
- Azure Container Registry (ACR) or Docker Hub account

## Deployment Options

### Option 1: Azure App Service

Azure App Service is the simplest option for deploying containerized applications.

#### Step 1: Create Resources

```bash
# Login to Azure
az login

# Create a resource group
az group create --name ner-service-rg --location eastus

# Create an App Service plan (Linux, B1 tier)
az appservice plan create \
  --name ner-service-plan \
  --resource-group ner-service-rg \
  --sku B1 \
  --is-linux
```

#### Step 2: Create Container Registry

```bash
# Create Azure Container Registry
az acr create \
  --resource-group ner-service-rg \
  --name nerserviceacr \
  --sku Basic

# Login to ACR
az acr login --name nerserviceacr
```

#### Step 3: Build and Push Image

```bash
# Build the Docker image
docker build -t nerserviceacr.azurecr.io/ner-service:latest .

# Push to ACR
docker push nerserviceacr.azurecr.io/ner-service:latest
```

#### Step 4: Create Web App

```bash
# Create the web app with container image
az webapp create \
  --resource-group ner-service-rg \
  --plan ner-service-plan \
  --name ner-service-webapp \
  --deployment-container-image-name nerserviceacr.azurecr.io/ner-service:latest

# Configure app settings
az webapp config appsettings set \
  --resource-group ner-service-rg \
  --name ner-service-webapp \
  --settings WEBSITES_PORT=8000 MODEL_NAME=en_core_web_sm LOG_LEVEL=info
```

#### Step 5: Enable Container Registry Access

```bash
# Enable managed identity
az webapp identity assign \
  --resource-group ner-service-rg \
  --name ner-service-webapp

# Configure ACR integration
az webapp config container set \
  --name ner-service-webapp \
  --resource-group ner-service-rg \
  --docker-custom-image-name nerserviceacr.azurecr.io/ner-service:latest \
  --docker-registry-server-url https://nerserviceacr.azurecr.io
```

#### Step 6: Verify Deployment

```bash
# Get the app URL
az webapp show \
  --resource-group ner-service-rg \
  --name ner-service-webapp \
  --query defaultHostName \
  --output tsv

# Test the health endpoint
curl https://ner-service-webapp.azurewebsites.net/health
```

### Option 2: Azure Container Apps

Azure Container Apps provides more flexibility with auto-scaling and advanced features.

#### Step 1: Create Container Apps Environment

```bash
# Install Container Apps extension
az extension add --name containerapp --upgrade

# Create a Container Apps environment
az containerapp env create \
  --name ner-service-env \
  --resource-group ner-service-rg \
  --location eastus
```

#### Step 2: Deploy Container App

```bash
# Create the container app
az containerapp create \
  --name ner-service-app \
  --resource-group ner-service-rg \
  --environment ner-service-env \
  --image nerserviceacr.azurecr.io/ner-service:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 5 \
  --cpu 0.5 \
  --memory 1Gi \
  --env-vars MODEL_NAME=en_core_web_sm LOG_LEVEL=info
```

#### Step 3: Configure Scaling

```bash
# Configure HTTP scaling rules
az containerapp update \
  --name ner-service-app \
  --resource-group ner-service-rg \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 50
```

### Option 3: Azure Kubernetes Service (AKS)

For advanced scenarios requiring more control.

#### Step 1: Create AKS Cluster

```bash
# Create AKS cluster
az aks create \
  --resource-group ner-service-rg \
  --name ner-service-aks \
  --node-count 2 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials \
  --resource-group ner-service-rg \
  --name ner-service-aks
```

#### Step 2: Deploy to AKS

```bash
# Update the deployment YAML with your ACR name
# Then apply the configuration
kubectl apply -f deployment/azure/container-apps-deployment.yml

# Check deployment status
kubectl get pods
kubectl get services
```

## CI/CD with GitHub Actions

### Setup GitHub Secrets

Add these secrets to your GitHub repository:

1. `AZURE_CREDENTIALS`: Azure service principal credentials
   ```bash
   az ad sp create-for-rbac \
     --name "ner-service-sp" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/ner-service-rg \
     --sdk-auth
   ```

2. `REGISTRY_USERNAME`: ACR username
   ```bash
   az acr credential show --name nerserviceacr --query username
   ```

3. `REGISTRY_PASSWORD`: ACR password
   ```bash
   az acr credential show --name nerserviceacr --query passwords[0].value
   ```

### Trigger Deployment

The GitHub Actions workflow automatically triggers on:
- Push to `main` branch
- Pull request creation
- Manual workflow dispatch

## Monitoring and Logging

### Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app ner-service-insights \
  --location eastus \
  --resource-group ner-service-rg

# Get instrumentation key
az monitor app-insights component show \
  --app ner-service-insights \
  --resource-group ner-service-rg \
  --query instrumentationKey
```

### View Logs

```bash
# App Service logs
az webapp log tail \
  --resource-group ner-service-rg \
  --name ner-service-webapp

# Container Apps logs
az containerapp logs show \
  --name ner-service-app \
  --resource-group ner-service-rg
```

## Cost Optimization

1. **Use appropriate pricing tiers**:
   - Development: B1 (Basic)
   - Production: P1V2 (Premium V2) or higher

2. **Enable auto-scaling**:
   - Scale based on CPU/memory
   - Set minimum and maximum instances

3. **Monitor resource usage**:
   - Use Azure Cost Management
   - Set up budget alerts

## Security Best Practices

1. **Use managed identities** for ACR access
2. **Enable HTTPS only**
3. **Configure CORS** appropriately
4. **Use Azure Key Vault** for secrets
5. **Enable diagnostic logging**
6. **Implement API authentication** (Azure AD, API keys)

## Troubleshooting

### Container fails to start

```bash
# Check container logs
az webapp log tail --resource-group ner-service-rg --name ner-service-webapp

# Verify image exists
az acr repository show --name nerserviceacr --image ner-service:latest
```

### Health check failures

- Verify the `/health` endpoint is accessible
- Check if spaCy model is downloaded
- Review application logs

### Performance issues

- Scale up the App Service plan
- Increase memory/CPU limits
- Enable auto-scaling
- Use Azure CDN for static content

## Cleanup

```bash
# Delete all resources
az group delete --name ner-service-rg --yes --no-wait
```

## Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)
- [Azure Container Registry Documentation](https://docs.microsoft.com/azure/container-registry/)
