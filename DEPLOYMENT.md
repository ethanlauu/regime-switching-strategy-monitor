# AWS Deployment Guide

## Prerequisites

1. **AWS CLI** - Install from https://aws.amazon.com/cli/
2. **AWS SAM CLI** - Install from https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
3. **Node.js & npm** - For frontend build
4. **Python 3.11** - For backend

## Step 1: Configure AWS

```bash
# Configure AWS CLI
aws configure

# Enter your:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (e.g., us-east-1)
# - Default output format (json)
```

## Step 2: Test Local Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov=app --cov-report=html

# Start backend server
py -m uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

## Step 3: Test Local Frontend

```bash
# Install frontend dependencies
npm install

# Start frontend server
npm run dev
```

## Step 4: Deploy Backend to AWS

```bash
# Build the SAM application
sam build

# Deploy (first time - guided)
sam deploy --guided

# Follow the prompts:
# - Stack Name: regime-switching-trading-engine
# - AWS Region: us-east-1 (or your preferred region)
# - Confirm changes before deploy: Yes
# - Allow SAM CLI IAM role creation: Yes
# - Save arguments to configuration file: Yes
```

## Step 5: Update Frontend for Production

After deployment, you'll get an API Gateway URL. Update the production environment:

1. Copy the API Gateway URL from the deployment output
2. Update `env.production` with the correct URL:
   ```
   VITE_API_URL=https://your-actual-api-gateway-url.amazonaws.com/prod
   ```

## Step 6: Deploy Frontend

### Option A: Deploy to AWS S3 + CloudFront

```bash
# Build frontend for production
npm run build

# Create S3 bucket (replace with your bucket name)
aws s3 mb s3://your-regime-switching-app

# Upload to S3
aws s3 sync dist/ s3://your-regime-switching-app

# Create CloudFront distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

### Option B: Deploy to Vercel/Netlify

1. Push your code to GitHub
2. Connect your repository to Vercel or Netlify
3. Set environment variables:
   - `VITE_API_URL`: Your API Gateway URL

## Step 7: Test Production Deployment

1. Test backend API endpoints:
   ```bash
   curl https://your-api-gateway-url.amazonaws.com/prod/health
   curl https://your-api-gateway-url.amazonaws.com/prod/regime/latest
   ```

2. Test frontend:
   - Visit your deployed frontend URL
   - Verify all components load correctly
   - Check browser console for any errors

## Step 8: Monitor and Maintain

### CloudWatch Logs
```bash
# View Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/regime-switching"

# View recent logs
aws logs tail /aws/lambda/regime-switching-trading-engine --follow
```

### Update Application
```bash
# Make changes to your code
# Build and deploy
sam build
sam deploy
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure API Gateway has CORS enabled
2. **Lambda Timeout**: Increase timeout in `template.yaml`
3. **Memory Issues**: Increase memory allocation in `template.yaml`
4. **Import Errors**: Check that all dependencies are in `requirements.txt`

### Debug Commands

```bash
# Check SAM build
sam build --debug

# Check deployment status
aws cloudformation describe-stacks --stack-name regime-switching-trading-engine

# View API Gateway logs
aws logs describe-log-groups --log-group-name-prefix "API-Gateway-Execution-Logs"
```

## Cost Optimization

1. **DynamoDB**: Use on-demand billing for development
2. **Lambda**: Monitor execution time and memory usage
3. **API Gateway**: Consider caching for frequently accessed endpoints
4. **CloudWatch**: Set up log retention policies

## Security Considerations

1. **API Keys**: Consider adding API key authentication
2. **CORS**: Restrict CORS origins to your frontend domain
3. **IAM Roles**: Use least privilege principle
4. **Environment Variables**: Use AWS Systems Manager Parameter Store for secrets

## Performance Optimization

1. **Lambda Cold Starts**: Consider provisioned concurrency
2. **DynamoDB**: Use appropriate read/write capacity
3. **API Gateway**: Enable caching
4. **Frontend**: Use CDN for static assets 