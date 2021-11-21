from os import listdir, mkdir, getcwd, chdir
from os.path import join, isfile, exists
from datetime import date, timedelta, datetime
from sys import platform


top_of_file = "\n\n\
=============================================================================\n\
Between {first_date} and {last_date}, there were {num_serv} services added \n\
\n\nService                                              | Date           \n\
---------------------------------------------------- | ---------------\n"

bottom_of_file = "\n\n\n\n\
=============================================================================\n\
"
max_len = 52


def intdate(date_in, reverse):
    date_list = [x for x in date_in.split("/")]
    if reverse:
        date_list.reverse()
    return_str = ""
    for y in date_list:
        return_str = return_str + y
    return int(return_str)


def write_summary(new_path, time_stamp, reverse):
    service_files = [f for f in listdir(new_path) if isfile(join(new_path, f))]
    service_files.sort()

    deprecated_list = []
    service_list = []
    first_date = "99999999"
    last_date = "0"
    for service in service_files:
        service = service.split(".")[0]  # Get rid of .txt
        service_str = ""
        service_date = ""
        if service == ".DS_Store" or not service:
            continue

        service_split = service.split("_")
        deprecated = False
        if reverse:
            service_split.reverse()
        for stuff in service_split:
            if stuff == "ZZZ" or stuff == "DEPRECATED":
                deprecated = True
                continue
            if stuff.isdigit():
                service_date = service_date + stuff + "/"
            else:
                service_str = stuff

        service_date = service_date[:-1]  # take off trailing /
        if intdate(service_date, reverse) > intdate(last_date, reverse):
            last_date = service_date
        if intdate(service_date, reverse) < intdate(first_date, reverse):
            first_date = service_date

        if deprecated:
            deprecated_list.append((service_date, service_str))
        else:
            service_list.append((service_date, service_str))

    with open("AutomatedSummary.txt", "w") as file:
        # Beginning of file
        file.write("This File Was Last Updated: ")
        file.write(time_stamp)
        file.write(" (Pacific Time; PDT=UTC-7:00 or PST=UTC-8:00)\n\n")

        global top_of_file
        top_of_file = top_of_file.replace("{first_date}", first_date)
        top_of_file = top_of_file.replace("{last_date}", last_date)
        top_of_file = top_of_file.replace("{num_serv}", str(len(service_list)))
        file.write(top_of_file)

        # Non-deprecated Services with dates
        prev_mth = None
        global max_len
        for service_date, service_str in service_list:
            service_str = service_str+(" "*(max_len - len(service_str)))
            # Add a blank line between months - doesn't work in table...
            # if prev_mth != None and prev_mth != service_date.split("/")[1]:
            #     file.write((" "*max_len)+" | \n")
            file.write(service_str+" | "+service_date+"  \n")
            prev_mth = service_date.split("/")[1]

        # End of file
        global bottom_of_file
        file.write(bottom_of_file)


def crontab_chdir_fix():
    print("Current Working Directory ", getcwd())
    if platform == "linux" or platform == "linux2":  # linux
        chdir("wilburtw/AWSPricingCalc")
    elif platform == "darwin":  # OS X
        chdir("wilburtw/Desktop/AWSPricingCalc")
    else:
        print("Operating System not supported. Use Linux or MacOS.")
        exit()
    print("Current Working Directory ", getcwd())


def main():
    crontab_chdir_fix()  # Goes from home to Desktop to run program in crontab

    selenium_output_dir = "SeleniumOutputs"
    lists_services_dir = "ListsOfServices"
    new_services_dir = "NewServicesDates"

    reverse = False
    selenium_output_path = join(getcwd(), selenium_output_dir)

    lists_services_path = join(selenium_output_path, lists_services_dir)
    new_path = join(selenium_output_path, new_services_dir)

    # current_time = datetime.now().strftime("%H:%M:%S")
    current_utc_time = datetime.now().strftime("%H:%M:%S")
    time_stamp = str(date.today()) + " " + str(current_utc_time)
    print("\nCurrent Date and Time: ", time_stamp)
    write_summary(new_path, time_stamp, reverse)
    print("Summary Generated.")
    return


if __name__ == "__main__":
    main()
