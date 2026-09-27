import numpy as np
from translator import UniversalTranslator
from scoring import Scorer

UPPER_BND = 1
LOWER_BND = 0

class Searcher:

    # need to validate init args

    def __init__(self, n_dim: int, stop_limit: int, step_size: float):
        self.scorer = Scorer(UniversalTranslator(n_dim=n_dim))
        self.n_dim = n_dim             # number of knobs: 2 or 10
        self.stop_limit = stop_limit   # max number of times we can call self.scorer
        self.step_size = step_size     # how far one move changes a knob, in (0, 1)
        self.num_evals = 0             # number of scorer calls so far; also the next free row in the two arrays below
        self.has_searched = False

        self.curr = np.full(n_dim, np.nan)      # shape (n_dim,): knob values of the point we are standing on
        self.curr_score = np.nan                # score of curr; nan until curr has been scored

        self.frontier = np.empty((0, n_dim))    # shape (k, n_dim): neighbours of curr still worth considering, one per row
        self.seen = np.empty((0, n_dim))        # shape (m, n_dim): every point we have stood on, one per row
        self.seen_scores = []

        self.curr_best_pos = np.full(n_dim, np.nan)

    def __call__(self, starting_settings: np.ndarray):
        if not self.has_searched:
            self.validate_start(starting_settings)
            self.curr = starting_settings
            self.seen = np.vstack((self.seen, starting_settings)) # add starting settings to the array of settings we've been to
            
            while self.num_evals < self.stop_limit:
                self.expand_frontier()
                self.examine_frontier()
                self.take_step()

            self.has_searched = True
  
            return self.curr, self.scorer.best()[1]
        else:
            raise LookupError("A searcher can only climb one hill. Create another searcher to climb another hill.")



        

    def expand_frontier(self):
        '''
        Expands the frontier from our self.curr position by creating a step_matrix (identify matrix multiplied by
        step size scalar) and adding/subtracting our current knob settings to each row of the step_matrix, then stacking
        those two matrices on the self.frontier stack of matrices. Element values are bound in [0, 1] with np.clip(),
        and deduped with np.unique() (which sorts the knob setting arrays in asc order).

        Args:
            self: searcher object
        Returns:
            none
        '''
        self.frontier = np.empty((0, self.n_dim))
        step_matrix = np.eye(self.n_dim) * self.step_size # creates identity matrix with diagonal value of step_size

        # add/subtract curr knob position to each row of identify matrix
        # clipping element values to be within bounds with np.clip
        incr_frontier = np.clip((self.curr + step_matrix), a_min=LOWER_BND, a_max=UPPER_BND)
        decr_frontier = np.clip((self.curr - step_matrix), a_min=LOWER_BND, a_max=UPPER_BND)

        self.frontier = np.vstack((self.frontier, incr_frontier, decr_frontier)) # "vertically stacks" arrays to self.frontier
        self.frontier = np.unique(self.frontier, axis=0) # axis=0 means it looks for duplicate ROWS. SORTS self.frontier

    def examine_frontier(self):
        '''
        Scores every array of knob settings in self.frontier and updates self.curr_best_pos with the pos that
        provided the best score
        '''
        self.curr_score = self.scorer(self.curr)
        best_score = self.curr_score
        self.curr_best_pos = self.curr

        self.num_evals += 1

        for pos in self.frontier:
            score = self.scorer(pos)
            self.seen_scores.append(score)
            self.num_evals += 1

            if score >= best_score:
                self.curr_best_pos = pos
                print(f"found better score {best_score} -> {score} at {pos}")
                best_score = score
                
    def take_step(self):
        self.curr = self.curr_best_pos
        self.seen = np.vstack((self.seen, self.curr))


    def validate_start(self, start_pos: np.ndarray):
        if start_pos.shape != (self.n_dim,):
            raise ValueError(f"starting settings must have shape ({self.n_dim}, ), but {start_pos} has shape {start_pos.shape}")
        for knob in start_pos:
            if knob < 0 or knob > 1:
                raise ValueError(f"knob settings must be bound by [0, 1], got {start_pos}.")

if __name__ == "__main__":
    searcher = Searcher(2, 50, 0.05)
    print(searcher(np.array([.5, .5])))




        

         
