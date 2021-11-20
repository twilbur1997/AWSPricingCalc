#!/bin/bash
/usr/bin/python3 wilburtw/AWSPricingCalc/AWSCalculatorNewServices.py 
/usr/bin/python3 wilburtw/AWSPricingCalc/SummarizeServicesAdded.py
cd wilburtw/AWSPricingCalc
day_val=$(date +'%d/%m/%Y %H:%M:%S')
git status
git add SeleniumOutputs/
git commit -m "Selenium Crawls gathered up to ${day_val}"
git add AutomatedSummary.txt
git commit -m "AutomatedSummary.txt changes up to ${day_val}"
cp text_README.md README.md
cat AutomatedSummary.txt >> README.md
git add README.md
git commit -m "README.md changes up to ${day_val}"
git add *
git commit -m "All other file changes up to ${day_val}"
git push
git status
