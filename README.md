# Discord Bot - Dice roll

Simple Discord robot that allows you to simulate a roll of the dice with the possibility of choosing the desired percentages on the desired surfaces.

## USAGE

Requires the creation of a `config` file with a `TOKEN` key

for run the script :

`python3 rolled_dice.py`

Command to launch on Discord to activate the bot:

**Roll a die and choose the desired percentages per side:**

`!dice dp10 d 1 3 5 p 20 20 20`

**Explanation of the command :**

`!dice` allows to call the bot.

`dp10` *dp for Dice Percent* - allows you to choose the number of sides of the dice (example, d2, d6, d20)

`d 1 3 5` *d for Dice* - allows you to select the faces of the dice on which we want to assign a percentage.

`p 20 20 20` *p for Percent* - allows to assign the percentages in the order given beforehand


**Rolling a simple dice**

`!dice 3d6`

**Explanation of the command :**

`!dice` allows to call the bot.

`3` the number of dice
`d` for dice
`6` the number of surfaces of the die
