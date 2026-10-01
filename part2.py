from translator import UniversalTranslator
import numpy as np
import time
from searcher import Searcher
from scoring import Scorer

def main():
    # create the UniversalTranslator object, with 10 knobs
    translator = UniversalTranslator(n_dim=10)

    # scorer wraps the translator and returns the decode rate for a setting
    scorer = Scorer(translator)

    # same hill-climbing searcher as part 1, with a 10,000 evaluation limit
    
    # starting step is 0.2; patience (50) stops after that many climbs in a row with no new best
    searcher = Searcher(10, 10000, 0.2, scorer, patience=50)

    # start every knob in the middle of its [0, 1] range
    start_settings = np.full(10, 0.5)

    start_time = time.perf_counter()

    best_settings, best_score = searcher(start_settings)

    end_time= time.perf_counter()
    full_time = end_time - start_time

    # print the best settings, decode rate, run time, and total number of settings evaluated
    print(f"Best settings = [{', '.join(f'{x:.4f}' for x in best_settings)}]")
    print(f"Best decode rate = {best_score:.4f}")
    print(f"Time taken = {full_time:.4f} seconds")
    print(f"Total number of settings tried = {translator.n_settings_tried()}")


if __name__ == "__main__":
    main()


