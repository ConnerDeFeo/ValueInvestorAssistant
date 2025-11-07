# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "my-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Basic execution permissions
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# Allow Lambda to invoke Bedrock models
resource "aws_iam_role_policy" "bedrock_policy" {
  name = "bedrock-access"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "bedrock:InvokeModel"
      ]
      Resource = "*"
    }]
  })
}

# Define local map for Lambda function locations
locals {
  lambda_function_locations = {
    "compare_filings" = {
      source_dir  = "../server/lambdas/compare_filings"
      output_path = "../server/lambdas/zips/compare_filings.zip"
    },
    "search_tickers" = {
      source_dir  = "../server/lambdas/search_tickers"
      output_path = "../server/lambdas/zips/search_tickers.zip"
    }
  }
}

# Archive files using for_each
data "archive_file" "lambda_archives" {
  for_each = local.lambda_function_locations
  
  type        = "zip"
  source_dir  = each.value.source_dir
  output_path = each.value.output_path
}

# Create Lambda functions using for_each
resource "aws_lambda_function" "lambdas" {
  for_each = local.lambda_function_locations

  function_name    = each.key
  role             = aws_iam_role.lambda_role.arn
  handler          = "${each.key}.${each.key}"
  runtime          = "python3.12"
  filename         = data.archive_file.lambda_archives[each.key].output_path
  source_code_hash = data.archive_file.lambda_archives[each.key].output_base64sha256
  timeout          = 120
  memory_size      = 512
}

# Give each lambda an endpoint
resource "aws_lambda_function_url" "lambda_urls" {
  for_each = aws_lambda_function.lambdas

  function_name = each.value.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]
    allow_methods = ["*"]
    allow_headers = ["*"]
  }
}

# Output the Lambda function URLs
output "lambda_function_urls" {
  value = {
    for key, lambda in aws_lambda_function.lambdas :
    key => aws_lambda_function_url.lambda_urls[key].function_url
  }
}