import random

class OptimizedBiddingStrategy:
    """
    An advanced bidding strategy that maximizes total star ratings 
    while maintaining team balance and budget constraints.
    """

    # Minimum role requirements
    ROLE_REQUIREMENTS = {"batsman": 3, "bowler": 3, "wicketkeeper": 1}
    MAX_FOREIGN_PLAYERS = 4

    def __init__(self, total_budget):
        """
        Initializes the strategy with budget and constraints.
        
        Args:
            total_budget (float): Total budget available for the team.
        """
        self.total_budget = total_budget
        self.remaining_budget = total_budget
        self.team = {"batsman": 0, "bowler": 0, "allrounder": 0, "wicketkeeper": 0, "foreign_players": 0}
        self.players_acquired = []

    def is_valid_bid(self, player, current_bid):
        """
        Checks if bidding for a player maintains balance and budget.

        Args:
            player: Player object containing role and nationality.
            current_bid (float): Current highest bid in the auction.

        Returns:
            bool: Whether bidding is allowed.
        """
        if current_bid > self.remaining_budget:
            return False

        if player.nationality != "I" and self.team["foreign_players"] >= self.MAX_FOREIGN_PLAYERS:
            return False

        return True

    def estimate_value(self, player):
        """
        Predicts a player's value based on stars, performance, and base price.

        Args:
            player: Player o bject containing stats.

        Returns:
            float: Estimated fair price for the player.
        """
        base = player.base_price
        stars = player.stats.get("stars", 5)
        star_factor = (stars - 5) * 0.4  
        estimated_value = base + star_factor

        if stars >= 8:
            estimated_value *= 1.2  

        return max(estimated_value, base)

    def decide_bid(self, player, current_bid):
        """
        Determines if the bot should bid and how much.

        Args:
            player: Player object.
            current_bid (float): Current highest bid.

        Returns:
            float: New bid amount if bidding, otherwise returns current bid.
        """
        if not self.is_valid_bid(player, current_bid):
            return current_bid  

        estimated_value = self.estimate_value(player)
        role_needed = self.team[player.role] < self.ROLE_REQUIREMENTS.get(player.role, 0)

        if role_needed and current_bid < 0.95 * estimated_value:
            return round(current_bid + 0.6, 2)  

        if player.stats.get("stars", 5) >= 8 and current_bid < estimated_value:
            return round(current_bid + 0.4, 2)

        if current_bid < estimated_value and random.random() < 0.4:
            return round(current_bid + 0.2, 2)  

        return current_bid

    def update_team(self, player, winning_bid):
        """
        Updates team composition after winning a bid.

        Args:
            player: Player object.
            winning_bid (float): Final bid amount for the player.
        """
        self.players_acquired.append(player)
        self.remaining_budget -= winning_bid
        self.team[player.role] += 1
        if player.nationality != "I":
            self.team["foreign_players"] += 1


def bidding_bot(player, purse_money_left, current_bid):
    """
    Function to decide whether to bid on a player.

    Args:
        player: Player object containing name, role, nationality, stats, and base price.
        purse_money_left (float): Amount of purse money left for bidding.
        current_bid (float): The current highest bid.

    Returns:
        tuple: (boolean indicating whether to bid, next bid amount if bidding)
    """
    strategy = OptimizedBiddingStrategy(purse_money_left)
    next_bid = strategy.decide_bid(player, current_bid)
    should_bid = next_bid > current_bid and next_bid <= purse_money_left
    return should_bid, next_bid if should_bid else current_bid