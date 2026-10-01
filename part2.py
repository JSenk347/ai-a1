from translator import UniversalTranslator
import numpy as np
import time
from searcher import Searcher
from scoring import Scorer 

def main():
    translator = UniversalTranslator(n_dim=10)
    scorer = Scorer(translator)
    searcher = Searcher(10, 10000, 0.2, scorer, patience=50)

    start_settings = np.full(10, 0.5)

    start_time = time.perf_counter()

    best_settings, best_score = searcher(start_settings)
    print(best_score)

    end_time= time.perf_counter()  
    full_time = end_time - start_time

    print(f"Best settings = {best_settings}")
    print(f"Best decode rate = {best_score:.4f}")
    print(f"Time taken = {full_time:.4f} seconds")
    print(f"Total number of settings tried = {translator.n_settings_tried()}")
        

if __name__ == "__main__":
    main() 


