from datetime import datetime

class GameAnalyzer:
    def __init__(self):
        pass

    def sort_games(self, games, sort_by="last_updated", reverse=False):
        """
        Sorts the list of games based on the criteria.
        
        Args:
            games (list): List of game dictionaries.
            sort_by (str): 'last_updated' or 'size'.
            reverse (bool): True for descending (Newest/Largest first), False for ascending (Oldest/Smallest first).
                            Default recommendation for cleaning is Oldest first (False) for Date, Largest first (True) for Size.
        """
        if sort_by == "last_updated":
            # Sort by timestamp (Oldest first by default)
            return sorted(games, key=lambda x: x['last_updated_timestamp'], reverse=reverse)
        elif sort_by == "size":
            # Sort by size (Smallest first by default, usually we want Largest first to clean space)
            return sorted(games, key=lambda x: x['size_gb'], reverse=reverse)
        return games

    def rank_games(self, games):
        """
        Adds a 'priority_score' or determines removal candidates.
        For now, just returns sorted list by 'last_updated' (Oldest first).
        """
        return self.sort_games(games, sort_by="last_updated", reverse=False)

if __name__ == "__main__":
    # Mock data for testing
    mock_games = [
        {"name": "Game A", "size_gb": 10, "last_updated_timestamp": 1600000000}, # Older
        {"name": "Game B", "size_gb": 50, "last_updated_timestamp": 1700000000}, # Newer
    ]
    analyzer = GameAnalyzer()
    sorted_games = analyzer.rank_games(mock_games)
    for g in sorted_games:
        print(f"{g['name']} - {g['last_updated_timestamp']}")
