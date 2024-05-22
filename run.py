import gspread
from google.oauth2.service_account import Credentials
# from datetime import datetime


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
    validate_team_names(team_a)
    team_b = input('Team B name:\n')
    validate_team_names(team_b)

    return (team_a, team_b)

def validate_team_names(data):
    try:
        # Check if the data is empty
        if data == "":
            raise ValueError("Input cannot be empty.")
        
        # If the check passes, the input is valid
        return True

    except ValueError as e:
        # Print the error message and return False to indicate invalid input
        print(f"Validation error: {e}")
        return False

def get_scores_data(team_name):
    """
    Get scores data input from user.
    Run a while loop to get valid data from the user.
    Data should be in a string of 6 numbers (0-6) or letter W 
    if a player is out. The loop will repeatedly request data, 
    until it is valid. 
    """
    print(f"""
Please enter the scores for {team_name}, one over at a time.


    """)
    # print("Please enter the scores, one over at a time.")
    # print("Scores can be 0-6 or 'W' if a player is out." )
    # print('Enter 6 scores for the over, each seperated by a comma.')
    # print("Example: 0,2,1,4,W,0\n")
    #change range back to 20
    for i in range(3):
        while True:
            score_str = input(f"Enter the score for {team_name}'s over ({i + 1}/20:)\n")
            score_over = score_str.split(",")
            print('test', score_over)

            if validate_data(score_over):
                print("Data is valid!\n")
                final_score_over = [team_name] + [i] + score_over
                update_scoresheet(final_score_over, 'Team A', team_name)
                break  
            
    print('Innings complete.\n')

    return [team_name, score_over]

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

def update_scoresheet(data, worksheet, team_name):
    """
    Update the scoresheet with the scores from the over.
    Players total is talleyed aswell as the teams total.
    """
    # today_now = datetime.now()
    # today_now_formated = today_now.strftime("%Y-%m-%d %H:%M:%S")

    print('Updating scoresheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print('Scoresheet updated successfully\n')

def main():
    """
    Run all program functions
    """
    team_a, team_b = enter_team_names()
    print(team_a, team_b)
    team_a_scores = get_scores_data(team_a)
    team_b_scores = get_scores_data(team_b)
    # update_scoresheet(score_over, 'Team A')


print("Welcome to Cricket Scoresheet")
main()
