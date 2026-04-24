param(
    [Parameter(Mandatory = $true)]
    [string]$AwsRegion,

    [Parameter(Mandatory = $true)]
    [string]$AwsAccountId,

    [Parameter(Mandatory = $true)]
    [string]$ClusterName,

    [Parameter(Mandatory = $true)]
    [string]$ServiceName,

    [string]$RepositoryName = "job-application-copilot",
    [string]$TaskFamily = "job-application-copilot",
    [string]$ImageTag = "latest",
    [string]$OpenAIModel = "gpt-5-mini",
    [string]$TaskDefinitionPath = "task-definition.json"
)

$ErrorActionPreference = "Stop"

function Require-Command {
    param([string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found on PATH."
    }
}

Require-Command "aws"
Require-Command "docker"

$repoUri = "$AwsAccountId.dkr.ecr.$AwsRegion.amazonaws.com/$RepositoryName"
$renderedTaskDef = Join-Path $env:TEMP "$TaskFamily.rendered.json"

Write-Host "Ensuring ECR repository exists..."
try {
    aws ecr describe-repositories --repository-names $RepositoryName --region $AwsRegion | Out-Null
}
catch {
    aws ecr create-repository --repository-name $RepositoryName --region $AwsRegion | Out-Null
}

Write-Host "Logging Docker into ECR..."
aws ecr get-login-password --region $AwsRegion | docker login --username AWS --password-stdin "$AwsAccountId.dkr.ecr.$AwsRegion.amazonaws.com"

Write-Host "Building container image..."
docker build -t "${RepositoryName}:${ImageTag}" .

Write-Host "Tagging container image..."
docker tag "${RepositoryName}:${ImageTag}" "${repoUri}:${ImageTag}"

Write-Host "Pushing image to ECR..."
docker push "${repoUri}:${ImageTag}"

Write-Host "Rendering task definition..."
$taskDefinition = Get-Content $TaskDefinitionPath -Raw
$taskDefinition = $taskDefinition.Replace("<AWS_ACCOUNT_ID>", $AwsAccountId)
$taskDefinition = $taskDefinition.Replace("<AWS_REGION>", $AwsRegion)
$taskDefinition = $taskDefinition.Replace(
    "$AwsAccountId.dkr.ecr.$AwsRegion.amazonaws.com/$RepositoryName:latest",
    "${repoUri}:${ImageTag}"
)
$taskDefinition = $taskDefinition.Replace('"value": "gpt-5-mini"', "`"value`": `"$OpenAIModel`"")
$taskDefinition | Set-Content -Path $renderedTaskDef

Write-Host "Registering task definition..."
$registerOutput = aws ecs register-task-definition --cli-input-json "file://$renderedTaskDef" --region $AwsRegion | ConvertFrom-Json
$taskDefinitionArn = $registerOutput.taskDefinition.taskDefinitionArn

Write-Host "Updating ECS service..."
aws ecs update-service `
    --cluster $ClusterName `
    --service $ServiceName `
    --task-definition $taskDefinitionArn `
    --force-new-deployment `
    --region $AwsRegion | Out-Null

Write-Host ""
Write-Host "Deployment submitted successfully."
Write-Host "ECR image: ${repoUri}:${ImageTag}"
Write-Host "Task definition: $taskDefinitionArn"
Write-Host "Cluster: $ClusterName"
Write-Host "Service: $ServiceName"
