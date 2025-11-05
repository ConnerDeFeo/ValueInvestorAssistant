# main.tf

# Archive your Python code into a zip
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "../server/lambdas/compare_filings"  # Your Python file
  output_path = "../server/lambdas/zip"
}

# The Lambda function
resource "aws_lambda_function" "compare_filings" {
  filename         = "compare_filings.zip"
  function_name    = "compare-filings-function"
  role            = aws_iam_role.lambda_role.arn
  handler         = "compare_filings.compare_filings"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30
  
  environment {
    variables = {
      ENV = "production"
    }
  }
}

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