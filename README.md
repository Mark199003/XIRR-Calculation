# XIRR Calculation Program

This Python program calculates the Extended Internal Rate of Return (XIRR) for a series of cash flows occurring at irregular intervals. The XIRR is equivalent to Excel's XIRR function. Users can input the cash flows either by importing a CSV file or manually through a GUI.

## Dependencies

The program uses the following Python libraries:

- `csv` for reading CSV files.
- `numpy` for numerical analysis.
- `scipy.optimize` for optimization algorithms.
- `easygui` for creating a simple GUI.
- `datetime` for dealing with dates and times.

You can install `numpy`, `scipy`, and `easygui` using pip:

```
pip install numpy scipy easygui
```

## Usage

To use the program, run it in a Python environment. A GUI will ask you to choose your input method. You can choose to either import a CSV file or manually input the cash flows.

### Import a CSV File

If you choose to import a CSV file, the program will prompt you to select your CSV file. The CSV file should have two columns: the first column for the dates of the cash flows and the second column for the amounts of the cash flows. The dates should be in the format `YYYY-MM-DD`, and the amounts should be numerical. The first row of the CSV file is assumed to be the column header and will be skipped.

### Manually Input

If you choose to manually input the cash flows, the program will first ask you to enter the number of cash flows. Then, for each cash flow, it will ask you to enter the date and amount. The date should be in the format `YYYY-MM-DD`, and the amount should be numerical.

## Confirmation and Amendment

After you have inputted all the cash flows, the program will display them for your confirmation. If there is anything incorrect, you can choose to amend them. The program will ask you to enter the number of the cash flow you want to amend, and then enter the amended date and amount.

## Calculation and Result

After you have confirmed the cash flows, the program will calculate the XIRR and display the result. The XIRR is expressed as a percentage.

## Notes

For the XIRR to be valid, the cash flows should have at least one negative cash flow (outflow) and one positive cash flow (inflow). If the cash flows do not meet this requirement, the program will ask you to enter them again.
