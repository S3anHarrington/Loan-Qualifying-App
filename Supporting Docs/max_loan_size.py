# -*- coding: utf-8 -*-
"""Max Loan Size Filter.

This script filters the bank list by comparing the user's loan value
against the bank's maximum loan size.

"""
import sys
import csv
from pathlib import Path

def filter_max_loan_size(loan_amount, bank_list):
    """Filters the bank list by the maximum allowed loan amount.

    Args:
        loan_amount (int): The requested loan amount.
        bank_list (list of lists): The available bank loans.

    Returns:
        A list of qualifying bank loans.
    """


    loan_size_approval_list = []

    approved_banks = Path('Desktop/daily_rate_sheet.csv')
    with open(approved_banks, 'r') as csvfile:
        bank_list = csv.reader(csvfile)
        for bank in bank_list:
            if loan_amount >= int(bank[1]):
                loan_size_approval_list.append(bank)
    print(loan_size_approval_list)
     
    return loan_size_approval_list
