from translator import UniversalTranslator
from plotter import generate_search_plot

# create the UniversalTranslator object, with 2 knobs
translator = UniversalTranslator(n_dim=2)

# demo of how to use the UniversalTranslator object. You can delete these lines
sample_settings = [0, 0.5]
translated_string = translator.translate(sample_settings)
print(translated_string)

# print total number of settings evaluated
print(f'# settings tried: {translator.n_settings_tried()}')

mock_data = {
    'setting_1': {"knobs": [0, 0.5], "scores": 0.1},
    'setting_2': {"knobs": [0.5, 0.5], "scores": 0.2},
    'setting_3': {"knobs": [0.5, 1], "scores": 0.3},
    'setting_4': {"knobs": [1, 0.5], "scores": 0.4},
}

# generating scatter plot for the data provided
generate_search_plot(mock_data)