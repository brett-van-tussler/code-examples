import random
from itertools import combinations
from collections import Counter

def generate_schedule(num_teams):
    if num_teams != 8:
        raise ValueError("This scheduler is designed specifically for 8 teams")
    
    # Create list of teams
    teams = [f"Team {i+1}" for i in range(num_teams)]
    
    # Initialize schedule
    schedule = []
    
    # Create all possible matchups
    all_matchups = list(combinations(teams, 2))
    # Each team needs to play each other team twice
    all_matchups = all_matchups * 2
    
    # Track remaining matchups
    remaining_matchups = all_matchups.copy()
    max_attempts = 1000  # Prevent infinite loops
    attempt = 0
    
    while remaining_matchups and attempt < max_attempts:
        attempt += 1
        random.shuffle(remaining_matchups)  # Shuffle before each attempt
        week_games = [[] for _ in range(4)]  # 4 time slots per week
        teams_per_week = Counter()
        used_teams_per_time = set()
        teams_in_first_slot = set()  # Track teams playing in first time slot
        
        # Try to fill each time slot with 2 games
        for time_slot in range(4):
            used_teams_per_time.clear()
            # Try to find 2 games where no team plays twice in this time slot
            for game in remaining_matchups[:]:
                team1, team2 = game
                # For the last time slot, check if teams played in first slot
                if time_slot == 3 and (team1 in teams_in_first_slot or team2 in teams_in_first_slot):
                    continue
                # Check if neither team is already playing in this time slot
                # and neither team has played twice this week
                if (team1 not in used_teams_per_time and 
                    team2 not in used_teams_per_time and 
                    teams_per_week[team1] < 2 and 
                    teams_per_week[team2] < 2):
                    week_games[time_slot].append(game)
                    used_teams_per_time.add(team1)
                    used_teams_per_time.add(team2)
                    teams_per_week[team1] += 1
                    teams_per_week[team2] += 1
                    # Track teams playing in first time slot
                    if time_slot == 0:
                        teams_in_first_slot.add(team1)
                        teams_in_first_slot.add(team2)
                    remaining_matchups.remove(game)
                    if len(week_games[time_slot]) == 2:
                        break
        
        # If we found 8 valid games (2 per time slot), add them to the schedule
        total_games = sum(len(games) for games in week_games)
        if total_games == 8:
            schedule.append(week_games)
        else:
            # Put any removed games back and try again
            for time_slot_games in week_games:
                remaining_matchups.extend(time_slot_games)
    
    if attempt >= max_attempts:
        raise RuntimeError("Could not generate a valid schedule after maximum attempts")
    
    return schedule

def print_schedule(schedule):
    print("\nSeason Schedule:")
    print("-" * 40)
    for week_num, week_games in enumerate(schedule, 1):
        print(f"\nWeek {week_num}:")
        for time_slot, time_games in enumerate(week_games, 1):
            print(f"\nTime Slot {time_slot}:")
            for game_num, (team1, team2) in enumerate(time_games, 1):
                print(f"Game {game_num}: {team1} vs {team2}")
        print("-" * 40)

def validate_schedule(schedule, num_teams):
    # Create a Counter to track games between each pair of teams
    matchup_counts = Counter()
    
    # Count all matchups in the schedule
    for week in schedule:
        for time_slot_games in week:
            for team1, team2 in time_slot_games:
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
    # Test for 8 teams
    num_teams = 8
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
