"""
    File name: energy_consumption_by_corporates.py
    Author: Lawrence Liu
    Date created: April 7th, 2022
    Python Version: 3.10

    Description: Takes Calgary's Open Data API (https://dev.socrata.com/foundry/data.calgary.ca/crbp-innf) and sorts
    the data into alphabetical order. This program will ask some specific questions in order to narrow down the data
    needed to display the total energy consumed each month for that year.
"""

# imports
import json
import urllib.request
from datetime import datetime
import matplotlib.pyplot as plt

# import JSON file from Socrata's Open Calgary API
# Contains information licensed under the Open Government Licence – City of Calgary.
JSON_FILE = "https://data.calgary.ca/resource/crbp-innf.json"

"""
Sample data:
        "business_unit_desc": "Calgary Comm Standards",
        "facilityname": "INACTIVE - EC - UTILITY YARD - CM",
        "site_id": "0020004409284",
        "facilityaddress": "3030 68 ST SE",
        "energy_description": "Electricity",
        "year": "2014",
        "month": "Jan",
        "total_consumption": "63",
        "unit": "kWh"
"""


# contains the four main methods used to grab the data
def main():
    load_time()
    data = load_data()
    filter_data(data)
    continue_program()


# displays what time it currently is
def load_time():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    print("The current time is: {}".format(time))


# loads the data from the JSON file and displays how long it takes to load the data
def load_data():
    starttime = datetime.now()

    print("Welcome to the 'Energy Consumption used by Corporates in Calgary'.")
    print("")

    with urllib.request.urlopen(JSON_FILE) as url:
        data = json.loads(url.read().decode())

    print("Time took to load data: {}".format(datetime.now() - starttime))

    return data


# begins to filter the data through various questions
def filter_data(data):
    """
    :param data: receives the JSON file from 'load_data'
    """
    print("")

    # stores the energy unit
    store_unit = ""

    # stores the total value of energy consumption
    store_consumption_value = 0

    # lists to hold data received from the JSON file
    holdFacility = []
    holdMonths = []
    holdYears = []
    holdEnergy = []
    holdConsumption = []

    print("Here are the facilities you can choose from: ")

    # puts the facility name into a list
    for facility in data:
        if facility.get("business_unit_desc") not in holdFacility:
            holdFacility.append(facility.get("business_unit_desc"))

    # prints out the facility names
    print(holdFacility)

    # empty print statement to space out text
    print("")

    # asks the user a question on which facility they want
    facility_answer = facility_ask_question()

    # checks to see if the facility exist
    if facility_answer not in holdFacility:
        print("That facility does not exist. Check the spelling and try again.")
        filter_data(data)

    print("")
    print("Please choose a year from this selection.")

    # puts the year into a list
    for year in data:
        if facility_answer == year.get("business_unit_desc") and year.get("year") not in holdYears:
            holdYears.append(year.get("year"))

    # stores the years into numerical order
    holdYears.sort()
    print(holdYears)
    year_user_input = input()

    # checks to see if the year exist
    if year_user_input not in holdYears:
        print("That year is not available. Try again.")
        filter_data(data)

    print("")
    print("Please choose a specific energy.")

    # puts the energy type into a list
    for energy_data in data:
        if year_user_input == energy_data.get("year") and energy_data.get("energy_description") not in holdEnergy:
            holdEnergy.append(energy_data.get("energy_description"))

    # sorts the energy type in alphabetical order
    holdEnergy.sort()
    print(holdEnergy)
    energy_user_input = input()

    # checks to see if the energy type exist
    if energy_user_input not in holdEnergy:
        print("Energy chosen does not exist. Check your spelling and try again.")
        filter_data(data)

    print("")

    # prints out the selection the user has picked
    print("Here is your selections: {}, {}, {}".format(facility_answer, year_user_input, energy_user_input))

    # using the data the user chose, it now searches for that specific data in the JSON file
    for specific_data in data:

        # if it finds the exact match...
        if facility_answer == specific_data.get("business_unit_desc") and year_user_input == specific_data.get(
                "year") and energy_user_input == specific_data.get("energy_description"):

            # if the month, such as Jan, exist in the list "holdMonths", then add the consumption value
            if specific_data.get("month") in holdMonths:
                store_consumption_value += int(specific_data.get("total_consumption"))

            # otherwise, add the month to the "holdMonths" list
            else:
                holdMonths.append(specific_data.get("month"))

                # and if the consumption value is not 0, add it to the "holdConsumption" list and reset the value to 0
                if store_consumption_value != 0:
                    holdConsumption.append(store_consumption_value)
                    store_consumption_value = 0

            # grab the energy unit for this specific data
            store_unit = specific_data.get("unit")

    # for the final consumption value, we add it after the for loop in order to ensure all the data is added
    holdConsumption.append(store_consumption_value)

    # this data now is shown in the console
    print("Months: {}".format(holdMonths))
    print("Consumption: {}".format(holdConsumption))

    # bar graph is created
    bar_graph(holdConsumption, holdMonths, facility_answer, year_user_input, energy_user_input, store_unit)


def facility_ask_question():
    print(
        "From these choices, type in which facility you would like to explore. Make sure to type in the full. If you "
        "would like to exit, type in 'EXIT' "
        "facility name.")
    user_input_answer = input()

    return user_input_answer


def bar_graph(holdConsumption, holdMonths, facility_answer, year_user_input, energy_user_input, store_unit):

    """
    :param holdConsumption: list of total consumption values
    :param holdMonths: list of all months for specific data
    :param facility_answer: grabs the user's chosen facility name
    :param year_user_input: grabs the user's chosen year
    :param energy_user_input: grabs the user's chosen energy type
    :param store_unit: grabs the specific energy unit used for the data
    :return: a bar graph that shows energy used per month in that year
    """

    # plt is our way to create the bar graph
    plt.title(facility_answer + ", " + year_user_input + " for " + energy_user_input)
    plt.xlabel("Months")
    plt.ylabel("Energy Consumed in " + store_unit)

    # plt.bar(x, y)
    plt.bar(holdMonths, holdConsumption)
    plt.show()


def continue_program():
    print("Do you wish to continue the program? (Y/N)")
    answer_user_input = input()

    if answer_user_input.lower() == "y":
        main()
    elif answer_user_input.lower() == "n":
        exit()
    else:
        print("Input either 'Y' or 'N' to continue or exit the program.")
        continue_program()


if __name__ == '__main__':
    main()
