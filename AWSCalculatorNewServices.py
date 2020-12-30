from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from os import listdir, mkdir, getcwd, chdir
from os.path import join, isfile, exists
import time
from datetime import date
from datetime import timedelta
import signal

# catmail = cat ../../var/mail/wilburtw
# delmail = sudo echo "" > ../../var/mail/wilburtw
# sudo rm ../../var/mail/wilburtw

def get_day_before(day):
    return day - timedelta(days = 1)


def get_full_path_for_day_file(day, lists_services_path):
    str_date = day.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+str_date
    complete_file_name = join(lists_services_path, partial_file_name+".txt")
    return complete_file_name


def create_directories(selenium_output_path, lists_services_path, new_services_path):
    mkdir(selenium_output_path)
    mkdir(lists_services_path)
    mkdir(new_services_path)
    print("Directory '% s' created" % selenium_output_path)
    return


def write_new_services_file(new_services_path, new_services, deprecated=False):
    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")

    if deprecated:
        partial_file_names = ["ZZZ_"+date_today+"_DEPRECATED_"+service for service in new_services]
    else:
        partial_file_names = [date_today+"_"+service for service in new_services]

    for partial_file_name in partial_file_names:
        complete_file_name = join(new_services_path, partial_file_name+".txt")
        with open(complete_file_name, "w") as file:
            file.write(partial_file_name+"\n")
    for service in new_services:
        print(service, "has been written to new file.\n")
    return


def check_previous_file(list_of_current_services, selenium_output_path, lists_services_path, new_services_path):
    today = date.today()
    # YY_mm_dd

    date_before = get_day_before(today)
    old_services = []
    # Checking if the list directory is empty or not
    if len(os.listdir(lists_services_path)) == 0:
        print("Last Scan: Never")
    else:
        previous_day_file_name = get_full_path_for_day_file(date_before, lists_services_path)
        while not exists(previous_day_file_name):
            print("File from ", date_before, " does not exist. Looking for day before.", sep='')
            date_before = get_day_before(date_before)
            previous_day_file_name = get_full_path_for_day_file(date_before, lists_services_path)

        with open(previous_day_file_name, "r") as file:
            print("Last Scan: ", previous_day_file_name.split("/")[-1])
            print(file.readline().strip(), " services were found in previous file.")
            line = file.readline()
            while line:
                old_services.append(line.strip())
                line = file.readline()

    new_services = []
    for service in list_of_current_services:
        if service not in old_services:
            new_services.append(service)

    deprecated = []
    for service in old_services:
        if service not in list_of_current_services:
            deprecated.append(service)

    if new_services:
        write_new_services_file(new_services_path, new_services)
        print("\n\n########################\n# NEW SERVICE(S) ADDED #\n########################\n")
        for service in new_services:
            print(service, "\n")
    else:
        print("No new services found since last scan.")

    if deprecated:
        write_new_services_file(new_services_path, deprecated, True)
        print("\n\n########################\n# SERVICE(S) DEPRECATED #\n########################\n")
        for service in deprecated:
            print(service, "\n")
    else:
        print("No services deprecated since last scan.")

    return


def list_services():
    list_of_current_services = []

    # driver = webdriver.Firefox()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options, executable_path='/Users/wilburtw/Downloads/chromedriver')

    driver.get("https://calculator.aws/#/addService")

    time.sleep(5)
    for li in driver.find_elements_by_xpath("//ol/li/div/div/span[@class='awsui-cards-card-header-inner']"):
        list_of_current_services.append(li.text)

    driver.close()
    return list_of_current_services


def write_data_to_file(list_of_current_services, selenium_output_path, lists_services_path, new_services_path):
    # Write data to unique file

    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+date_today
    complete_file_name = join(lists_services_path, partial_file_name+".txt")
    with open(complete_file_name, "w") as file:
        file.write(str(len(list_of_current_services))+"\n")
        print(len(list_of_current_services), " services found today.")
        for service_name in list_of_current_services:
            file.write(service_name+"\n")

    check_previous_file(list_of_current_services, selenium_output_path, lists_services_path, new_services_path)
    return



class InputTimedOut(Exception):
    pass


def inputTimeOutHandler(signum, frame):
    raise InputTimedOut


signal.signal(signal.SIGALRM, inputTimeOutHandler)


def input_with_timeout(timeout=0):
    unput = ""
    try:
        print("Would you like to abort the scan? (y/n)\nYou have {0} seconds\n".format(timeout))
        signal.alarm(timeout)
        unput = input()
        signal.alarm(0)
    except InputTimedOut:
        pass
    return unput


def checked_today(new_services_path):
    print("\n\n##########################\n#  ALREADY SCANNED TODAY #\n##########################\n")
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    service_files = [f for f in listdir(new_services_path) if isfile(join(new_services_path, f))]
    today = date.today().strftime("%Y_%m_%d")
    today_files = [f for f in service_files if today in f]

    if not today_files:
        print("No new services found today... Running Scan again.")
        return 0
    print("A file with these services found already today:")

    for file in today_files:
        print(file.split("_")[-1])
    print("\nPreparing to scan for services again...")

    scan_again = input_with_timeout(timeout=5)
    if not scan_again:
        print('No command, scanning again\n')
        return 0
    elif scan_again.lower() == "n":
        print('Not aborting scan, scanning again\n')
        return 0

    # Abort scan
    return 1


def dumb_crontab_fix():
    print("Current Working Directory " , getcwd())
    chdir("Desktop/AWSCalc")
    print("Current Working Directory " , getcwd())


def main():
    dumb_crontab_fix() # Goes from home to Desktop to run program in crontab

    selenium_output_dir = "SeleniumOutputs"
    lists_services_dir = "ListsOfServices"
    new_services_dir = "NewServicesDates"

    cwd_dir = getcwd()
    selenium_output_path = join(cwd_dir, selenium_output_dir)
    lists_services_path = join(selenium_output_path, lists_services_dir)
    new_services_path = join(selenium_output_path, new_services_dir)

    if not exists(selenium_output_path):
        create_directories(selenium_output_path, lists_services_path, new_services_path)
    else:
        print("Directory '% s' already exists" % selenium_output_path)

    # Check for services list from today
    today_file_name = get_full_path_for_day_file(date.today(), lists_services_path)
    if exists(today_file_name):
        if checked_today(new_services_path):
            return
    print("\n")
    list_of_current_services = list_services()
    write_data_to_file(list_of_current_services, selenium_output_path, lists_services_path, new_services_path)

    print("\n===================================\n\n")
    return


if __name__ == "__main__":
    main()
