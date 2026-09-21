from translator import UniversalTranslator
from scoring import Scorer

translator = UniversalTranslator(n_dim=2)
score = Scorer(translator)

print(score([0.77, 0.31]))    # 0.3942
print(score([0.1, 0.1]))      # 0.0
print(score.best())           # ([0.77, 0.31], 0.3942)