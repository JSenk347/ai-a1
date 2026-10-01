Write your answers to the following questions in this file, *after* completing everything else.

# 1) How many settings must be evaluated to *exhaustively* search for the best set (e.g. through some kind of brute-force search). State your assumptions and explain how you arrived at your answer. How does your solution compare to this (quantitatively)?




# 2) Why is the 10-knob problem harder than the 2-knob problem? (It may help you to know that the *mechanics* of both problems were the same: the relationship between settings and performance had the same general characteristics, there were just more settings to tune in the 10-knob problem).

The search works the same way in both problems but each knob adds a dimension and three things get worse as dimensions are added:

1. The space grows exponentially. Two knobs give 10^2 = 100 combinations and ten knobs give 10^10 = 10 billion. The same number of evaluations covers a far smaller share of the space. 
2. Each step costs more. Our searcher moves one knob up or down at a time, so it checks 2d neighbours. That's 4 for two knobs and 20 for ten, so every step costs five times as many evaluations.
3. Almost every settings scores zero. 

As a result, part 1 reached a decode rate of 0.938 in 100 evaluations, while part 2 needed about 9,400 evaluations to reach 0.700.

# 3) If your program was seen as an "agent program", which of the agent types discussed in class would it be?
- A **utility agent** as there is no explicit goal state since a 100% decode rate may be impossible
- It ranks candidate settings using a utility function, which in this code is the Scorer.score() function that calculates the settings decode rate, which is the score. This utility function
allows us to find the next best step to take, all while maintaining state and never re-writing its own decision rules.

# 4) it's often said that the simplest solution is the best. How well would a basic hill-climbing search perform in this problem? Justify your answer using your findings or plots from part 1 (you can answer this question whether or not you used hill-climbing as your approach). 
- A basic hill climbing search would perform very poorly on this problem. Basic hill climbing will keep evaluating its neighbours, but once it no longer finds a neighbour with a higher decode rate it will end up stopping. Our part 1 plot shows exactly why this would fail. On our graph you can see multiple disconnected clusters of points. For example, near (0.5,0.5) its a lone purple (low decode rate) point and the yellow (high decode rate) point cluster at (0.15,0.6). Because the data includes multiple local maximums and zero score plateaus (an area where all of the neighbours are the same) it is clear that a basic hill climbing search starting at (0.5,0.5) would get stuck almost immediately on a minor peak and fail to reach the global peak at (0.15,0.6). To be able to overcome this, we incorporated a calibrate method to escape zero plateaus, step size halving to search with more detail as in the assignment outline neighbours would be smooth transitions and not jumps, and random restarts to jump across the graph in the case of a local maximum and escape it. Finally, while a basic hill climbing search would indeed perform poorly, our modified and enhanced one performs successfully.

# 5) When you moved from the 2- to the 10-knob problem, did you change your search algorithm? Why or why not?

Partly. Both parts run the same hill-climbing Searcher class. Neighbours are built from n_dim so the code handles any number of knobs. We kept hill climbing because the assignment says the decode rate varies smoothly, so a neighbour's score reliably shows which direction is uphill and the 10 knob problem has the same mechanics as the 2 knob one.


The 10 knob problem did expose weaknesses in a plain hill climber, so we added three extensions:

1. Plateau escape (calibrate): if the start point scores zero, the searcher samples random settings until one scores above zero then climbs from there. Most 10 knob settings score zero. Our first version moved on ties, so it drifted across the flat region until every knob was at 1.0, still scoring zero. 
2. Step halving: When no neighbour improves the score, the step size halves, down to a minimum of 0.005. The search makes drastic moves first and finer ones near a peak.
3. Restarts near the best point: when a climb ends, the searcher adds noise to the best setting so far and climbs again. This changes the best point locally rather than restarting somewhere random, so it checks nearby hills for a higher peak. The downside of that is that if the first hill is a weak one, the restarts tend to stay near it. 

We changed one parameter for part 2. The evaluation limit goes from 100 to 10,000 because each step costs five times as many evaluations. Patience, the number of climbs in a row without a new best before the search stops, stays at 50, but in practice the evaluation limit is what stops the search. The starting step stays at 0.2 and a 45 second time limit keeps the search under the 60 second requirement, although a run takes about 3.5 seconds. 