from models.model_building import build_embedding_model
import tensorflow.keras.layers as layers
from models.difference_layer import DifferenceLayer
from tensorflow.keras.models import load_model


# for loading the siamese model

def load_siamese_model(
    path=''
  ):
  """
  For loading the model while indicating the custom layer we made.
  """
  # default value
  if not path:
    path = 'results/models/best_model.h5'
  model = load_model(path, custom_objects={'DifferenceLayer': DifferenceLayer})
  return model


# for loading a submodel

def load_embedding_model(
    num_dense_layers,
    embedding_size,
    path_to_siamese='results/models/best_model.h5'
    ):
    """
    Loads the siamese model and extracting the trained embedding model.
    """
    siamese_model = load_siamese_model(path=path_to_siamese)

    # we get the input shape of one submodel from that of the siamese model
    input_shape = siamese_model.input_shape[0][1:]
    input_a = layers.Input(name="input_a", shape = input_shape)

    # we build the model
    embedding_model = build_embedding_model(
        input=input_a,
        num_dense_layers=num_dense_layers,
        embedding_size=embedding_size,
        name='a'
    )

    # we load the weights into the model by name
    embedding_model.load_weights(path_to_siamese, by_name=True)

    return embedding_model
