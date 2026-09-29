Write your answers to the following questions in this file, *after* completing everything else.

# 1) How many settings must be evaluated to *exhaustively* search for the best set (e.g. through some kind of brute-force search). State your assumptions and explain how you arrived at your answer. How does your solution compare to this (quantitatively)?




# 2) Why is the 10-knob problem harder than the 2-knob problem? (It may help you to know that the *mechanics* of both problems were the same: the relationship between settings and performance had the same general characteristics, there were just more settings to tune in the 10-knob problem).




# 3) If your program was seen as an "agent program", which of the agent types discussed in class would it be?
- A **utility agent** as there is no explicit goal state since a 100% decode rate may be impossible
- It ranks candidate settings using a utility function, which in this code is the Scorer.score() function that calculates the settings decode rate, which is the score. This utility function
allows us to find the next best step to take, all while maintaining state and never re-writing its own decision rules.

# 4) it's often said that the simplest solution is the best. How well would a basic hill-climbing search perform in this problem? Justify your answer using your findings or plots from part 1 (you can answer this question whether or not you used hill-climbing as your approach). 



# 5) When you moved from the 2- to the 10-knob problem, did you change your search algorithm? Why or why not?