import db


total_games = db.get_urls_with_info_count()
print("TOTAL GAMES: 1947")
print("TOTAL GAMES WITH INFO ", total_games)