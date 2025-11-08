#!/bin/bash

cd lambdas/compare_10k_filings
pip install -r requirements.txt -t .
cd ../compare_10k_filings_worker
pip install -r requirements.txt -t .
cd ../get_available_10k_filings
pip install -r requirements.txt -t .

cd ../../../terraform
terraform apply --auto-approve

cd ../server/lambdas/compare_10k_filings
rm -rf bin boto3** botocore** dateutil jmespath** python** s3transfer** six** urllib3**
cd ../compare_10k_filings_worker
rm -rf bin annotated_types** anyio** beautifulsoup4** boto3** botocore** certifi** bs4** dateutil** h11** httpcore** idna** jmespath** pydantic** s3transfer** six** httpx** python** sniffio** soupsieve** typing_inspection** urllib3**
cd ../get_available_10k_filings
rm -rf bin boto3** botocore** certifi** dateutil** jmespath** s3transfer** six** urllib3** charset_normalizer** idna** urllib3** requests**