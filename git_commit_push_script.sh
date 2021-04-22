#!/bin/bash
cd Desktop/AWSCalc/
day_val=$(date +'%Y_%m_%d')
git status
git add SeleniumOutputs/
git commit -m "Selenium Crawls gathered up to ${day_val}"
git add AutomatedSummary.txt
git commit -m "AutomatedSummary.txt changes up to ${day_val}"
git add *
git commit -m "All other file changes up to ${day_val}"
git push
git status