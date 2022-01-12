# -*- coding: utf-8 -*-
"""Loan Qualifier Application. This is a command line application to match applicants with qualifying loans."""

# Begin by importing all the necessary libraries and filters.

import sys
import fire
import questionary
import csv
import os
from pathlib import Path


from fileio import load_csv, save_csv

from calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from max_loan_size import filter_max_loan_size
from credit_score import filter_credit_score
from debt_to_income import filter_debt_to_income
from loan_to_value import filter_loan_to_value


     
def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
    The bank data from the data rate sheet CSV file.
    """
    # We begin by loading our program, listed below is the current path we are using. 

    # The load bank data is our main file we are using to import all information in order to calculate the loan.
    # We have an if not statement that allows the program to shut down if the correct path isnot entered.

    #csvpath = Path('Desktop/app.py')
    csvpath = questionary.text("What is the CSV file path?").ask()
    if not os.path.exists(csvpath):
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_bank_data


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
    Returns the applicant's financial information.
    """

    # Below are listed a series of questons to determine which banks will approve your loan.
    # Provided next to each question is are sample answers used in the model.

    credit_score = questionary.text("What's your credit score?").ask() # 790
    debt = questionary.text("What's your current amount of monthly debt?").ask() # 1000
    income = questionary.text("What's your total monthly income?").ask() # 3000
    loan_amount = questionary.text("What's your desired loan amount?").ask() # 100000
    home_value = questionary.text("What's your home value?").ask() # 450000

    # Here we assign the intgers for our upcoming data filters.

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
            - Credit Score
            - Loan Size
            - Debit to Income ratio (calculated)
            - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # This save command funtion allows the members to save the qualified data to a CSV file of their choosing.
    # We are utilizing an if, elif, and else statement to give the saving option to ours users.

    # In this instance we are using the file path 'Desktop/qualifying_loans.csv'.
    
    save_text = questionary.confirm("You are saving loans to a CSV file").ask()

    if save_text == True: # Yes
        save_csv(Path('Desktop/qualifying_loans.csv'), qualifying_loans)
        print('Saved!')
    
    elif save_text == False: # No
        print('Not Saved')

    else: # All other responces will print an "Error" message.
       print('\n Invalid Option. Please Enter a Valid Option.')

    return qualifying_loans



def run():
    """The main function for running the script."""
    # The run statment tells the program to run in this order of operations allowing our users to make the most of our product.

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)
 
if __name__ == "__main__":
    fire.Fire(run)
