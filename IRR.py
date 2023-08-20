import csv
import numpy as np
from scipy.optimize import newton
import easygui as eg
from datetime import datetime


# Custom XIRR function
def xirr(values, dates, guess=0.1):
    """Calculate the XIRR equivalent of Excel's XIRR function.
    
    Args:
    vales (list of float): Cash flows.
    dates (list of datetime): Dates of the cash flows.
    guess (float, optional): Initial guess for the rate.
    
    Returns:
    float: The internal rate of return.
    """
    dates = np.array(dates)
    values = np.array(values)
    years = (dates - dates[0]).astype("timedelta64[D]").astype(int) / 365.0

    # Function to optimize
    def total(pv):
        return sum([v / (1 + pv) ** year for v, year in zip(values, years)])

    # Derivative function
    def df(pv):
        return sum([-year * v / (1 + pv) ** (year + 1)for v, year in zip(values, years)])

    # Use Newton's method to find the root
    return newton(total, guess, df, maxiter=100)


# Ask for the input method
input_methods = ["Import a CSV file", "Manually input"]
method = eg.buttonbox(msg="Choose your input method:", title="IRR Calculation", choices=input_methods)

if method == "Import a CSV file":
    # Prompt for CSV file
    file_path = eg.fileopenbox(msg="Select your CSV file:", title="IRR Calculation", filetypes="*.csv")

    # Read CSV file
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Unpack dates and cash flows
    dates, cash_flows = zip(*data[1:])  # Skip the column header
    cash_flows = [float(cf) for cf in cash_flows]
    n = len(cash_flows)  # Ask for the number of cash flows

elif method == "Manually input":
    # Ask for the number of cash flows
    n = eg.integerbox(msg="Enter the number of cash flows:", title="IRR Calculation", default=0, lowerbound=0,
                      upperbound=1000)

    # Initialize lists to store the dates and cash flows
    dates = []
    cash_flows = []

    # Get the dates and cash flows
    valid_cash_flows = False
    while not valid_cash_flows:
        dates = []
        cash_flows = []
        for i in range(n):
            correct_date = False
            while not correct_date:
                try:
                    date = eg.enterbox(msg=f"Enter the date of cash flow {i+1} (YYYY-MM-DD):", title="XIRR Calculation")
                    datetime.strptime(date, "%Y-%m-%d")  # Check if the date is in the correct format
                    correct_date = True
                except ValueError:
                    eg.msgbox("The date format is incorrect. Please enter the date in the format YYYY-MM-DD.",
                              title="Error")
            cash_flow = eg.enterbox(msg=f"Enter the amount of cash flow {i+1}:", title="XIRR Calculation", default="0",
                                    strip=True)
            cash_flow = float(cash_flow)
            dates.append(date)
            cash_flows.append(cash_flow)
        if np.any(np.array(cash_flows) < 0) and np.any(np.array(cash_flows) > 0):
            valid_cash_flows = True
        else:
            eg.msgbox(
                "Cash flows should have at least 1 negative and 1 positive cash flow. Please enter the cash flows again.",
                title="Error")

# Ask for confirmation and allow amendment
confirmed = False
while not confirmed:
    msg = "You entered the following dates and cash flows:\n\n"
    for i in range(n):
        msg += f"Cash flow {i+1}: Date = {dates[i]}, Amount = {cash_flows[i]}\n"
    msg += "\nAre these correct?"
    correct = eg.boolbox(msg, title="XIRR Calculation", choices=["Yes", "No"])
    if correct:
        # Check if there is at least one negative and one positive cash flow
        if np.any(np.array(cash_flows) < 0) and np.any(np.array(cash_flows) > 0):
            confirmed = True
        else:
            eg.msgbox(
                "Cash flows should have at least 1 negative and 1 positive cash flow. Please enter the cash flows again.",
                title="Error")
    else:
        valid_amendment = False
        while not valid_amendment:
            index = eg.integerbox(msg="Enter the number of the cash flow you want to amend:", title="XIRR Calculation",
                                  default=0, lowerbound=1, upperbound=n)
            correct_date = False
            while not correct_date:
                try:
                    date = eg.enterbox(msg=f"Enter the amended date of cash flow{index} (YYYY-MM-DD):",
                                       title="XIRR Calculation")
                    datetime.strptime(date, "%Y-%m-%d")  # Check if the date is in the correct format
                    correct_date = True
                except ValueError:
                    eg.msgbox("The date format is incorrect. Please enter the date in the format YYYY-MM-DD.",
                              title="Error")
            cash_flow = eg.enterbox(msg=f"Enter the amended amount of cash flow {index}:", title="XIRR Calculation",
                                      default="0", strip=True)
            cash_flow = float(cash_flow)
            dates[index - 1] = date
            cash_flows[index - 1] = cash_flow
            if np.any(np.array(cash_flows) < 0) and np.any(np.array(cash_flows) > 0):
                valid_amendment = True
            else:
                eg.msgbox(
                    "Cash flows should have at least 1 negative and 1 positive cash flow. Please amend the cash flows again.",
                    title="Error")

# Convert dates to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

# Calculate the XIRR
xirr_value = xirr(cash_flows, dates)

# Display the result
eg.msgbox(f"The Extended Internal Rate of Return (XIRR) is: {xirr_value*100:.2f}%", title="XIRR Calculation")
