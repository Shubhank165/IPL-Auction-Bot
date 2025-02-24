import pandas as pd
from auctionengine.dealer import Dealer
from auctionengine.team import Team
from auctionengine.utils import load_players
from strategies.advanced import AdvancedBiddingStrategy
from strategies.statistical import StatisticalBiddingStrategy
from strategies.optimized import OptimizedBiddingStrategy
from strategies.optimized2 import OptimizedBiddingStrategy2
from strategies.optimized3 import OptimizedBiddingStrategy3
from strategies.optimized4 import OptimizedBiddingStrategy4

class Player:
    def __init__(self, name, role, matches, wickets, base_price):
        self.name = name
        self.role = role
        self.matches = matches
        self.wickets = wickets
        self.base_price = base_price
        self.stats = {"stars": 0}  # Example for stats, you can extend it

def calculate_total_stars(team):
    return sum(player.stats.get("stars", 0) for player in team.players)

def load_players(file_path, role=""):
    """
    Loads players data from a CSV file and processes missing or NaN values.
    """
    df = pd.read_csv(file_path)
    
    players = []
    
    for _, row in df.iterrows():
        # Handle NaN in "Wkts" and other fields by setting them to 0
        wickets = row.get("Wkts", 0)
        if pd.isna(wickets):
            wickets = 0  # Default value if NaN
        
        # Handle NaN in "Matches" and other fields by setting them to 0
        matches = row.get("Matches", 0)
        if pd.isna(matches):
            matches = 0  # Default value if NaN
        
        base_price = row.get("BasePrice", 0)  # Assuming "BasePrice" is in the CSV

        # Create a Player object instead of a dictionary
        player = Player(
            name=row.get("Player", ""),
            role=role,
            matches=int(matches),  # Safely convert to int
            wickets=int(wickets),  # Safely convert to int
            base_price=float(base_price)  # Safely convert to float for price
        )
        
        players.append(player)
    
    return players

def main(): 
    """
    Main function that orchestrates the auction process.
    Loads player data, initializes teams, and runs the auction.
    """
    # Load data for all categories of players from CSV files
    batsmen = load_players("dataset/batsmen.csv", role="batsman")
    bowlers = load_players("dataset/bowlers.csv", role="bowler")
    allrounders = load_players("dataset/allrounders.csv", role="allrounder")
    wicket_keepers = load_players("dataset/wicketkeepers.csv", role="wicketkeeper")

    # Combine all player categories into one list for auction
    all_players = batsmen + bowlers + allrounders + wicket_keepers

    # Initialize team budgets (in millions)
    team_budgets = {
        "Team A": 60.0,
        "Team B": 60.0,
        "Team C": 60.0,
        "Team D": 60.0,
        "Team E": 60.0,
        "Team F": 60.0,
    }

    # Set maximum players allowed per team
    max_players = 15

    # Create team objects with their respective budgets and player limits
    team_a = Team(name="Team A", budget=team_budgets["Team A"], max_players=max_players)
    team_b = Team(name="Team B", budget=team_budgets["Team B"], max_players=max_players)
    team_c = Team(name="Team C", budget=team_budgets["Team C"], max_players=max_players)
    team_d = Team(name="Team D", budget=team_budgets["Team D"], max_players=max_players)
    team_e = Team(name="Team E", budget=team_budgets["Team E"], max_players=max_players)
    team_f = Team(name="Team F", budget=team_budgets["Team F"], max_players=max_players)
    
    teams = [team_a, team_b, team_c, team_d, team_e, team_f]

    # Assign bidding strategies to teams
    bidding_strategies = {
        "Team A": OptimizedBiddingStrategy2(total_budget=team_a.budget),
        "Team B": OptimizedBiddingStrategy4(total_budget=team_b.budget),
        "Team C": OptimizedBiddingStrategy2(total_budget=team_c.budget),
        "Team D": OptimizedBiddingStrategy4(total_budget=team_d.budget),
        "Team E": OptimizedBiddingStrategy2(total_budget=team_e.budget),
        "Team F": OptimizedBiddingStrategy4(total_budget=team_f.budget),
    }

    # Initialize dealer with players, teams, and their strategies
    dealer = Dealer(players=all_players, teams=teams, strategies=bidding_strategies)

    # Execute the auction process
    dealer.start_auction()

    # Display final team compositions and statistics
    for t in teams:
        t.print_team_summary()
        total_stars = calculate_total_stars(t)
        print(f"Total Stars: {total_stars}")
        print("---------------------------\n")

if __name__ == "__main__":
    main()
