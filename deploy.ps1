#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy Regime-Switching Trading Engine to AWS

.DESCRIPTION
    This script builds and deploys the application to AWS using SAM CLI.
#>

param(
    [string]$Environment = "prod",
    [string]$Region = "us-east-1"
)

Write-Host "🚀 Starting AWS deployment..." -ForegroundColor Green

# Check if AWS CLI is installed
try {
    aws --version | Out-Null
    Write-Host "✅ AWS CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ AWS CLI not found. Please install it first." -ForegroundColor Red
    exit 1
}

# Check if SAM CLI is installed
try {
    sam --version | Out-Null
    Write-Host "✅ SAM CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ SAM CLI not found. Please install it first." -ForegroundColor Red
    exit 1
}

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run tests
Write-Host "🧪 Running tests..." -ForegroundColor Yellow
pytest tests/ --cov=app --cov-report=html

# Build the application
Write-Host "🔨 Building SAM application..." -ForegroundColor Yellow
sam build

# Deploy to AWS
Write-Host "☁️ Deploying to AWS..." -ForegroundColor Yellow
sam deploy --guided --region $Region

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Your API will be available at the URL shown above" -ForegroundColor Cyan 