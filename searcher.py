import numpy as np
from translator import UniversalTranslator
from scoring import Scorer

UPPER_BND = 1
LOWER_BND = 0
MIN_STEP = 0.005

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

    def __init__(self, n_dim: int, stop_limit: int, step_size: float, scorer: Scorer):
        self._validate(n_dim, stop_limit, step_size)
        if scorer.translator.n_dim != n_dim:
            raise ValueError(f"searcher n_dim={n_dim} but translator n_dim={scorer.translator.n_dim}")
        
        self.scorer = scorer
        self.n_dim = n_dim             # number of knobs: 2 or 10
        self.stop_limit = stop_limit   # max number of times we can call self.scorer
        self.init_step = step_size     # step size each new climb starts with
        self.step_size = step_size     # current step size
        self.num_evals = 0             # number of scorer calls made so far
        self.has_searched = False

        self.curr = np.full(n_dim, np.nan)      # shape (n_dim,): knob values of the point we are standing on
        self.curr_score = np.nan                # score of curr; nan until curr has been scored

        self.frontier = np.empty((0, n_dim))    # shape (k, n_dim): neighbours of curr still worth considering, one per row

        self.seen = np.empty((0, n_dim))        # shape (m, n_dim): every point we have stood on, one per row
        self.seen_scores = []                   #

        self.curr_best_pos = np.full(n_dim, np.nan)

        self.best_pos = np.full(n_dim, np.nan) # best point found across all climbs
        self.best_score = -np.inf

    def __call__(self, start_settings: np.ndarray):
        if self.has_searched:
            raise LookupError("A searcher can only search once. Create another searcher")

        # first climb starts from the given point; only escape the plateau if it scores 0
        start_score = self._score(start_settings)
        if start_score is not None:
            if start_score > 0:
                self._stand_on(start_settings, start_score)
                started = True
            else:
                started = self.calibrate()

            while started:
                self._climb()
                started = self.calibrate()   # next restart (replaced in Change 2)

        self.has_searched = True
        return self.best_pos, self.best_score

    def _climb(self):
        '''
        Hill climbs from curr until step_size drops below MIN_STEP or the budget runs out.
        '''
        while self.step_size >= MIN_STEP and self.num_evals < self.stop_limit:
            self.expand_frontier()
            if not self.examine_frontier():
                break
            self.take_step()

    def _score(self, pos):
        '''
        Scores pos, updating the eval count and gloabl best. Returns None if out of budget.
        '''
        if self.num_evals >= self.stop_limit:
            return None
        score = self.scorer(pos)
        self.num_evals += 1
        if score > self.best_score:
            self.best_score, self.best_pos = score, np.array(pos, dtype=float)
        return score
        
    def calibrate(self):
        '''
        Random restart: sample uniformly until a point scores > 0, then stand on it.
        Returns False if the budget runs out first.
        '''
        while True:
            candidate = np.random.uniform(LOWER_BND, UPPER_BND, self.n_dim)
            score = self._score(candidate)
            if score is None:
                return False
            if score > 0:
                self._stand_on(candidate, score)
                return True

    def _stand_on(self, pos, score):
        '''
        Makes pos (already scored) the current point and resets the step size for a new climb.
        '''
        self.curr, self.curr_score = np.array(pos, dtype=float), score
        self.step_size = self.init_step
        self.seen = np.vstack((self.seen, self.curr))
        self.seen_scores.append(self.curr_score)

    def expand_frontier(self):
        '''+/- step_size on each knob (2*n_dim neighbours), clipped to [0, 1], deduped.'''
        step_matrix = np.eye(self.n_dim) * self.step_size
        incr = np.clip(self.curr + step_matrix, LOWER_BND, UPPER_BND)
        decr = np.clip(self.curr - step_matrix, LOWER_BND, UPPER_BND)
        self.frontier = np.unique(np.vstack((incr, decr)), axis=0)
        # drop rows identical to curr (happens when curr is on a boundary)
        self.frontier = self.frontier[~np.all(self.frontier == self.curr, axis=1)]

    def examine_frontier(self):
        '''
        Scores every neighbour. curr_score is already known, so curr is NOT re-scored.
        Only a STRICTLY better neighbour is a move; ties among the best improving
        neighbours are broken at random. No improvement -> halve step_size.
        Returns False if the budget ran out.
        '''
        best_score = self.curr_score
        tied = []
        for pos in self.frontier:
            score = self._score(pos)
            if score is None:
                return False
            if score > best_score:
                best_score, tied = score, [pos]
            elif score == best_score and tied:   # tie with an improving neighbour, not with curr
                tied.append(pos)

        if tied:
            self.curr_best_pos = tied[np.random.randint(len(tied))]
            self.curr_score = best_score
        else:
            self.curr_best_pos = self.curr       # local optimum at this resolution
            self.step_size /= 2                  # zoom in
        return True

                
    def take_step(self):
        if not np.array_equal(self.curr_best_pos, self.curr):
            self.curr = self.curr_best_pos
            self.seen = np.vstack((self.seen, self.curr))
            self.seen_scores.append(self.curr_score)


if __name__ == "__main__":
    N_DIM = 10
    translator = UniversalTranslator(n_dim=N_DIM)
    scorer = Scorer(translator)
    searcher = Searcher(N_DIM, 3000, 0.1, scorer)
    best_pos, best_score = searcher(np.full(N_DIM, 0.5))
    print(f"best settings: {np.round(best_pos, 3)}")
    print(f"best decode rate: {best_score:.4f}")
    print(f"settings tried: {translator.n_settings_tried()}")