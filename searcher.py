from translator import UniversalTranslator
from scoring import Scorer

class Searcher:
    '''
    A searcher class that utilizes the hill-climbing search algorithm to find the
    knob settings that yield the highest translation score.
    '''
    @staticmethod
    def _validate(n_dim, stop_limit, step_size):
        '''
        Raises ValueError if the search parameters can't produce a meaningful search.
        '''
        if isinstance(n_dim, bool) or (n_dim != 2 and n_dim != 10):
            raise ValueError(f"n_dim must be either 2 or 10, got {n_dim}")
        if isinstance(step_size, bool) or not isinstance(step_size, (int, float)):
            raise ValueError(f"step_size must be a number, got {step_size}")
        if not (0 < step_size < 1):
            raise ValueError(f"step_size must be in (0, 1), got {step_size}")
        if isinstance(stop_limit, bool) or not isinstance(stop_limit, int):
            raise ValueError(f"stop_limit must be an integer, got {stop_limit}")

        # 1 eval for start point, plus one full round of single-knob neighbours
        # (2 per knob: +step and -step)
        min_limit = 1 + 2 * n_dim
        if stop_limit < min_limit:
            raise ValueError(
                f"stop_limit={stop_limit} is too small for {n_dim} knobs: "
                f"need at least {min_limit} (1 start + {2 * n_dim} neighbours)"
            )  

    def __init__(self, n_dim: int, stop_limit: int, step_size: int):
        self._validate(n_dim, stop_limit, step_size)

        self.scorer = Scorer(UniversalTranslator(n_dim=n_dim))
        self.curr = ()
        self.curr_score = None
        self.frontier = set()          # neighbours of curr still worth considering
        self.seen = set()              # every place we have stood on, i.e. once been curr
        self.scores = {}               # every point we have paid to score: {settings tuple: score}
        self.stop_limit = stop_limit
        self.step_size = step_size
        self.num_evals = 0

    def __call__(self, start_settings):
        '''
        This function utilizes the hill-climbing search algorithm to 
        find the best knob setting for the receiver, using Joseph's 
        Scorer to determine which settings provide the steepest incline.
        Args:
            start: the starting knob positions
        Returns:
            The optimal knob settings for the receiver.
        '''
        self.curr = to_key(start_settings)
        self.curr_score = self._evaluate(self.curr)

        while True:
            self.seen.add(self.curr)
            self.expand()
            if not self.frontier:      # every neighbour is somewhere we've already stood
                break

            # look at every neighbour and remember the highest-scoring one
            best_neighbour = None
            best_score = float("-inf")
            budget_left = True
            for setting in sorted(self.frontier):    # sorted: ties break the same way every run
                if setting not in self.scores and self.num_evals >= self.stop_limit:
                    budget_left = False              # check BEFORE every scorer call
                    break
                score = self._evaluate(setting)
                if score > best_score:
                    best_neighbour = setting 
                    best_score = score

            # take the step only if it is strictly uphill
            if best_neighbour != None and best_score > self.curr_score:
                improved = best_neighbour
                self.curr = best_neighbour
                self.curr_score = best_score

            # no uphill neighbour = local maximum (a plateau also stops us), or out of budget
            if not improved or not budget_left:
                break

        return self.best()

    def _evaluate(self, point):
        '''
        Scores a point, paying for it (one scorer call) only the first time we see it.
        '''
        if point not in self.scores:
            self.scores[point] = self.scorer(point)
            self.num_evals += 1
        return self.scores[point]

    def expand(self):
        # a set: order doesn't matter, and duplicates (e.g. from clipping) vanish for free
        self.frontier = set()
        self.frontier.update(single_steps(self.curr, self.step_size))
        #self.frontier.extend(sweeping_steps(self.curr, self.step_size, direction=+1))
        #self.frontier.extend(sweeping_steps(self.curr, self.step_size, direction=-1))

        # never step back onto a place we've already stood on (this also stops loops)
        self.frontier.difference_update(self.seen)

    def best(self):
        '''
        Returns the best scored (knob settings, score) pair, in the same format
        as Scorer.best(): a list of settings and its score. If several
        settings tie, the one scored first wins.
        '''
        if not self.scores:
            raise ValueError("no settings have been scored yet")
        best_settings = max(self.scores, key=self.scores.get)
        return list(best_settings), self.scores[best_settings]


def clip(value):
    '''
    Keeps a knob value inside the legal range [0, 1]. Joseph's Scorer raises a
    ValueError for anything outside it.
    '''
    return min(1.0, max(0.0, value))

def to_key(point):
    '''
    Turns a list/tuple of knob values into a hashable tuple so it can live in a set.
    Rounding makes 0.30000000000000004 and 0.3 count as the same point.
    '''
    return tuple(round(v, 10) for v in point)

# curr is a tuple of knob values, with 2 or 10 elements (knobs)
def single_steps(curr, step_size):
    '''
    Returns a list of tuples: curr with one knob moved up or down by step_size.
    '''
    neigbs = []

    for i, knob in enumerate(curr):
        incr = list(curr)
        incr[i] = clip(knob + step_size)
        neigbs.append(to_key(incr))

        decr = list(curr)
        decr[i] = clip(knob - step_size)
        neigbs.append(to_key(decr))

    return neigbs

def sweeping_steps(curr, step_size, direction):
    """
    Walk step_size in `direction` (+1 or -1) across knobs left to right,
    then partially walk back in the opposite direction over all but the
    last two knobs.

    e.g. direction=+1, curr=[.5, .5, .5]:
        [.5,.5,.5] -> [.6,.6,.5] -> [.6,.6,.6] -> [.5,.6,.6]
    (the starting state is skipped — _perturb_single_knobs already covers it)
    """
    neighbours = []

    primed = list(curr)
    primed[0] = clip(primed[0] + direction * step_size)
    for i in range(1, len(primed)):
        primed[i] = clip(primed[i] + direction * step_size)
        neighbours.append(to_key(primed))

    reversed_primed = list(primed)
    for i in range(0, len(reversed_primed) - 2):
        reversed_primed[i] = clip(reversed_primed[i] - direction * step_size)
        neighbours.append(to_key(reversed_primed))

    return neighbours



if __name__ == "__main__":
    # hangs if stop_limit > 13. idk why
    searcher = Searcher(n_dim=2, stop_limit=13, step_size=0.1)
    print(searcher((0.5, 0.5)))
