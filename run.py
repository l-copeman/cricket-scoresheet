import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cricket_scoresheet')

def enter_team_names():
    """
    Enter the names of the two teams playing this game
    """
    print('Please enter the two team names for this game.')

    team_a = input('Team A name:\n')
    team_b = input('Team B name:\n')

    return (team_a, team_b)

def get_scores_data():
    """
    Get scores data input from user.
    Run a while loop to get valid data from the user.
    Data should be in a string of 6 numbers (0-6) or letter W 
    if a player is out. The loop will repeatedly request data, 
    until it is valid. 
    """
    while True:
        print("Please enter the scores from the last over.")
        print("Scores can be 0-6 or 'W' if a player is out." )
        print('Enter 6 scores for the over, each seperated by a comma.')
        print("Example: 0,2,1,4,W,0\n")

        score_str = input("Enter the score from the over:\n")

        score_data = score_str.split(",")

        if validate_data(score_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data():
    """
    Validate...
    """


def main():
    """
    Run all program functions
    """
    enter_team_names()
    get_scores_data()


print("Welcome to Cricket Scoresheet")
main()