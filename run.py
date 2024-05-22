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
    print("Please enter the scores, one over at a time.")
    print("Scores can be 0-6 or 'W' if a player is out." )
    print('Enter 6 scores for the over, each seperated by a comma.')
    print("Example: 0,2,1,4,W,0\n")
    for i in range(20):
        while True:
            score_str = input(f"Enter the score from the over {i + 1}/20:\n")
            score_over = score_str.split(",")

            if validate_data(score_over):
                print("Data is valid!\n")
                update_scoresheet(score_over, 'Team A')
                break  

    return score_over

def validate_data(data):
    """
    Validate the data that has been inputed.
    Only allowing the numbers 0-6 or the letter 
    'W' which represents a player getting out.
    """
    try:
        # Check if the input string length is exactly 6
        if len(data) != 6:
            raise ValueError("Input must contain exactly 6 characters.")

        # Check each character in the input string
        for input in data:
            if input not in '0,1,2,3,4,5,6,w,W':
                raise ValueError(f"Invalid character found: {input}")

        # If all checks pass, the input is valid
        return True

    except ValueError as e:
        # Print the error message and return False to indicate invalid input
        print(f"Validation error: {e}")
        return False

def update_scoresheet(data, worksheet):
    """
    Update the scoresheet with the scores from the over.
    Players total is talleyed aswell as the teams total.
    """
    print('Updating scoresheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print('Scoresheet updated successfully\n')

def main():
    """
    Run all program functions
    """
    enter_team_names()
    score = get_scores_data()
    update_scoresheet(score_over, 'Team A')


print("Welcome to Cricket Scoresheet")
main()