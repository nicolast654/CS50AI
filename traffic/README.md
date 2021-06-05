# Traffic

I started with the same number and types of layer as the lecture code: 
<ul>
    <li> 1 convolutional layer. Learn 32 filters using a 3x3 kernel</li>
    <li> 1 max-pooling layer with a 2x2 kernel size</li>
    <li> 1 hidden layer with 128 units</li>
    <li> A 0.5 dropout rate</li>
    <li> My output layer is different, to adapt to the number of units required (NUM_CATEGORY, one for each category)</li>
</ul>
---
I have done 15 experiementations, by changing the number of convolutional and pooling layers, the number and size of filters for conolutional layers, the pool size for pool layer, the number and size of hidden layers, and the dropout rate.

Among the 15 experimentations, here are the 8 from which I learned the most:

| Modification  | Accuracy | Loss |
|--------------|------------|---|
| Original from lecture | 0.0553 | 3.4878 |
| Change the max-pooling layer's kernel from 2x2 to 3x3 | 0.056  | 3.5026 |
| Added a second hidden layer with 128 units | 0.8831 | 0.4267 |
| Added another conolutional layer and another max-pooling (same as the 2 first) | 0.7710 | 0.6967 |
| Reduced dropout to 0.3 | 0.9021 | 0.3273 |
| Increased dropout to 0.7 | 0.7456 | 0.7920 |
| Got back dropout to 0.3, and added a third convolutional layer with 16 filters | 0.8929 | 0.3541 |
| Increased the number of filters from 16 to 48 with 3x3 kernel | 0.9523 | 0.2012 |

After trying many other combinations, adding and removing layers, none would go higher than 0.9523 accuracy, my neural network is made of:
<ul>
    <li> Convolutional layer. Learn 32 filters using a 3x3 kernel</li>
    <li> Max-pooling layer, using 3x3 pool size</li>
    <li> Second convolutional layer. Learn 32 filters using a 2x2 kernel</li>
    <li> Max-pooling layer, using 2x2 pool size</li>
    <li> Third convolutional layer. Learn 48 filters using 2x2</li>
    <li> Two hidden layers with 128 units</li>
    <li> A dropout rate of 0.3</li>
    <li> A final output layer with NUM_CATEGORY (43) units</li>
</ul>
