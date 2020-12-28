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


def get_full_path_for_day_file(day, list_path):
    str_date = day.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+str_date
    complete_file_name = join(list_path, partial_file_name+".txt")
    return complete_file_name


def create_directories(output_path, list_path, change_path):
    mkdir(output_path)
    mkdir(list_path)
    mkdir(change_path)
    print("Directory '% s' created" % output_path)
    return


def write_new_services_file(change_path, new_services, deprecated=False):
    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")

    if deprecated:
        partial_file_names = ["ZZZ_"+date_today+"_DEPRECATED_"+service for service in new_services]
    else:
        partial_file_names = [date_today+"_"+service for service in new_services]

    for partial_file_name in partial_file_names:
        complete_file_name = join(change_path, partial_file_name+".txt")
        with open(complete_file_name, "w") as file:
            file.write(partial_file_name+"\n")
    for service in new_services:
        print(service, "has been written to new file.\n")
    return


def check_previous_file(list_of_current_services, output_path, list_path, change_path):
    today = date.today()
    # YY_mm_dd

    date_before = get_day_before(today)
    old_services = []
    # Checking if the list directory is empty or not
    if len(os.listdir(list_path)) == 0:
        print("Last Scan: Never")
    else:
        previous_day_file_name = get_full_path_for_day_file(date_before, list_path)
        while not exists(previous_day_file_name):
            print("File from ", date_before, " does not exist. Looking for day before.", sep='')
            date_before = get_day_before(date_before)
            previous_day_file_name = get_full_path_for_day_file(date_before, list_path)

        with open(previous_day_file_name, "r") as file:
            print("Last Scan: ", previous_day_file_name)
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
        write_new_services_file(change_path, new_services)
        print("\n\n########################\n# NEW SERVICE(S) ADDED #\n########################\n")
        for service in new_services:
            print(service, "\n")
    else:
        print("No new services found since last scan.")

    if deprecated:
        write_new_services_file(change_path, deprecated, True)
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


def write_data_to_file(list_of_current_services, output_path, list_path, change_path):
    # Write data to unique file

    today = date.today()
    # YY_mm_dd
    date_today = today.strftime("%Y_%m_%d")
    partial_file_name = "PricingCalcList_"+date_today
    complete_file_name = join(list_path, partial_file_name+".txt")
    with open(complete_file_name, "w") as file:
        file.write(str(len(list_of_current_services))+"\n")
        print(len(list_of_current_services), " services found today.")
        for service_name in list_of_current_services:
            file.write(service_name+"\n")

    if len(os.listdir(path)) == 0:
        print("Empty directory")
    check_previous_file(list_of_current_services, output_path, list_path, change_path)
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


def checked_today(change_path):
    print("\n\n##########################\n#  ALREADY SCANNED TODAY #\n##########################\n")
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    service_files = [f for f in listdir(change_path) if isfile(join(change_path, f))]
    today = date.today().strftime("%Y_%m_%d")
    today_files = [f for f in service_files if today in f]

    if not today_files:
        print("No files found today... Running Scan again.")
        return 0
    print("Files found already today:")

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

    output_dir = "SeleniumOutputs"
    list_dir = "ListsOfServices"
    change_dir = "NewServicesDates"

    cwd_dir = getcwd()
    output_path = join(cwd_dir, output_dir)
    list_path = join(output_path, list_dir)
    change_path = join(output_path, change_dir)

    if not exists(output_path):
        create_directories(output_path, list_path, change_path)
    else:
        print("Directory '% s' already exists" % output_path)

    # Check for services list from today
    today_file_name = get_full_path_for_day_file(date.today(), list_path)
    if exists(today_file_name):
        if checked_today(change_path):
            return
    print("\n")
    list_of_current_services = list_services()
    write_data_to_file(list_of_current_services, output_path, list_path, change_path)

    print("\n===================================\n\n")
    return


if __name__ == "__main__":
    main()
