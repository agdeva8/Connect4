let canvas : any = document.getElementById("myCanvas");
let ctx = canvas.getContext("2d");

let nRows: number = 4;
let nCols: number= 4;

let startGrid_x: number= 100;
let startGrid_y: number= 100;
let cell_width: number = 120;
let cell_height: number = 120;

let currMouse_x: number;
let currMouse_y: number;
let humanPolicy: boolean;
let aiPolicy: boolean;
let bgColor: string = "grey";
let diskRadius: number = cell_width / 2 - 0.15 * cell_width;

let d_isCheckMate: boolean = false;
let nConnect: number = 3;

let diskColor = {
    "1": "yellow",
    "-1": "red",
};

ctx.fillStyle = bgColor;
ctx.fillRect(0, 0, canvas.width, canvas.height);

class State {
    nRows; nCols; player: number;
    board: number[][];

    constructor() {
        this.board = new Array(nRows);

        for (let i = 0; i < this.board.length; i++) {
            this.board[i] = new Array(nCols);
        }

        for (let i = 0; i < nRows; i++) {
            for (let j = 0; j < nCols; j++) {
                this.board[i][j] = 0;
            }
        }

        this.nRows = nRows;
        this.nCols = nCols;

        this.player = 1;
    }
}

let currState: State = new State();

function RCFromXY(x, y) {
    let col: number = Math.floor((x - startGrid_x) / cell_width);
    let row: number  = Math.floor((y - startGrid_y) / cell_height);

    return [row, col];
}

function XYFromRC(row, col) {
    let x: number = startGrid_x + col * cell_width;
    let y: number = startGrid_y + row * cell_height;
    return [x, y];
}

function centerFromRC(row, col) {
    let x, y: number;
    [x, y] = XYFromRC(row, col);
    x += cell_width / 2;
    y += cell_height / 2;
    return [x, y];
}

function isValidRC(row, col) {
    return row >= 0 && row < nRows && col >= 0 && col < nCols;
}

function createCell(row, col) {
    let x, y: number;
    [x, y] = XYFromRC(row, col);
    ctx.beginPath();
    ctx.lineWidth = "2";
    ctx.strokeStyle = "black";
    ctx.rect(x, y, cell_width, cell_height);
    ctx.stroke();
    ctx.fillStyle = "blue";
    ctx.fill();
    ctx.closePath();
}

function createDiskFromXY(x, y, color) {
    ctx.beginPath();
    ctx.lineWidth = "2";
    ctx.strokeStyle = "black";
    ctx.arc(x, y, diskRadius, 0, Math.PI * 2);
    // ctx.stroke()
    ctx.fillStyle = color;
    ctx.fill();
    ctx.closePath();
}

function createDisk(row, col, color) {
    const [x, y] = centerFromRC(row, col);
    createDiskFromXY(x, y, color);
}

function emptyDisk(row, col) {
    createDisk(row, col, bgColor);
}

function fillDisk(row, col, state) {
    let color: string = diskColor[state.player];
    createDisk(row, col, color);
}

function createGrid() {
    for (let row = 0; row < nRows; row++) {
        for (let col = 0; col < nCols; col++) {
            createCell(row, col);
            emptyDisk(row, col);
        }
    }
}

createGrid();

// Mouse Move Handler
document.addEventListener("mousemove", mouseMoveHandler, false);

function mouseMoveHandler(e) {
    let relativeX: number = e.clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        currMouse_x = relativeX;
    }

    let relativeY: number = e.clientY - canvas.offsetTop;
    if (relativeY > 0 && relativeY < canvas.height) {
        currMouse_y = relativeY;
    }
}

document.addEventListener("click", mouseClickHandler, false);

function mouseClickHandler(e) {
    if (!humanPolicy) return;

    let x: number = e.clientX - canvas.offsetLeft;
    let y: number = e.clientY - canvas.offsetTop;
    if (x > 0 && x < canvas.width && y > 0 && y < canvas.height) {
        let row, col: number;
        [row, col] = RCFromXY(x, y);

        if (performAction(col, currState)) humanPolicy = false;
    }
}

function statusBarUpdate(col, state) {
    let x, y: number;

    x = startGrid_x;
    y = startGrid_y - 40;
    let width: number = cell_width * nCols;
    let height: number = 25;

    ctx.clearRect(x, y, width, height);
    ctx.fillStyle = bgColor;
    ctx.fillRect(x, y, width, height);

    if (!isValidRC(0, col)) {
        return;
    }

    // ctx.beginPath();
    // ctx.lineWidth = "2";
    // ctx.strokeStyle = "black";
    // ctx.rect(x, y, width, height);
    // ctx.stroke();
    // ctx.closePath();

    [x, y] = centerFromRC(0, col);
    y = startGrid_y - 25;
    // // the triangle
    ctx.beginPath();
    ctx.moveTo(x - 4, y - 5);
    ctx.lineTo(x, y);
    ctx.lineTo(x + 4, y - 5);
    ctx.closePath();

    ctx.lineWidth = 10;
    ctx.strokeStyle = diskColor[state.player];
    ctx.stroke();

    ctx.fillStyle = diskColor[state.player];
    ctx.fill();
}

