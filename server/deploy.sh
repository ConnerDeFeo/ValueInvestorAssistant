#!/bin/bash
cd lambdas/compare_10k_filings
pip install -r requirements.txt -t .
cd ../get_available_10k_filings
pip install -r requirements.txt -t .

cd ../../../terraform
terraform apply --auto-approve

cd ../server/lambdas/compare_10k_filings
shopt -s extglob
rm -rf !(compare_10k_filings.py|requirements.txt)
cd ../get_available_10k_filings
shopt -s extglob
rm -rf !(get_available_10k_filings.py|requirements.txt)