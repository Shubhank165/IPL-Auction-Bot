"""
This module implements the main auction functionality for a cricket team auction system.
It loads player data, sets up teams with budgets, and runs the auction process using
different bidding strategies for each team.

The auction system supports different types of players (batsmen, bowlers, all-rounders,
and wicket-keepers) and allows teams to bid based on either basic or statistical strategies.
"""

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
def main(): 
    """
    Main function that orchestrates the auction process.
    Loads player data, initializes teams, and runs the auction.
    """
    # Load data for all categories of players from CSV files
    #batsmen = load_players("C:\Users\LENOVO\.vscode\python\auction bot\dataset\batsmen.csv", role="batsman")
    #bowlers = load_players(r"C:\Users\LENOVO\.vscode\python\auction bot\dataset\bowlers.csv", role="bowler")
    #allrounders = load_players(r"C:\Users\LENOVO\.vscode\python\auction bot\dataset\allrounders.csv", role="allrounder")
    #wicket_keepers = load_players(r"C:\Users\LENOVO\.vscode\python\auction bot\dataset\wicketkeepers.csv", role="wicketkeeper")
    
    batsmen = load_players("dataset/batsmen.csv", role="batsman")
    bowlers = load_players("dataset/bowlers.csv", role="bowler")
    allrounders = load_players("dataset/allrounders.csv", role="allrounder")
    wicket_keepers = load_players("dataset/wicketkeepers.csv", role="wicketkeeper")

    # Combine all player categories into one list for auction
    all_players = batsmen  +bowlers+ allrounders + wicket_keepers

    # Initialize team budgets (in millions)
    team_budgets = {
        "Team A": 60.0,
        "Team B": 60.0,
        "Team C": 60.0,
        "Team D": 60.0
    }

    # Set maximum players allowed per team
    max_players = 15

    # Create team objects with their respective budgets and player limits
    team_a = Team(name="Team A", budget=team_budgets["Team A"], max_players=max_players)
    team_b = Team(name="Team B", budget=team_budgets["Team B"], max_players=max_players)
    team_c = Team(name="Team C", budget=team_budgets["Team C"], max_players=max_players)
    team_d = Team(name="Team D", budget=team_budgets["Team D"], max_players=max_players)
    teams = [team_a, team_b, team_c, team_d]

    # Assign bidding strategies to teams
    bidding_strategies = {
        "Team A": OptimizedBiddingStrategy(total_budget=team_a.budget),
        "Team B": OptimizedBiddingStrategy2(total_budget=team_b.budget),
        "Team C": OptimizedBiddingStrategy3(total_budget=team_c.budget),
        "Team D": OptimizedBiddingStrategy4(total_budget=team_d.budget)
    }
    
    # Initialize dealer with players, teams and their strategies
    dealer = Dealer(players=all_players, teams=teams, strategies=bidding_strategies)

    # Execute the auction process
    dealer.start_auction()

    # Display final team compositions and statistics
    for t in teams:
        t.print_team_summary()

if __name__ == "__main__":
    main()
