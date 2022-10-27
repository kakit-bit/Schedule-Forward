from datetime import date, timedelta
import csv

# Script Determines Annual Schedule Based on User Entered Year and Pre-Determined 28 Week Schedule
# Script Outputs .csv file of Annual Schedule Compatible for Google Calendar Import

# User Input Error Check Functions
def is_number(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def in_range(value):
    if value not in range(2020,2100):
        return False
    else:
        return True

# Function to Get Year
def get_year():
    while True:
        year_string = input("Enter the Year to Generate For: ")
        # Check if Input is a Valid Number
        if not is_number(year_string):
            print("Not a valid input")
            continue
        target_year = int(year_string)

        if not in_range(target_year):
            print("Input not in range. Year must be post-2020.")
            continue
        return target_year

# Function Determines Current Date in Reference to Master Schedule - Proof of Concept Only
def find_current_week():
    # September 12, 2020 is the Known Point of Reference for First Week of Master Schedule
    # Find Number of Days Since Point of Reference
    reference_date = date(2020,9,12)
    today = date.today()
    days_elapsed = (today - reference_date)

    # Determine Current Week
    days_past = days_elapsed.days
    adjusted_elapsed_days = int(days_past + 7)
    current_week = int(adjusted_elapsed_days / 7)

    return current_week, days_past, adjusted_elapsed_days

# Function Determines New Year's Index Position in Master Schedule
def find_new_year(target_year):
    # September 12, 2020 is Point of Reference for First Week of Master Schedule
    # Find Number of Days Since Point of Reference
    reference_date = date(2020,9,12)

    # Determine Range of Calendar Year
    start_date = date(target_year, 1, 1)
    days_elapsed = (start_date - reference_date)

    # Determine Current Week
    days_past = days_elapsed.days
    adjusted_elapsed_days = int(days_past + 7)
    current_week = int(adjusted_elapsed_days / 7)

    return days_past

# Function Determines Current Year and Generates a List of All Days in the Year
def generate_year(target_year):
    # Determine Range of Calendar Year
    start_date = date(target_year,1,1)
    end_date = date(target_year,12,31)

    days_delta = end_date - start_date

    this_year = []

    for x in range(days_delta.days + 1):
        day = start_date + timedelta(days=x)
        this_year.append(day)

    return this_year

if __name__ == '__main__':

    # Pre-Determined Line Number Seven of SMH Haematology Lab
    seventh_line = [
        "D", "D", None, None, "D", "D", "D",  # Week 1
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",
        None, None, "V1", "V1", "V1", "V1", "V1",
        None, None, "D", "D", "D", "D", "D",
        "D", "D", None, None, "D", "D", "D",

        None, None, "V3", "V3", "V3", "V3", "V3",  # Week 7
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", None,
        "N", "N", None, "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",

        None, None, "D", "D", "D", "D", "D",  # Week 13
        None, None, "E", "E", "E", "E", "E",
        "E", "E", None, None, "D", "D", "D",
        None, None, "V4", "V4", "V4", "V4", "V4",
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",

        None, None, "D", "D", "D", "D", None,  # Week 19
        "N", "N", None, "D", "D", "D", "D",
        None, None, "V2", "V2", "V2", "V2", "V2",
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",
        "D", "D", None, None, "D", "D", "D",

        None, None, "E", "E", "E", "E", "E",  # Week 25
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",
        None, None, "D", "D", "D", "D", "D",
    ]

    target_year = get_year()
    this_year = generate_year(target_year)
    new_year_index = find_new_year(target_year)

    result = {i : seventh_line[(counter+new_year_index) % len(seventh_line)] for counter, i in enumerate(this_year)}

    csv_title = "my_csv_schedule_"+str(target_year)+".csv"
    with open(csv_title, 'w', newline='') as f:
        the_writer = csv.writer(f)
        the_writer.writerow(["Subject", "Start Date", "Start Time"])
        for k, v in result.items():
            if v == 'D':
                the_writer.writerow(["Days",k,"07:00 AM"])
            elif v == 'V1':
                the_writer.writerow(["V1 Days",k,"07:00 AM"])
            elif v == 'V2':
                the_writer.writerow(["V2 Days",k,"07:00 AM"])
            elif v == 'V3':
                 the_writer.writerow(["V3 Days",k,"07:00 AM"])
            elif v == 'V4':
                the_writer.writerow(["V4 Days",k,"07:00 AM"])
            elif v == 'E':
                the_writer.writerow(["Evenings",k, "03:00 PM"])
            elif v == 'N':
                the_writer.writerow(["Nights",k, "11:00 PM"])