# Create DynamoDB table for comparison jobs
resource "aws_dynamodb_table" "comparison_jobs" {
  name         = "comparison_jobs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "job_id"

  attribute {
    name = "job_id"
    type = "S"
  }

  tags = {
    Name        = "FinDiff Comparison Jobs"
    Environment = "prod"
  }
}