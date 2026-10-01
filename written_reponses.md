Write your answers to the following questions in this file, *after* completing everything else.

# 1) How many settings must be evaluated to *exhaustively* search for the best set (e.g. through some kind of brute-force search). State your assumptions and explain how you arrived at your answer. How does your solution compare to this (quantitatively)?

- Each knob is continuous on the range of [0,1], so a complete exhaustive search would require an infinite amount of computations. 

- The amount of settings that must be tried to exhaustively search for the best solution set depends on the step size taken so taking only 0.2 steps will result in 6^(number of knobs) possible combinations. 2 knobs would be 36 settigns and 10 knobs would 6^10 so 60.5 million settings. Our searcher starts with 0.2 and our step size shrinks down to 0.005 so matching that resolution would require 201^10 settings

- Our searcher will try at most 10000 settings which amounts to about 0.017% of the 0.2 grid of possible solutions which is around 6000 times fewer evaluations than a brute force ssolutionwould try at 0.2 step size.




# 2) Why is the 10-knob problem harder than the 2-knob problem? (It may help you to know that the *mechanics* of both problems were the same: the relationship between settings and performance had the same general characteristics, there were just more settings to tune in the 10-knob problem).




# 3) If your program was seen as an "agent program", which of the agent types discussed in class would it be?
- A **utility agent** as there is no explicit goal state since a 100% decode rate may be impossible
- It ranks candidate settings using a utility function, which in this code is the Scorer.score() function that calculates the settings decode rate, which is the score. This utility function
allows us to find the next best step to take, all while maintaining state and never re-writing its own decision rules.

# 4) it's often said that the simplest solution is the best. How well would a basic hill-climbing search perform in this problem? Justify your answer using your findings or plots from part 1 (you can answer this question whether or not you used hill-climbing as your approach). 
- A basic hill climbing search would perform very poorly on this problem. Basic hill climbing will keep evaluating its neighbours, but once it no longer finds a neighbour with a higher decode rate it will end up stopping. Our part 1 plot shows exactly why this would fail. On our graph you can see multiple disconnected clusters of points. For example, near (0.5,0.5) its a lone purple (low decode rate) point and the yellow (high decode rate) point cluster at (0.15,0.6). Because the data includes multiple local maximums and zero score plateaus (an area where all of the neighbours are the same) it is clear that a basic hill climbing search starting at (0.5,0.5) would get stuck almost immediately on a minor peak and fail to reach the global peak at (0.15,0.6). To be able to overcome this, we incorporated a calibrate method to escape zero plateaus, step size halving to search with more detail as in the assignment outline neighbours would be smooth transitions and not jumps, and random restarts to jump across the graph in the case of a local maximum and escape it. Finally, while a basic hill climbing search would indeed perform poorly, our modified and enhanced one performs successfully.

# 5) When you moved from the 2- to the 10-knob problem, did you change your search algorithm? Why or why not?
