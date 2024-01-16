### Traffic project for CS50ai!

It's my first time experimenting with Tensroflow and that's why I ended up trying a lot of different things and configurations for my neural network to make it very accurate but also fast to train, althought basic stuff was what worked the best for me at the end of the day. 

The fist thing I tried is something not that interesting but I found it useful to add a layer that does the rescaling for me: 
"model.add(tf.keras.layers.experimental.preprocessing.Rescaling(scale=1.0 / 255, input_shape=(30, 30, 3))"
this just helps with the rescaling of the values for each pixel instead of doing it "manually" as in the lecture. This should give the same results as just rescaling the input before passing it to the model. Without rescaling these values the accuracy of the model is like 15% less than the accuracy with rescaling (at least for my final neural network).

Then I experimented a little with the convolution layer, I started with 32 kernels because, apparently, it's common practice to use multiple of 8 number of kernels so then i tried to use something different than that (like 25 or 40) and it didn't really change a lot the accuracy or the time it took to train the model. After that I tried more kernels (64) and it got me the best results in terms of accuracy but now it would take like 25 seconds for each epoch so I went back to 32. At the end I gave a try to just 16 kernels and it was almost as accurate as the model with 32 but with less time to train.

With pooling i just try a couple different things (min and average pooling) but it gave me similar results to the max pooling.
To avoid overfitting I first wanted to use L2 regularization by adding ", kernel_regularizer=tf.keras.regularizers.l2(0.01)" to the last couple layers but it didn't give me good results for accuracy so I ended up going back to Dropout.
For the hidden layers I started with 128 nodes in one layer and it worked well but with 64 it gave me similar results with a bit less training time, later i added another layer with 64 nodes and it didn't really changed a lot.
For the final layer I just tried a couple different activation functions but they will give me similar results