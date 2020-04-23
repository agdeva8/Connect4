from flask import Flask, render_template, request, jsonify
import sys
import json
from policies import RandomPolicy
from policies import MiniMaxRaw
from policies import MiniMaxABPruning
from policies import MiniMaxDQN
from backendFunctions import GameEnv
import numpy as np
import time
app = Flask(__name__)


@app.route('/')
def index():
    # sys.stderr.write("Hello")
    # print('Hello world!', file=sys.stderr)
    return render_template('index.html')


@app.route('/AIResponse', methods=["POST"])
def AIResponse():
    stateStr = request.get_data().decode("utf-8")
    # sys.stderr.write('\n\n')
    # sys.stderr.write(stateStr)
    # sys.stderr.write('\n\n')
    state = json.loads(stateStr)

    game = GameEnv()
    # AIPolicy = RandomPolicy(game)
    # AIPolicy = MiniMaxRaw(game)
    # AIPolicy = MiniMaxABPruning(game)
    AIPolicy = MiniMaxDQN(game)

    # nRows, nCols = np.shape(state["board"])
    # state["nRows"] = nRows
    # state["nCols"] = nCols
    # startTime = time.time()
    sys.stderr.write("Geitting action policy")
    action = AIPolicy.getAction(state)
    # sys.stderr.write("time is ")
    # sys.stderr.write(str(time.time() - startTime))
    # sys.stderr.write('\n')
    # action = AIPolicy.getAction((state["player"], state["board"]))

    # sys.stderr.write(str(action))

    return jsonify(
        success=True,
        action=int(action)
    )
