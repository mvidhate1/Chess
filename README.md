# PyChess
A simple AI agent for Chess in python. 

## Prerequisites

For a smooth and hassle free experience, make sure you are working with conda
```
python=3.7.6
``` 

If not, you can follow the installation steps on https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html pertaining to your system.
Once you have conda installed, you can get python3.7.6 by using the command
```
conda install python=3.7.6
```

## Rules

The rules of play can be found on https://www.fide.com/FIDE/handbook/LawsOfChess.pdf

Only the basic rules of play have been adopted and not the competition rules.

## Controls

The chess pieces can be selected using the mouse pointer and then the grid to which you want to move the piece to should be selected.

If the move is deemed legal according to the Basic Rules of Play mentioned in the rulebook provided above, the chess piece will be shifted, else the move will not take place.

## Run

```
cd PyChess
chmod u+x run.sh
./run.sh
```
