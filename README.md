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
https://crontab.guru/

Another resource that can also help
https://crontab.cronhub.io/


# You Have Mail

Finally, the cronjob will have output from the print statements in the python
program as well as output from the git commands. To access this output, you must
access `/var/mail/<your_username>`

For example, the command I use as an alias when at `$pwd = /Users/wilburtw` is

`cat ~/../../var/mail/wilburtw`

Here is a simple way to launch that command using Aliases.

First, open your bash profile using the following command.

`vim ~/.bash_profile`

Then, add similar lines like the following (any line after a hashtag is a
comment and is ignored). Do NOT include any whitespace around the `=`!!

```
# Aliases
# alias alias_name="command_to_run"

# Get mail from the cronjob
alias catmail="cat ~/../../var/mail/wilburtw"

# Delete the mail file
alias delmail="sudo rm ~/../../var/mail/wilburtw"
```


More about Aliases
https://www.moncefbelyamani.com/create-aliases-in-bash-profile-to-assign-shortcuts-for-common-terminal-commands/



# Actual results (updated every Friday)(see AutomatedSummary.txt for this info)
This File Was Last Updated: 2021-05-11 08:53:59 (Pacific Time; PDT=UTC-7:00 or PST=UTC-8:00)



================================================================================
Between 2020/10/08 and 2021/05/11, there were 43 services added 


SERVICE ADDED | DATE ADDED BY MONTH
===================================
AWS Database Migration Service                    |          2020/10/08  
Amazon Comprehend                                 |          2020/10/19  
Amazon Elastic Container Registry                 |          2020/10/21  
AWS Systems Manager                               |          2020/10/28  

AWS Outposts                                      |          2020/11/13  
AWS Snowmobile                                    |          2020/11/13  
AWS Elemental MediaLive                           |          2020/11/18  
AWS Snowball                                      |          2020/11/24  
Amazon DynamoDB                                   |          2020/11/24  
Amazon SageMaker                                  |          2020/11/24  
Amazon Transcribe                                 |          2020/11/24  

AWS IoT Core                                      |          2020/12/08  
AWS IoT Device Defender                           |          2020/12/08  
AWS IoT Device Management                         |          2020/12/08  
Amazon EKS                                        |          2020/12/09  
AWS Direct Connect                                |          2020/12/17  
Amazon QuickSight                                 |          2020/12/17  
Windows Server and SQL Server on Amazon EC2       |          2020/12/18  
AWS Elemental MediaPackage                        |          2020/12/23  

Amazon Kinesis Data Firehose                      |          2021/01/07  
Amazon SageMaker Ground Truth                     |          2021/01/14  
Amazon Translate                                  |          2021/01/19  

AWS Secrets Manager                               |          2021/02/08  
Amazon Textract                                   |          2021/02/08  
AWS CodeBuild                                     |          2021/02/11  
AWS IoT Things Graph                              |          2021/02/18  
AWS X-Ray                                         |          2021/02/18  
Amazon Cognito                                    |          2021/02/18  
Amazon Managed Streaming for Apache Kafka (MSK)   |          2021/02/18  
AWS CodePipeline                                  |          2021/02/25  
Amazon Neptune                                    |          2021/02/26  

AWS Data Pipeline                                 |          2021/03/05  
Amazon GuardDuty                                  |          2021/03/12  
Amazon QuickSight                                 |          2021/03/18  
Amazon Lookout for Vision                         |          2021/03/22  
AWS Budgets                                       |          2021/03/26  
AWS Cost Explorer                                 |          2021/03/26  

AWS Elemental Media Tailor                        |          2021/04/06  
AWS IoT Analytics                                 |          2021/04/06  
Amazon Polly                                      |          2021/04/09  
Amazon Rekognition                                |          2021/04/15  
AWS IoT Events                                    |          2021/04/27  

Amazon Kendra                                     |          2021/05/11  




================================================================================
