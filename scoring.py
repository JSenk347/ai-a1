class Scorer:

    def __init__(self, translator):

        self.translator = translator     
        self.history = []   # pair of (knobs_setting, score)
        
    def __call__(self, knobs_setting):

        knobs_setting = self.check_settings(knobs_setting)

        message = self.translator.translate(knobs_setting)
        score = decode(message)

        self.history.append((knobs_setting, score))

        return score
    
    def best(self):
        best_settings, best_score = self.history[0]
        
        for settings, score in self.history:
            if score > best_score:
                best_settings = settings
                best_score = score
        return best_settings, best_score


def decode(message):

    words = message.split()
    translated_count = 0

    for word in words:

        if word.isdigit():           # all digits = still an alien code
            continue

        translated_count = translated_count + 1

    return translated_count / len(words)

def check_settings()