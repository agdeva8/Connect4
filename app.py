from flask import Flask, render_template, request, jsonify
import sys
import json
from policies import RandomPolicy
from backendFunctions import GameEnv
app = Flask(__name__)


@app.route('/')
def index():
    # sys.stderr.write("Hello")
    # print('Hello world!', file=sys.stderr)
    return render_template('index.html')


@app.route('/AIResponse', methods=["POST"])
def AIResponse():
    stateStr = str(request.get_data())
    state = json.loads(stateStr)

    game = GameEnv()
    AIPolicy = RandomPolicy(game)
    action = AIPolicy.getAction((state["board"], state["player"]))

    # sys.stderr.write(str(action))
 
    return jsonify(
        success=True,
        action=action,
        player=state["nCols"]
    )