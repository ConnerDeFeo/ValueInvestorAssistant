# Data for user auth layer
data "archive_file" "user_auth_layer" {
  type        = "zip"
  source_dir  = "${path.module}/../server/layers/user_auth/"
  output_path = "${path.module}/../server/layers/user_auth/user_auth.zip"
}

resource "aws_lambda_layer_version" "user_auth" {
  filename         = data.archive_file.user_auth_layer.output_path
  layer_name       = "user_auth"
  compatible_runtimes = ["python3.12"]
  source_code_hash = data.archive_file.user_auth_layer.output_base64sha256
}

# IAM role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "findiff_lambda_role"

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

# Grant Lambda permissions to access DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb" {
  name = "lambda_dynamodb_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = aws_dynamodb_table.comparison_jobs.arn
      }
    ]
  })
}

# Define local map for Lambda function locations
locals {
  lambda_function_locations = {
    "compare_10k_filings" = {
      source_dir  = "../server/lambdas/compare_10k_filings"
      output_path = "../server/lambdas/zips/compare_10k_filings.zip"
    },
    "compare_10k_filings_worker" = {
      source_dir  = "../server/lambdas/compare_10k_filings_worker"
      output_path = "../server/lambdas/zips/compare_10k_filings_worker.zip"
    },
    "search_tickers" = {
      source_dir  = "../server/lambdas/search_tickers"
      output_path = "../server/lambdas/zips/search_tickers.zip"
    },
    "get_available_10k_filings" = {
      source_dir  = "../server/lambdas/get_available_10k_filings"
      output_path = "../server/lambdas/zips/get_available_10k_filings.zip"
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

  layers           = [aws_lambda_layer_version.user_auth.arn]
}