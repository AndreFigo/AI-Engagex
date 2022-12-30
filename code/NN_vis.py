
from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np
from ann_visualizer.visualize import ann_viz
import graphviz







def main():

    lr= 1e-06
    n_actions = 11
    input_dims = (179,)


    # fc1_dims = 256
    # fc2_dims = 256

    # model = Sequential(
    #     [
    #         Dense(fc1_dims, input_shape=(*input_dims,)),
    #         Activation("relu"),
    #         Dense(fc2_dims),
    #         Activation("relu"),
    #         Dense(n_actions),
    #     ]
    # )

    # model.compile(optimizer=Adam(lr=lr), loss="mse")


    fc1_dims = 128
    fc2_dims = 128
    fc3_dims = 128
    fc4_dims = 128

    init = tf.keras.initializers.HeUniform()

    model = Sequential(
        [
            Dense(fc1_dims, input_shape=(*input_dims,), activation = 'relu', kernel_initializer = init),
            Dense(fc2_dims,activation = 'relu', kernel_initializer = init),
            Dense(fc3_dims,activation = 'relu', kernel_initializer = init),
            Dense(fc4_dims, activation = 'relu', kernel_initializer = init),
            Dense(n_actions, kernel_initializer = init)
        ]
    )
    model.compile(optimizer=Adam(lr=lr), loss=tf.keras.losses.Huber())


    ann_viz(model, title="", view=True)
    # graph_file = graphviz.Source.from_file('network.gv')
    # print(graph_file)
    # grapg_file.render('network.gv', view=True)
    



if __name__ == '__main__':
    main()

    # g = graphviz.Source.from_file('network.gv')
    # print(graph_file)
    # graph_file.render('network.gv', format='pdf')
    # g.view()