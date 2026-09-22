from translator import UniversalTranslator
import numpy as np
import time

# create the UniversalTranslator object, with 10 knobs
translator = UniversalTranslator(n_dim=10)

# demo of how to use the UniversalTranslator object. You can delete these lines
random_settings = np.random.random(size=10)
translated_string = translator.translate(random_settings)
print(translated_string)

# print total number of settings evaluated
print(f'# settings tried: {translator.n_settings_tried()}')

# 60 second timer
def sixty_seconds():
    for seconds in range(60, -1, -1):
        print(f"\rTime remaining: {seconds} seconds", end="", flush=True)
        time.sleep(1)

    print("\nTime's up!")

