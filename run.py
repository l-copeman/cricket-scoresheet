import gspread
from google.oauth2.service_account import Credentials
import datetime


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('cricket_scoresheet')

team_a = {
    "name": None,
    "total": [],
    "wickets": []
}

team_b = {
    "name": None,
    "total": [],
    "wickets": []
}

def ask_for_date():
    while True:
        date_input = input("Enter the date in the format dd/mm/yy: \n")
        try:
            # Attempt to parse the date
            date_object = datetime.datetime.strptime(date_input, '%d/%m/%y')
            # If parsing is successful, break the loop and return the date
            return date_object.strftime('%d/%m/%y')
        except ValueError:
            # If parsing fails, inform the user and ask for input again
            print("Invalid date format. Please try again.")

    return date_input        

def enter_team_names():
    """
    Enter the names of the two teams playing this game
    """
    print('Please enter the two team names for this game.')
    global team_a
    global team_b

    while True:
        team_a['name'] = input('Team A name:\n')
        team_b['name'] = input('Team B name:\n')
        
        if validate_team_names(team_a['name'], team_b['name']):
            break

    return (team_a, team_b)

def validate_team_names(name_a, name_b):
    try:
        # Check if the data is empty
        if (name_a, name_b) == "":
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
Scores can be 0-6 or 'W' if a player is out.
Enter 6 scores for the over, each seperated by a comma.
Example: 0,2,1,4,W,0
    """)

    #change range back to 20 after testing
    for i in range(3):
        while True:
            score_str = input(f"Enter the score for {team_name}'s over ({i + 1}/20:)\n")
            score_stripped = score_str.replace(" ", "")
            str_list = score_stripped.split(",")
            score_over = list(filter(None, str_list))
            
            if validate_data(score_over):
                print("Data is valid!\n")
                total_over = calculate_total_over(score_over, team_name)
                wickets_lost = calculate_wickets_lost(score_over, team_name)
                final_score_over = [team_name] + [i] + score_over + [total_over] + [wickets_lost]
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

    # print('Updating scoresheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    # print('Scoresheet updated successfully\n')

def calculate_total_over(total, team_name):
    """
    Calculate total score....
    """
    # Convert the list of strings to a list of integers, ignoring non-integer values
    int_data = []
    for num in total:
        try:
            int_data.append(int(num))
        except ValueError:
            # Ignore the value if it cannot be converted to an integer
            continue
    
    total_over_score = sum(int_data)

    if team_name == team_a['name']:
        team_a['total'].append(total_over_score)
    else:
        team_b['total'].append(total_over_score)


def calculate_wickets_lost(data, team_name):
    """
    Calculate wickets lost...
    """
    count = 0

    for item in data:
        # Count occurrences of 'w' in the current string and add to the total count
        count += item.count('w') + item.count('W')

    if team_name == team_a['name']:
        team_a['wickets'].append(count)
    else:
        team_b['wickets'].append(count)

    return count

def main():
    """
    Run all program functions
    """
    global team_a
    global team_b
    todays_date = ask_for_date()
    enter_team_names()
    # Appends title for this match: date and name of two teams
    title_header = [todays_date] + [team_a['name']] + [team_b['name']]
    update_scoresheet(title_header, 'Team A', 0)
    # Appends header row for scoresheet
    header_row = ['Team Name', 'Over','','','','','','','Total','Wickets']
    update_scoresheet(header_row, 'Team A', 0)
    team_a_scores = get_scores_data(team_a['name'])
    # Appends header row for scoresheet
    header_row = ['Team Name', 'Over','','','','','','','Total','Wickets']
    update_scoresheet(header_row, 'Team A', 0)
    team_b_scores = get_scores_data(team_b['name'])

    print(team_a)
    print(team_b)

print("Welcome to Cricket Scoresheet")
main()
