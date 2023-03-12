from flask import Flask, render_template, url_for, redirect, abort, request, jsonify
import os
import db

app = Flask(__name__)

def transorm_game_info(game_info: dict):
    new_info = {}
    new_info['TITLE']= f"Hot NFT Games | {game_info['NAME']}"
    new_info['FOCUS_KEYPHRASE'] = 'NFT Games'
    new_info['SEO_TITLE'] = f"{game_info['NAME']} | Hot NFT Games | metaverse Job Japan"
    new_info['SLUG'] = f"Hot NFT Games | {game_info['NAME']}"
    formatted_genres = ', '.join(game_info['GENRES'].split(','))
    new_info['GENRES'] = formatted_genres
    new_info['META_DESCRIPTION'] = f"Explore exciting new NFT Games with mJJ! Checkout {game_info['NAME']}, a {formatted_genres} game. Learn more and start playing!!"
    formatted_tokens = 'N/A' if game_info['TOKENS'] is None else ', '.join(game_info['TOKENS'].split(','))
    new_info['TOKENS'] = formatted_tokens
    new_info['GAME_SNAPSHOT'] = game_info['DESCRIPTION'] + f" {game_info['NAME']} is an NFT game which has play-to-earn feature. Let's play {game_info['NAME']} and you can check their {formatted_tokens} Token and NFT price on their official website"
    new_info['BLOCKCHAIN'] = 'Binance Smart Chain'
    formatted_devices = ', '.join(game_info['DEVICES'].split(','))
    new_info['DEVICES'] = formatted_devices
    free_to_play = True
    if game_info['FREE_TO_PLAY'] is None or game_info['FREE_TO_PLAY'].lower() != 'yes':
        free_to_play = False
    new_info['FREE_TO_PLAY'] = free_to_play
    
    nft_support = True
    if game_info['NFT_SUPPORT'] is None or game_info['NFT_SUPPORT'].lower() != 'yes':
        nft_support = False
    new_info['NFT_SUPPORT'] = nft_support

    current_id = int(game_info['ID'])
    new_info['NEXT_ID'] = None
    new_info['PREV_ID'] = None
    if current_id > 1:
        new_info['PREV_ID'] = current_id - 1
    if current_id < 1947:
        new_info['NEXT_ID'] = current_id + 1
    new_info['IMAGES'] = []
    new_info['IMAGES_PATH'] = None
    images_path = os.path.join('static', 'images', str(game_info['ID']))
    if os.path.exists(images_path):
        new_info['IMAGES'] = [os.path.join('/',images_path, i).replace('\\', '/') for i in os.listdir(images_path)]
        new_info['IMAGES_PATH'] = os.path.join(os.getcwd(), images_path)

    return new_info
@app.route("/", methods=["GET"])
def index():
    redirect_url = None
    if not os.path.exists('last.txt'):
        redirect_url = url_for('game', game_id='1')
    else:
        with open('last.txt', 'r') as f:
            game_id = f.read().strip()
            redirect_url = url_for('game', game_id=game_id)
    return redirect(redirect_url)

@app.route("/<int:game_id>", methods=["GET", "POST"])
def game(game_id):
    game_info = db.get_game_by_id(game_id)
    if game_info is None:
        abort(404)
    transormed_info = transorm_game_info(game_info)
    with open('last.txt', 'w') as f:
        f.write(str(game_info['ID']))
    return render_template("index.html", transformed_info=transormed_info, game_info=game_info)

@app.route("/openfolder", methods=["POST"])
def open_path():
    folder = request.json['folderPath']
    command = f'explorer {folder}'
    print(command)
    os.system(f'explorer {folder}')
    response = jsonify({ 'status_code': 200 })
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run()