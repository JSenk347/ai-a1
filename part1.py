from translator import UniversalTranslator
from plotter import generate_search_plot
from scoring import Scorer
from searcher import Searcher
from plotter import generate_search_plot
import numpy as np


def main(): 
    # create the UniversalTranslator object, with 2 knobs
    translator = UniversalTranslator(n_dim=2)

    # Josephs scorer to our translator instance
    scorer = Scorer(translator)
    #searcher = Searcher(n_dim=2, stop_limit=25, step_size=0.1, scorer=scorer)
    searcher = Searcher(n_dim=2, stop_limit=100, step_size=0.2, scorer=scorer, patience=50)

    start_settings = np.array([0.5, 0.5])
    best_settings, best_score = searcher(start_settings)

    # print total number of settings evaluated
    print(f"Best Knob Setting Found: {best_settings}")
    print(f"Best Decode Rate Found: {best_score}")
    print(f"Total Number of Settings Tried: {translator.n_settings_tried()}")

    # generating scatter plot for the data provided
    generate_search_plot(scorer.history)

if __name__ == "__main__":
    main()
