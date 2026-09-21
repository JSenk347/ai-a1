import math

class Scorer:
    '''A scoring class that uses a translator to compute scores for knob settings. 
    The score is computed by translating the knob settings and counting the number of translated words. 
    The score is normalized by the total number of words in the message.'''
    def __init__(self, translator):

        self.translator = translator     
        self.history = []   # pair of (knobs_setting, score)
        
    '''
    Computes the score for a given knob setting. The score is computed by translating the knob settings'''
    def __call__(self, knobs_settings):

        knobs_settings = self.check_settings(knobs_settings)

        message = self.translator.translate(knobs_settings)
        score = decode(message)

        self.history.append((knobs_settings, score))

        return score
    
    '''
    Computes the best score and the corresponding knob settings from the history of scores.
    '''
    def best(self):
        best_settings, best_score = self.history[0]
        
        for settings, score in self.history:
            if score > best_score:
                best_settings = settings
                best_score = score
        return best_settings, best_score
    '''
    Checks the validity of the knob settings, if the settings are unvalid it would inflate our attempt count.
    '''
    def check_settings(self, settings):
        our_copy = []

        for value in settings:
            our_copy.append(float(value))

        if len(our_copy) != self.translator.n_dim:
            raise ValueError(
                f"expected {self.translator.n_dim} knob values, "
                f"got {len(our_copy)}"
            )

        for knob_number, value in enumerate(our_copy):
            if math.isnan(value):
                raise ValueError(
                    f"knob {knob_number} is not a number"
                )

            if value < 0 or value > 1:
                raise ValueError(
                    f"knob {knob_number} is {value}, "
                    "which is outside [0, 1]"
                )

        return our_copy
    
'''
Decodes the message by counting the number of translated words and dividing by words in the coded message.
'''
def decode(message):
    words = message.split()
    translated_count = 0

    for word in words:
        if word.isdigit():           # all digits = still an alien code
            continue
        translated_count = translated_count + 1
    return translated_count / len(words)
