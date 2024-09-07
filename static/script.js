let moveHistory = [];

function drop(event) {
    event.preventDefault();
    const diskSize = event.dataTransfer.getData("text/plain");
    const targetTower = event.currentTarget.id;

    const disk = document.querySelector(`.disk[data-size='${diskSize}']`);
    const startTower = getTowerFromDisk(disk);

    if (isValidMove(startTower, targetTower, diskSize)) {
        event.currentTarget.appendChild(disk);
        towers[targetTower].push(disk);
        towers[startTower] = towers[startTower].filter(d => d.dataset.size !== diskSize);
        moveCount++;
        moveHistory.push(`Move disk ${diskSize} from ${startTower} to ${targetTower}`);
        updateMoveCounter();

        // Check if the game is completed
        if (towers.C.length === parseInt(document.getElementById("numDisks").value)) {
            displayTimeTaken();
            console.log("Moves History: ", moveHistory);
            alert("Game completed successfully! Check console for move history.");
        }

    } else {
        alert("Invalid move! A smaller disk cannot be placed on a larger disk.");
    }

    if (moveCount >= maxMoves) {
        alert("You've reached the maximum number of moves!");
    }
}
