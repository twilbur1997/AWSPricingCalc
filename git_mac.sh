#!/bin/bash
/usr/local/bin/python3 /Users/wilburtw/Desktop/AWSPricingCalc/AWSCalculatorNewServices.py
/usr/local/bin/python3 /Users/wilburtw/Desktop/AWSPricingCalc/SummarizeServicesAdded.py
cd wilburtw/Desktop/AWSPricingCalc/
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
clear
git status
