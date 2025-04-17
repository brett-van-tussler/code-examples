```python
import random
from itertools import combinations
from collections import Counter

num_teams = 9
# Create list of teams
teams = [f"Team {i+1}" for i in range(num_teams)]

# Generate all possible matchups
all_matchups = list(combinations(teams, 2))
# Double the matchups since each team plays each other twice
all_matchups = all_matchups * 2
random.shuffle(all_matchups)
```


```python
all_matchups
```




    [('Team 4', 'Team 6'),
     ('Team 3', 'Team 4'),
     ('Team 3', 'Team 9'),
     ('Team 1', 'Team 2'),
     ('Team 6', 'Team 8'),
     ('Team 7', 'Team 8'),
     ('Team 6', 'Team 7'),
     ('Team 1', 'Team 2'),
     ('Team 4', 'Team 6'),
     ('Team 2', 'Team 5'),
     ('Team 1', 'Team 3'),
     ('Team 5', 'Team 7'),
     ('Team 5', 'Team 8'),
     ('Team 1', 'Team 4'),
     ('Team 1', 'Team 8'),
     ('Team 1', 'Team 5'),
     ('Team 2', 'Team 8'),
     ('Team 5', 'Team 6'),
     ('Team 2', 'Team 7'),
     ('Team 5', 'Team 8'),
     ('Team 1', 'Team 3'),
     ('Team 3', 'Team 6'),
     ('Team 3', 'Team 7'),
     ('Team 1', 'Team 6'),
     ('Team 4', 'Team 7'),
     ('Team 1', 'Team 7'),
     ('Team 4', 'Team 5'),
     ('Team 3', 'Team 9'),
     ('Team 4', 'Team 5'),
     ('Team 2', 'Team 3'),
     ('Team 3', 'Team 4'),
     ('Team 7', 'Team 9'),
     ('Team 1', 'Team 6'),
     ('Team 3', 'Team 5'),
     ('Team 3', 'Team 8'),
     ('Team 1', 'Team 4'),
     ('Team 4', 'Team 9'),
     ('Team 2', 'Team 6'),
     ('Team 2', 'Team 9'),
     ('Team 1', 'Team 8'),
     ('Team 1', 'Team 5'),
     ('Team 5', 'Team 9'),
     ('Team 1', 'Team 7'),
     ('Team 4', 'Team 7'),
     ('Team 2', 'Team 7'),
     ('Team 3', 'Team 7'),
     ('Team 7', 'Team 9'),
     ('Team 1', 'Team 9'),
     ('Team 3', 'Team 5'),
     ('Team 5', 'Team 9'),
     ('Team 6', 'Team 7'),
     ('Team 2', 'Team 9'),
     ('Team 2', 'Team 4'),
     ('Team 7', 'Team 8'),
     ('Team 6', 'Team 8'),
     ('Team 3', 'Team 6'),
     ('Team 4', 'Team 9'),
     ('Team 4', 'Team 8'),
     ('Team 5', 'Team 7'),
     ('Team 5', 'Team 6'),
     ('Team 1', 'Team 9'),
     ('Team 8', 'Team 9'),
     ('Team 6', 'Team 9'),
     ('Team 2', 'Team 3'),
     ('Team 2', 'Team 8'),
     ('Team 8', 'Team 9'),
     ('Team 2', 'Team 6'),
     ('Team 2', 'Team 4'),
     ('Team 4', 'Team 8'),
     ('Team 2', 'Team 5'),
     ('Team 6', 'Team 9'),
     ('Team 3', 'Team 8')]




```python
# Calculate max games per week based on number of teams
max_games_per_week = 8 if num_teams >= 8 else 4

# Organize games into weeks with paired games and rest constraints
schedule = []
remaining_matchups = all_matchups.copy()
max_games_per_week
```




    8




```python


if remaining_matchups:
    week_games = []
    used_teams = set()
    
    # Try to create pairs of games where no team plays in both games of a pair
    while len(week_games) < max_games_per_week and remaining_matchups:
        # Find a valid game for the current pair
        valid_game_found = False
        for i, (team1, team2) in enumerate(remaining_matchups):
            # Check if neither team has played in the current pair of games
            if team1 not in used_teams and team2 not in used_teams:
                week_games.append((team1, team2))
                used_teams.add(team1)
                used_teams.add(team2)
                remaining_matchups.pop(i)
                valid_game_found = True
                break
        
        # If we couldn't find a valid game for the current pair, move to next pair
        if not valid_game_found:
            # If we're at an odd number of games and can't find a valid pair,
            # it's okay to have a single game
            if len(week_games) % 2 == 0:
                break
    
    if week_games:
        schedule.append(week_games)
```


```python
def print_schedule(schedule):
    print("\nSeason Schedule:")
    print("-" * 40)
    for week_num, week_games in enumerate(schedule, 1):
        print(f"\nWeek {week_num}:")
        for game_num, (team1, team2) in enumerate(week_games, 1):
            print(f"Game {game_num}: {team1} vs {team2}")
        print("-" * 40)

def validate_schedule(schedule, num_teams):
    # Create a Counter to track games between each pair of teams
    matchup_counts = Counter()
    
    # Count all matchups in the schedule
    for week in schedule:
        for team1, team2 in week:
            # Sort teams to ensure consistent counting regardless of order
            matchup = tuple(sorted([team1, team2]))
            matchup_counts[matchup] += 1
    
    # Check if each team plays every other team exactly twice
    teams = [f"Team {i+1}" for i in range(num_teams)]
    expected_matchups = list(combinations(teams, 2))
    
    all_valid = True
    errors = []
    
    # Verify each possible matchup occurs exactly twice
    for matchup in expected_matchups:
        matchup = tuple(sorted(matchup))
        count = matchup_counts[matchup]
        if count != 2:
            all_valid = False
            errors.append(f"{matchup[0]} vs {matchup[1]}: Played {count} times (should be 2)")
    
    return all_valid, errors

def main():
    # Test for each possible number of teams
    for num_teams in [9]:
        print(f"\nGenerating and validating schedule for {num_teams} teams:")
        schedule = generate_schedule(num_teams)
        print_schedule(schedule)
        
        # Validate the schedule
        valid, errors = validate_schedule(schedule, num_teams)
        print("\nSchedule Validation:")
        if valid:
            print("✓ All teams play each other exactly twice")
        else:
            print("✗ Schedule has errors:")
            for error in errors:
                print(f"  - {error}")
        print("-" * 40)

if __name__ == "__main__":
    main()

```

    
    Generating and validating schedule for 9 teams:



    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    Cell In[7], line 57
         54         print("-" * 40)
         56 if __name__ == "__main__":
    ---> 57     main()


    Cell In[7], line 42, in main()
         40 for num_teams in [9]:
         41     print(f"\nGenerating and validating schedule for {num_teams} teams:")
    ---> 42     schedule = generate_schedule(num_teams)
         43     print_schedule(schedule)
         45     # Validate the schedule


    NameError: name 'generate_schedule' is not defined



```python

```
