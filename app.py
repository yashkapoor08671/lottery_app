import pandas as pd
import streamlit as st

# Load the lottery data (ensure '649.csv' is in the same directory)
lottery_canada = pd.read_csv('649.csv')

def factorial(n):
    if n == 0:
        return 1
    final_product = 1
    for i in range(n, 0, -1):
        final_product *= i
    return final_product

def combinations(n, r):
    return factorial(n) / (factorial(r) * factorial(n - r))

def extract_numbers(row):
    return set(row[4:10])

# Historical winning numbers
historical_numbers = lottery_canada.apply(extract_numbers, axis=1)

# Streamlit app
st.title("Lottery Number Checker API")

# Input for single ticket probability
st.header("Check Single Ticket Probability")
user_numbers_input = st.text_input("Enter your 6 numbers separated by commas:", "1,2,3,4,5,6")
if st.button("Check Winning Probability"):
    user_numbers = list(map(int, user_numbers_input.split(',')))
    n_combinations = combinations(49, 6)
    user_numbers_set = set(user_numbers)

    n_occurrences = historical_numbers.apply(lambda x: user_numbers_set == x).sum()

    if n_occurrences == 0:
        st.write(f"The combination {user_numbers} has never occurred.")
        st.write("Your chances to win the big prize in the next drawing are 0.0000072%.")
        st.write("In other words, you have a 1 in 13,983,816 chance to win.")
    else:
        st.write(f"The number of times combination {user_numbers} has occurred in the past is {n_occurrences}.")
        st.write("Your chances to win the big prize in the next drawing are 0.0000072%.")
        st.write("In other words, you have a 1 in 13,983,816 chance to win.")

# Input for multi-ticket probability
st.header("Calculate Multi-Ticket Probability")
n_tickets = st.number_input("Enter number of tickets:", min_value=1, value=1, step=1)
if st.button("Calculate Probability"):
    n_combinations = combinations(49, 6)
    probability = n_tickets / n_combinations * 100
    combinations_simplified = round(n_combinations / n_tickets)

    if n_tickets == 1:
        st.write(f"Your chances to win the big prize with one ticket are {probability:.6f}%.")
        st.write(f"In other words, you have a 1 in {int(n_combinations)} chance to win.")
    else:
        st.write(f"Your chances to win the big prize with {n_tickets:,} different tickets are {probability:.6f}%.")
        st.write(f"In other words, you have a 1 in {combinations_simplified} chance to win.")

# Input for winning number probabilities
st.header("Calculate Probability of Winning Numbers")
n_winning_numbers = st.number_input("Enter number of winning numbers (0 to 6):", min_value=0, max_value=6, value=0)
if st.button("Calculate Winning Numbers Probability"):
    n_combinations_ticket = combinations(6, n_winning_numbers)
    n_combinations_remaining = combinations(43, 6 - n_winning_numbers)
    successful_outcomes = n_combinations_ticket * n_combinations_remaining

    n_combinations_total = combinations(49, 6)
    probability = successful_outcomes / n_combinations_total * 100
    combinations_simplified = round(n_combinations_total / successful_outcomes)

    st.write(f"Your chances of having {n_winning_numbers} winning numbers with this ticket are {probability:.6f}%.")
    st.write(f"In other words, you have a 1 in {combinations_simplified} chance to win.")


