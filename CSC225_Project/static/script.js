document.addEventListener('DOMContentLoaded', () => {
    const welcome = document.getElementById('welcome');
    const gameArea = document.getElementById('game-area');
    const startBtn = document.getElementById('start-btn');
    const restartBtn = document.getElementById('restart-btn');
    const continueBtn = document.getElementById('continue-btn');
    const statusDiv = document.getElementById('status');

    let board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ];
    let gameOver = false;
    let humanStars = 0;
    let aiDiamonds = 0;
    let tieCount = 0;

    function renderBoard() {
        const cells = document.querySelectorAll('.cell');
        if (!cells.length) return; // Patch: skip if no cells
        cells.forEach(cell => {
            const row = Number(cell.dataset.row);
            const col = Number(cell.dataset.col);
            cell.textContent = board[row][col];
            cell.classList.remove('x', 'o');
            if (board[row][col] === 'X') cell.classList.add('x');
            if (board[row][col] === 'O') cell.classList.add('o');
            cell.onclick = handleClick;
        });
    }

    function handleClick(e) {
        if (gameOver) return;
        const row = Number(e.target.dataset.row);
        const col = Number(e.target.dataset.col);
        if (board[row][col] !== '') return;
        board[row][col] = 'X';
        renderBoard();

        // Send move to backend for AI response
        fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board, player: 'X' })
        })
        .then(res => res.json())
        .then(data => {
            if (data.ai_move) {
                const [aiRow, aiCol] = data.ai_move;
                board[aiRow][aiCol] = 'O';
                renderBoard();
            }
            if (data.win) {
                gameOver = true;
                statusDiv.textContent = data.winner + ' wins!';
                if (data.winner === 'X') {
                    humanStars++;
                } else {
                    aiDiamonds++;
                }
                renderScoreboard();
            } else if (data.tie) {
                gameOver = true;
                statusDiv.textContent = "It's a tie!";
                tieCount++;
                renderScoreboard();
            }
        });
    }

    function renderScoreboard() {
        let humanTrophy = humanStars >= 5 ? ' <span class="trophy">🏆</span>' : '';
        let aiTrophy = aiDiamonds >= 5 ? ' <span class="trophy">🏆</span>' : '';
        document.getElementById('human-stars').innerHTML = '★'.repeat(humanStars) + humanTrophy;
        document.getElementById('ai-diamonds').innerHTML = '◆'.repeat(aiDiamonds) + aiTrophy;
        document.getElementById('tie-count').textContent = tieCount;
    }

    startBtn.onclick = () => {
        welcome.style.display = 'none';
        gameArea.style.display = 'block';
        renderBoard(); // <-- Only call here, when the board is visible
    };

    continueBtn.onclick = () => {
        board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ];
        gameOver = false;
        statusDiv.textContent = '';
        renderBoard(); // <-- Add this line!
    };

    restartBtn.onclick = () => {
        board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ];
        humanStars = 0;
        aiDiamonds = 0;
        tieCount = 0;
        gameOver = false;
        statusDiv.textContent = '';
        renderBoard();
        renderScoreboard();
    };
});