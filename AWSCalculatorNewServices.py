from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import listdir, mkdir, getcwd, chdir
from os.path import join, isfile, exists
import time
from datetime import date, timedelta, datetime
import signal
from sys import platform
import boto3
import json

# catmail = cat ../../var/mail/wilburtw
# delmail = sudo echo "" > ../../var/mail/wilburtw
# sudo rm ../../var/mail/wilburtw
# Testing git credential store
# twice over


def get_day_before(day):
    return day-timedelta(days=1)


def get_full_path_day(day, lists_path):
    str_date = day.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+str_date
    complete_file_name = join(lists_path, partial_file_name+".txt")
    return complete_file_name


def create_directories(sel_out_path, lists_path, new_path):
    mkdir(sel_out_path)
    mkdir(lists_path)
    mkdir(new_path)
    print("Directory '% s' created" % sel_out_path)
    return


def invoke_lambda_text(payload):
    """
    Example Payload
    {
        "new_services_list": "Amazon Alpha, Amazon Beta, AWS Omega"
    }
    """
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    response = lambda_client.invoke(
        FunctionName='ReminderText',
        InvocationType='Event',
        Payload=payload
    )


def write_new_services_file(new_path, new_services, deprecated=False):
    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")

    if deprecated:
        d = "_DEPRECATED_"
        partial_file_names = [date_today+d+service for service in new_services]
    else:
        s = "_"
        partial_file_names = [date_today+s+service for service in new_services]

    for partial_file_name in partial_file_names:
        complete_file_name = join(new_path, partial_file_name+".txt")
        with open(complete_file_name, "w") as file:
            file.write(partial_file_name+"\n")
    for service in new_services:
        print(service, "has been written to new file.\n")
    return


def check_previous_file(list_curr_serv, sel_out_path, lists_path, new_path):
    today = date.today()
    # YY_mm_dd

    date_before = get_day_before(today)
    old_services = []
    # Checking if the list directory is empty or not
    if len(listdir(lists_path)) == 0:
        print("Last Scan: Never")
    else:
        previous_day_file_name = get_full_path_day(date_before, lists_path)
        while not exists(previous_day_file_name):
            print("File from ", date_before, " does not exist.", sep='')
            print("Looking for day before.")
            date_before = get_day_before(date_before)
            previous_day_file_name = get_full_path_day(date_before, lists_path)

        with open(previous_day_file_name, "r") as file:
            print("Last Scan: ", previous_day_file_name.split("/")[-1])
            print(file.readline().strip(), " services found in previous file.")
            line = file.readline()
            while line:
                old_services.append(line.strip())
                line = file.readline()

    new_services = []
    for service in list_curr_serv:
        if service not in old_services:
            new_services.append(service)

    deprecated = []
    for service in old_services:
        if service not in list_curr_serv:
            deprecated.append(service)

    if new_services:
        write_new_services_file(new_path, new_services)
        print("\n\n########################\n# NEW SERVICE(S) ADDED ")
        print("########################\n")
        new_services_string = ""
        for service in new_services:
            print(service, "\n")
            new_services_string = new_services_string+service+" ,"

        new_services_string = new_services_string[:-2]  # del final space+comma
        payload_dict = {}
        payload_dict["new_services_list"] = new_services_string
        payload = json.dumps(payload_dict, indent=4)
        invoke_lambda_text(payload)

    else:
        print("No new services found since last scan.")

    if deprecated:
        write_new_services_file(new_path, deprecated, True)
        print("\n\n########################\n# SERVICE(S) DEPRECATED ")
        print("########################\n")
        for service in deprecated:
            print(service, "\n")
    else:
        print("No services deprecated since last scan.")

    return


