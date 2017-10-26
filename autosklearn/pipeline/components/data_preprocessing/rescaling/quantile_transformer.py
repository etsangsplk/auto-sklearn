from ConfigSpace.configuration_space import ConfigurationSpace
from ConfigSpace.hyperparameters import UniformIntegerHyperparameter, \
    CategoricalHyperparameter

from autosklearn.pipeline.constants import *
from autosklearn.pipeline.components.data_preprocessing.rescaling.abstract_rescaling \
    import Rescaling
from autosklearn.pipeline.components.base import \
    AutoSklearnPreprocessingAlgorithm


class QuantileTransformerComponent(Rescaling, AutoSklearnPreprocessingAlgorithm):
    def __init__(self, n_quantiles, output_distribution, random_state):
        from sklearn.preprocessing import QuantileTransformer
        self.preprocessor = QuantileTransformer(
            n_quantiles=n_quantiles,
            output_distribution=output_distribution,
        )

    @staticmethod
    def get_properties(dataset_properties=None):
        return {'shortname': 'QuantileTransformer',
                'name': 'QuantileTransformer',
                'handles_regression': True,
                'handles_classification': True,
                'handles_multiclass': True,
                'handles_multilabel': True,
                'is_deterministic': True,
                # TODO find out of this is right!
                'handles_sparse': True,
                'handles_dense': True,
                'input': (DENSE, UNSIGNED_DATA),
                'output': (INPUT, SIGNED_DATA),
                'preferred_dtype': None}

    def get_hyperparameter_search_space(dataset_properties=None):
        cs = ConfigurationSpace()
        n_quantiles = UniformIntegerHyperparameter(
            'n_quantiles', lower=10, upper=int(1e5), default_value=1000
        )
        output_distribution = CategoricalHyperparameter(
            'output_distribution', ['uniform', 'normal']
        )
        cs.add_hyperparameters((n_quantiles, output_distribution))
        return cs