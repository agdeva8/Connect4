from flask import Flask, render_template, request, jsonify
import sys
import json
from policies import RandomPolicy
from backendFunctions import GameEnv
import numpy as np
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

    nRows, nCols = np.shape(state["board"])
    state["nRows"] = nRows
    state["nCols"] = nCols
    action = AIPolicy.getAction(state)
    # action = AIPolicy.getAction((state["player"], state["board"]))

    # sys.stderr.write(str(action))
 
    return jsonify(
        success=True,
        action=action,
        player=state["nCols"]
    )
