# Astracraft (real name pending)

Submission for itch.io Beginner's Circle Game Jam #3
https://vagranttechnology.itch.io/astracraft

## Getting the code
https://github.com/ivcafe413/Astracraft.git

Keeping the source code open for possible future tutorial/post-mortem

## Debugging the game
Run the entrypoint.py script to debug the game. A launch configuration for debugging is available in .vscode/launch.json (VS Code)

## Building the game
pip install pyinstaller
pyinstaller entrypoint.py --name astracraft

## Pusing the build
Initial build channel is vagranttechnology/astracraft:windows-dev
butler push dist/astracraft vagranttechnology/astracraft:windows-dev