from models.model_building import build_embedding_model, build_siamese_model
import tensorflow.keras.layers as layers
from models.difference_layer import DifferenceLayer
from tensorflow.keras.models import load_model
import tensorflow_hub as hub
import numpy as np
import tensorflow as tf

# for loading the siamese model

def load_siamese_model(
    from_outputs_layer,
    path=''
  ):
  """
  For loading the model while indicating the custom layer we made.
  """
  if from_outputs_layer:
    if not path:
      path = 'results/outputs_layers/best_model.npy'
    # we build the model
    model = build_siamese_model(
      inputs_shape=(),
      num_dense_layers=0,
      embedding_size=0
    )
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=[tf.keras.metrics.Precision()])
    # then load the outputs layer into it
    model = load_outputs_layer(model, path)

  else:
    if not path:
      path = 'results/models/best_model.h5'
    model = load_model(path, custom_objects={
      'DifferenceLayer': DifferenceLayer,
      'KerasLayer': hub.KerasLayer
    })
  return model


# for loading a submodel

def load_embedding_model(
    num_dense_layers,
    embedding_size,
    from_outputs_layer,
    path_to_siamese='results/models/best_model.h5'
    ):
    """
    Loads the siamese model and extracts the trained embedding model.
    """
    siamese_model = load_siamese_model(from_outputs_layer, path_to_siamese)

    # we get the inputs shape of one submodel from that of the siamese model
    inputs_shape = siamese_model.inputs_shape[0][1:]
    inputs_a = layers.inputs(name="inputs_a", shape = inputs_shape)

    # we build the model
    embedding_model = build_embedding_model(
        inputs=inputs_a,
        num_dense_layers=num_dense_layers,
        embedding_size=embedding_size,
        name='a'
    )

    # we load the weights into the model by name
    embedding_model.load_weights(path_to_siamese, by_name=True)

    return embedding_model

def save_outputs_layer(model, name):
    # we get the last layer's weights and save them
    outputs_weights = model.layers[-1].get_weights()
    np.save(name, outputs_weights)

def load_outputs_layer(model, name):
    #we set the last layer's weights from the saved file
    outputs_weights = np.load(name,  allow_pickle=True)
    model.layers[-1].set_weights(outputs_weights)

    return model