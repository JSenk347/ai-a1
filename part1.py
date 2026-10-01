import time
from translator import UniversalTranslator
from plotter import generate_search_plot
from scoring import Scorer
from searcher import Searcher
import numpy as np


def main(): 
    # create the UniversalTranslator object, with 2 knobs
    translator = UniversalTranslator(n_dim=2)

    # Josephs scorer to our translator instance
    scorer = Scorer(translator)
    searcher = Searcher(n_dim=2, stop_limit=100, step_size=0.2, scorer=scorer, patience=50)

    start_settings = np.array([0.5, 0.5])

    start_time = time.perf_counter()

    best_settings, best_score = searcher(start_settings)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    # print total number of settings evaluated
    print(f"Best Knob Setting Found: [{', '.join(f'{x:.4f}' for x in best_settings)}]")
    print(f"Best Decode Rate Found: {best_score:.4f}")
    print(f"Time taken = {elapsed_time:.4f} seconds")
    print(f"Total Number of Settings Tried: {translator.n_settings_tried()}")

    # scatter plot of every setting tried (scorer.history logs each scorer call)
    generate_search_plot(scorer.history)

if __name__ == "__main__":
    main()
