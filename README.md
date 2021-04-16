# AWSCalc

Hi there!

This is a personal project I made to refresh my Selenium skills, bash scripting
skills, and crontab knowledge.

I was frustrated that the AWS Pricing Calculator did not post updates when they
added new services - the calculator offered pricing assistance on 57 services
when I started this project in late September of 2020, but supports 96 services
as of April 16th, 2021.

I started with a fairly basic Selenium program that scrapes the AWS Pricing
Calculator website and then used crontab to get it to run three times a day,
storing the service names that were found and comparing to previous lists to
see if any services had been added.

Eventually, I automated the summarization of this, checked for deprecated
services, and automated the Git commit flow as well.

This is all fully open-source, the AWS Pricing Calculator is free to use and I
haven't ever had trouble crawling it.

I may be looking to host this within AWS in the future, either with a Lambda
or a small EC2 instance. I also want to try to build a SlackBot to be able to
publish this information to a Slack Channel.

Thanks for the interest, feel free to send me any questions!


AWS Pricing Calculator
https://calculator.aws/#/addService

Explanation of Cron Expressions and English evaluator
https://crontab.cronhub.io/