function showCheckMatePattern(r, c, i, j, nConnect) {
    let x, y: number;
    for (let itr: number = 0; itr < nConnect; itr++) {
        [x, y] = centerFromRC(r + i * itr, c + j * itr);
        ctx.beginPath();
        ctx.arc(x, y, 0.1 * diskRadius, 0, Math.PI * 2);
        ctx.fillStyle = "black";
        ctx.fill();
        ctx.closePath();
    }

    let x0, y0: number;
    [x0, y0] = centerFromRC(r, c);

    ctx.beginPath();
    ctx.moveTo(x0, y0);
    ctx.lineTo(x, y);
    ctx.strokeStyle = "black";
    ctx.stroke();
}

function isCheckMate(state) {

    let ijPattern: number[][] = [
        [1, 0],
        [0, 1],
        [1, 1],
        [1, -1],
    ];
    let count: number = 0;

    for (let i = 0; i < 4; i++) {
        for (let row = 0; row < state.nRows; row++) {
            for (let col = 0; col < state.nCols; col++) {
                if (state.board[row][col] == 0) continue;
                count = 0;

                for (let j = 0; j < nConnect; j++) {
                    let cRow = row + ijPattern[i][0] * j;
                    let cCol = col + ijPattern[i][1] * j;
                    if (!isValidRC(cRow, cCol)) continue;

                    if (state.board[row][col] == state.board[cRow][cCol]) count++;
                }
                // console.log("count is " + count)
                if (count == nConnect) {
                    showCheckMatePattern(
                        row,
                        col,
                        ijPattern[i][0],
                        ijPattern[i][1],
                        nConnect
                    );
                    return true;
                }
            }
        }
    }
    return false;
}

function performAction(col, state) {
    // console.log("perform action")
    if (!isValidRC(0, col)) return false;

    let row:number = state.nRows - 1;

    while (row >= 0) {
        if (state.board[row][col] == 0) break;
        row--;
    }

    // console.log("row, col is " + row + " " + col)
    if (row < 0) return false;

    // console.log("update board")
    // fillDisk(row, col, state);
    //   state.board[row][col] = state.player;
    // state.player *= -1;

    fillDisk(row, col, currState);
    currState.board[row][col] = currState.player;
    currState.player *= -1;
    return true;
}

function showCurrPlayer(text, state) {
    let x, y: number;

    [x, y] = centerFromRC(state.nRows - 1, state.nCols - 1);
    y += cell_height + 20;

    let width: number = cell_width * 4;
    let height: number = cell_height;

    let startX: number = x - 3 * cell_width;
    let startY: number = y - 55;

    ctx.beginPath()
    ctx.clearRect(startX, startY, width, height);
    ctx.fillStyle = bgColor;
    ctx.fillRect(startX, startY, width, height);
    ctx.closePath()

    ctx.font = "50px Georgia";
    ctx.fillStyle = "green";
    ctx.textAlign = "right";
    ctx.fillText(text, x - diskRadius - 40, y + 20);
    createDiskFromXY(x, y, diskColor[state.player]);
}

function getAIResponse(state) {

    if (!aiPolicy)
        return

    // console.log("getting ai response")

    const request = new XMLHttpRequest();
    // const player = state.player;

    // console.log("opened request");
    request.open("POST", "/AIResponse");

    let action: number = -1
    request.onload = () => {
        // console.log("loaded AIResponse");
        const data = JSON.parse(request.responseText);

        // console.log(data);
        if (data.success) {
            // console.log(" Is a success");
            // console.log(data.player);
            // console.log(data.action)
            action = data.action
            // AIAction = data.action
            // console.log(action)
            if (performAction(action, currState))
                aiPolicy = false
        }
        // } else {
        //   // console.log("Not a success");
        // }
        // return action
    };

    let jsonString: string = JSON.stringify(state)
    request.send(jsonString);

    // const data = new FormData();
    // data.append('player', state.player)
    // data.append('board', state.board)

    // request.send(data)
}

humanPolicy = false;
aiPolicy = false;

function draw() {
    let currRow, currCol: number;
    [currRow, currCol] = RCFromXY(currMouse_x, currMouse_y);

    if (isValidRC(currRow, currCol)) {
        statusBarUpdate(currCol, currState);
    }

    if (d_isCheckMate)
        return;

    showCurrPlayer("PLAYER", currState);

    if (!humanPolicy && !aiPolicy) {
        if (currState.player == 1) {
            // console.log("p1 chance ")
            humanPolicy = true
        }
        else if (currState.player == -1) {
            // console.log("p2 chance")
            aiPolicy = true
            getAIResponse(currState)
        }

            // else 
            // console.log("There is some error in currState.player")

            // console.log('\n\n\n\n')
            if (isCheckMate(currState)) {
                // console.log("celebrating checkmate")
                currState.player *= -1
                d_isCheckMate = true;
                showCurrPlayer("WINNER", currState);
                humanPolicy = false
                aiPolicy = false
            }
    }
}
setInterval(draw, 10);
