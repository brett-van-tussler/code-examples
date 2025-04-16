import random
from itertools import combinations
from collections import Counter

def generate_schedule(num_teams):
    if num_teams != 9:
        raise ValueError("This scheduler is designed specifically for 9 teams")
    
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
    max_attempts = 10000  # Increase maximum attempts
    attempt = 0
    rotation_index = 0
    
    while remaining_matchups and attempt < max_attempts:
        attempt += 1
        # Instead of shuffling, rotate the list by moving first element to the end
        if rotation_index > 0:
            remaining_matchups = remaining_matchups[rotation_index:] + remaining_matchups[:rotation_index]
        rotation_index = 1  # Move by one position in subsequent iterations
        week_games = [[] for _ in range(4)]  # 4 time slots per week
        teams_per_week = Counter()
        used_teams_per_time = set()
        teams_this_week = set()
        
        # Fill time slots with games
        for time_slot in range(4):
            used_teams_per_time.clear()
            used_teams_per_time.update(team for game in week_games[time_slot] for team in game)
            for game in remaining_matchups[:]:
                team1, team2 = game
                if (team1 not in used_teams_per_time and 
                    team2 not in used_teams_per_time and 
                    teams_per_week[team1] < 2 and 
                    teams_per_week[team2] < 2):
                    week_games[time_slot].append(game)
                    used_teams_per_time.add(team1)
                    used_teams_per_time.add(team2)
                    teams_per_week[team1] += 1
                    teams_per_week[team2] += 1
                    remaining_matchups.remove(game)
                    if len(week_games[time_slot]) == 2:
                        break
        
        # If we found enough valid games (at least 6 games), add to schedule
        total_games = sum(len(games) for games in week_games)
        if total_games >= 6:  # Accept weeks with at least 6 games to ensure better distribution
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
    games_per_week = Counter()
    
    # Count all matchups in the schedule
    for week_games in schedule:
        week_teams = Counter()
        for time_slot_games in week_games:
            for team1, team2 in time_slot_games:
                # Sort teams to ensure consistent counting regardless of order
                matchup = tuple(sorted([team1, team2]))
                matchup_counts[matchup] += 1
                week_teams[team1] += 1
                week_teams[team2] += 1
        
        # Track number of games per team per week
        for team, count in week_teams.items():
            games_per_week[count] += 1
    
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
    
    # Print distribution of games per week
    total_team_weeks = sum(games_per_week.values())
    print("\nGames per week distribution:")
    for num_games in sorted(games_per_week.keys()):
        percentage = (games_per_week[num_games] / total_team_weeks) * 100
        print(f"Teams playing {num_games} game(s): {percentage:.1f}%")
    
    return all_valid, errors

def main():
    # Test for 9 teams
    num_teams = 9
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