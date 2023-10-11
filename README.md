# Daughters_of_the_Wreath
This is the current prototype for a character-building software for my Daughter's of the Wreath TTRPG system. The rules for this game system are still in development (as of 2023) and are being produced in concert with the software.
Much of this game relies on the use of skill trees, which this code implements in PyGame

SkillTree.py - hosts the game itsef which generates the skill tree and allows for building a character
SkillTreeFunctions.py - holds useful functions for running SkillTree
closing_graph_under_symmetry.py - is a helper function to make the underlying graph object symmetric, which eases the hard coding process

nodeEffects.py - hard codes all the node effects

the various spreadsheets hold node information, both game-functionality and tree-properties