def list_services():
    list_curr_serv = []

    # driver = webdriver.Firefox()
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    if platform == "linux" or platform == "linux2":
        # linux
        ex_path = '/usr/bin/chromedriver'
    elif platform == "darwin":
        # OS X
        # xattr -d com.apple.quarantine /Users/wilburtw/Downloads/chromedriver
        ex_path = '/Users/wilburtw/Downloads/chromedriver'
    else:
        print("ChromeDriver not found. Use Linux or MacOS with correct path.")
        exit()


    # driver = webdriver.Chrome(options=chrome_options, executable_path=ex_path)
    # above deprecated in Selenium v4
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://calculator.aws/#/addService")

    time.sleep(5)
    ele_xpath = "//ol/li/div/div/span[@class='awsui-cards-card-header-inner']"
    for li in driver.find_elements_by_xpath(ele_xpath):
        list_curr_serv.append(li.text)

    driver.close()
    return list_curr_serv


def write_data_to_file(list_curr_serv, sel_out_path, lists_path, new_path):
    # Write data to unique file

    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+date_today
    complete_file_name = join(lists_path, partial_file_name+".txt")
    with open(complete_file_name, "w") as file:
        file.write(str(len(list_curr_serv))+"\n")
        print(len(list_curr_serv), " services found today.")
        for service_name in list_curr_serv:
            file.write(service_name+"\n")

    check_previous_file(list_curr_serv, sel_out_path, lists_path, new_path)
    return


"""
class InputTimedOut(Exception):
    pass


def inputTimeOutHandler(signum, frame):
    raise InputTimedOut


signal.signal(signal.SIGALRM, inputTimeOutHandler)


def input_with_timeout(timeout=0):
    unput = ""
    try:
        print("Would you like to abort the scan? (y/n)")
        print("You have {0} seconds\n".format(timeout))
        signal.alarm(timeout)
        unput = input()
        signal.alarm(0)
    except InputTimedOut:
        pass
    return unput
"""


def checked_today(new_path):
    print("\n\n##########################\n#  ALREADY SCANNED TODAY ")
    print("##########################\n")
    service_files = [f for f in listdir(new_path) if isfile(join(new_path, f))]
    today = date.today().strftime("%Y_%m_%d")
    today_files = [f for f in service_files if today in f]

    if not today_files:
        print("No new services found today... Running Scan again.")
        return 0
    print("A file with these services found already today:")

    for file in today_files:
        print(file.split("_")[-1])
    print("\n Preparing to scan again...")

    # Timeout isn't working with Selenium. Short circuiting here
    return 0

    scan_again = input_with_timeout(timeout=5)
    if not scan_again:
        print('No command, scanning again\n')
        return 0
    elif scan_again.lower() == "n":
        print('Not aborting scan, scanning again\n')
        return 0

    # Abort scan
    return 1


def crontab_chdir_fix():
    print("Current Working Directory ", getcwd())

    if platform == "linux" or platform == "linux2":
        # linux
        chdir("wilburtw/AWSPricingCalc")

    elif platform == "darwin":
        # OS X
        chdir("wilburtw/Desktop/AWSPricingCalc")
    else:
        print("Operating System not supported. Use Linux or MacOS.")
        exit()

    print("Current Working Directory ", getcwd())


def main():
    crontab_chdir_fix()  # Goes from home to git dir to run program for crontab

    selenium_output_dir = "SeleniumOutputs"
    lists_services_dir = "ListsOfServices"
    new_services_dir = "NewServicesDates"

    cwd_dir = getcwd()
    sel_out_path = join(cwd_dir, selenium_output_dir)

    lists_path = join(sel_out_path, lists_services_dir)
    new_path = join(sel_out_path, new_services_dir)

    if not exists(sel_out_path):
        create_directories(sel_out_path, lists_path, new_path)
    else:
        print("Directory '% s' already exists" % sel_out_path)

    current_time = datetime.now().strftime("%H:%M:%S")
    print("\nCurrent Date and Time: ", date.today(), " ", current_time)

    # Check for services list from today
    today_file_name = get_full_path_day(date.today(), lists_path)
    if exists(today_file_name):
        if checked_today(new_path):
            return
    print("\n")
    list_curr_serv = list_services()
    write_data_to_file(list_curr_serv, sel_out_path, lists_path, new_path)

    """
    print("Sending text message test...")
    payload_dict = {}
    payload_dict["new_services_list"] = "asdf"
    payload = json.dumps(payload_dict, indent=4)
    invoke_lambda_text(payload)
    """

    print("\n===================================\n\n")
    return


if __name__ == "__main__":
    main()
