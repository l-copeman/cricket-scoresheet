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
    """
    Ask the user to enter the date of the game
    Date entered should be in the format dd/mm/yy
    If not entered correctly, user is asked to re-enter
    """
    while True:
        date_input = input("Enter the date for this game, format dd/mm/yy: \n")
        try:
            date_object = datetime.datetime.strptime(date_input, '%d/%m/%y')
            return date_object.strftime('%d/%m/%y')
        except ValueError:
            print("Invalid date format. Please try again.")

    return date_input      

def enter_team_names():
    """
    The user is asked for the names of the two teams
    Each team name must have a minimum of 3 characters
    Letters and numbers are accepted
    """
    print(f"""
Please enter the names of the two teams.
Each teams name must be a minimum of 3 characters.
    """)
    global team_a
    global team_b
    team_a['name'] = '' 
    while len(team_a['name'])< 3:
        team_a['name'] = input("Enter the name of the first team: ").strip().title()
    team_b['name'] = ''    
    while len(team_b['name'])< 3:
        team_b['name'] = input("Enter the name of the second team: ").strip().title()       

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

    #change range back to 10 after testing
    for i in range(1):
        while True:
            score_str = input(f"Enter the score for {team_name}'s over ({i + 1}/10:)\n")
            score_stripped = score_str.replace(" ", "")
            str_list = score_stripped.split(",")
            score_over = list(filter(None, str_list))
            
            if validate_data(score_over):
                print("Data is valid!\n")
                total_over = calculate_total_over(score_over, team_name)
                wickets_lost = calculate_wickets_lost(score_over, team_name)
                final_score_over = [team_name] + [i] + score_over + [total_over] + [wickets_lost]
                update_scoresheet(final_score_over, 'Scores')
                break  

    print('Innings complete.\n')

    return [team_name, score_over]

def validate_data(data):
    """
    Validate the data that has been inputted.
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
    Function that updates the worksheet
    """
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)

def calculate_total_over(total, team_name):
    """
    Converts the data to a list of integers,
    ignoring non-integer values (W).
    Finds the sum of the data and appends it to
    the relevant dictionary
    """
    # Convert the list of strings to a list of integers, ignoring non-integer values
    int_data = []
    for num in total:
        try:
            int_data.append(int(num))
        except ValueError:
            continue
    # Adds the list of integers 
    total_over_score = sum(int_data)
    # Appends the data to the relevant dictionary
    if team_name == team_a['name']:
        team_a['total'].append(total_over_score)
    else:
        team_b['total'].append(total_over_score)

    return total_over_score    

def calculate_wickets_lost(data, team_name):
    """
    Calculates number of wickets lost in the over.
    Appends the data to the relevant dictionary 
    """
    count = 0
    for item in data:
        # Count occurrences of 'W' in the current string and add to the total count
        count += item.count('w') + item.count('W')
    if team_name == team_a['name']:
        team_a['wickets'].append(count)
    else:
        team_b['wickets'].append(count)
    return count

def final_score_append(team_name):
    """
    Calculates the total score for the innings (10 overs)
    by adding the values from the 'total' list in the dictionary
    Appends headings to scoresheet for Final Total
    """
    if team_name['name'] == team_a['name']:
        end_score_a = sum(team_a['total'])
        end_wickets_a = sum(team_a['wickets'])
        team_a_final = ['','','','','','','', 'Final Total',end_score_a,end_wickets_a]
        update_scoresheet(team_a_final, 'Scores')

    else:
        end_score_b = sum(team_b['total'])
        end_wickets_b = sum(team_b['wickets'])
        team_b_final = ['','','','','','','', 'Final Total',end_score_b,end_wickets_b]
        update_scoresheet(team_b_final, 'Scores')

def calculate_winner():
    """
    Compares the final score values to determine the winner
    If scores are equal, the team which has lost the least
    wickets is the winner.
    """
    end_score_a = sum(team_a['total'])
    end_score_b = sum(team_b['total'])

    end_wickets_a = sum(team_a['wickets'])
    end_wickets_b = sum(team_b['wickets'])
 
    print(team_a['name'], 'final score', end_score_a,'/',end_wickets_a)
    print(team_b['name'], 'final score', end_score_b,'/',end_wickets_b)
    
    if end_score_a > end_score_b:
        print(team_a['name'] ,'are the winners\n')
    elif end_score_b > end_score_a:
        print(team_b['name'] ,'are the winners\n')   
    else:
        if end_wickets_a < end_wickets_b:
            print(team_a['name'] ,'are the winners\n')  
        elif end_wickets_b < end_wickets_a:
             print(team_b['name'] ,'are the winners\n')          
        else:
            print('Game is tied')       
 
def main():
    """
    Run all program functions
    """
    print("Welcome to Cricket Scoresheet")
    global team_a
    global team_b
    todays_date = ask_for_date()
    enter_team_names()
    # Appends title for this match: date and name of two teams
    title_header = [todays_date] + [team_a['name']] + [team_b['name']]
    update_scoresheet(title_header, 'Scores')
    # Appends header row for scoresheet
    header_row = ['Team Name', 'Over','','','','','','','Total/Over','Wickets']
    update_scoresheet(header_row, 'Scores')
    team_a_scores = get_scores_data(team_a['name'])
    final_score_append(team_a)
    footer = ['-']
    update_scoresheet(footer, 'Scores')
    # Appends header row for scoresheet
    header_row = ['Team Name', 'Over','','','','','','','Total/Over','Wickets']
    update_scoresheet(header_row, 'Scores')
    team_b_scores = get_scores_data(team_b['name'])
    final_score_append(team_b)
    calculate_winner()
    # Creates space below sccoring before a new game commences scoring
    footer = ['-']
    update_scoresheet(footer, 'Scores')
    footer = ['-']
    update_scoresheet(footer, 'Scores')
    # Ask the user if they want to repeat the program
    repeat = input('Do you want to score another game? (yes/no): \n').strip().lower()
    if repeat == 'yes':
        main()
    else:    
        print("Exiting the program. Goodbye!")
       

    
main()
