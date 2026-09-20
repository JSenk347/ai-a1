from translator import UniversalTranslator
import numpy as np


# create the UniversalTranslator object, with 10 knobs
translator = UniversalTranslator(n_dim=10)

# demo of how to use the UniversalTranslator object. You can delete these lines
random_settings = np.random.random(size=10)
translated_string = translator.translate(random_settings)
print(translated_string)

# print total number of settings evaluated
print(f'# settings tried: {translator.n_settings_tried()}')