import db


total_games = db.get_urls_with_info_count()
with_tokens = db.get_games_with_tokens_count()
print("TOTAL GAMES: 1947")
print("TOTAL GAMES WITH INFO ", total_games)
print("TOTAL GAMES WITH TOKENS ", with_tokens)