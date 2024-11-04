Scripts to automate importing and manipulating assets in various UE versions for various games.

Originally based on Tangerie's scripts for Hogwarts Legacy data assets, with extensive modifications made by me (peek) to support material instances (MIs) and various custom Tekken 8 datatypes.

 - Use the master branch for Hogwarts Legacy (UE 4.27chaos)
 - Use the aewff branch for AEW Fight Forever (UE 4.27).  Might work to a limited extent for other UE 4.27 games such as MK 1.
 - Use the tekken8 branch for Tekken 8 (UE 5.2)

Usage:
 - Grab the appropriate branch for your game's UE version, and stick the code in the Content/Python directory of your project
 - Enable the python editor script plugin in UE
 - Right-click on supported assets or MIs and select "Scripted actions" or go into the Output Log, change the dropdown from cmd to Python, and run whichever script you want
