'''
This file contains the UniversalTranslator object you'll use for the assignment
Don't make changes to this file.
'''

import numpy as np
from translator_core_ob import 𥩣𞸏𬧼𠕷𱮌, 𥩣𞸏𬧼𠕷𠧝


class UniversalTranslator:
    """
    A class to represent the spaceship's universal translator. 
    """
    
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, n_dim: int):
        """
        :param int n_dim: number of dimensions along which to optimize (number of settings for the translator)
        """
        if not self.__initialized:
            self.n_dim = n_dim
            self.__evals = 0

            self.problem = 𥩣𞸏𬧼𠕷𱮌(n_dim)

            self.__initialized = True

    def translate(self, settings: list | np.ndarray) -> str:
        """
        try to translate the alien message, using the given translator settings
        :param settings: a list or array of settings to try. Must have length = n_dims. Each value should be in the range [0, 1]
        :return: the translated string, with some fraction of the numeric codes translated successfully 
        """
        self.__evals += 1

        settings = np.array(settings)
        if len(settings) != self.n_dim:
            raise ValueError("length of settings array must match number of dimensions for the translator object")
        
        return 𥩣𞸏𬧼𠕷𠧝(self.problem(settings))
    
    def n_settings_tried(self) -> int:
        """
        returns the number of settings tried (the total number of translations performed)
        """
        return self.__evals


if __name__ == '__main__':
    # demo of how to use the UniversalTranslator object

    dimensions = 2
    translator = UniversalTranslator(n_dim=dimensions)
    translated_string = translator.translate(settings=[0, 0.5])
    print(translated_string)
    print(f'# settings tried: {translator.n_settings_tried()}')