# AWSCalc

Hi there!

This is a personal project I made to refresh my Selenium skills, bash scripting
skills, and crontab knowledge.

I was frustrated that the AWS Pricing Calculator did not post updates when they
added new services - the calculator offered pricing assistance on 57 services
when I started this project in late September of 2020, but supports 96 services
as of April 16th, 2021.

I wanted to know which new services were added and when!

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




# Cron, Crontab, and Cron jobs

Note: Cron is fairly easy to use. On Mac, simply open your Terminal and use
`crontab -e` to open your crontab. From there, you can copy and paste the text
from the crontab.txt file in this directory, or you can create your own
schedule.

Note that my crontab is configured to run a the program in my Desktop/AWSCalc/
folder, and you may have to change this path or edit your directory to make it
work.

As an example, one line in my crontab is the following:

`30 9 * * * /usr/local/bin/python3 /Users/wilburtw/Desktop/AWSCalc/AWSCalculatorNewServices.py`

I'll separate it into three important parts: When, Verb, and Object
When: `30 9 * * * `
This expression makes it so this line executes at 09:30 every day of every month.
Verb: `/usr/local/bin/python3`
Usually abbreviated to `python3`, this specifies the EXACT python you want to launch.
Object: `/Users/wilburtw/Desktop/AWSCalc/AWSCalculatorNewServices.py`
This is what the Verb will act on. This is the absolute path so it doesn't get confused.

The Verb and Object usually can be abbreviated as `python3 AWSCalculatorNewServices.py`,
but I had trouble doing this in my crontab because it wasn't in /Desktop/AWSCalc
for the .py file, and it couldn't find the correct Python version to run if it was.


More about Cron on Mac
https://ole.michelsen.dk/blog/schedule-jobs-with-crontab-on-mac-osx/

Explanation of Cron Expressions and a plain-English translator
https://crontab.cronhub.io/
