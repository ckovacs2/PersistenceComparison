# Process
Establish birth-death pairs from data for each Homology class. 

## Landscapes
- Compute landscapes from the birth-death pairs
- Suppose there are $N$ persistence diagrams. Then for the $i$-th landscape function, concatenate each $i$th landscape functions for all $N$ persistence diagrams as $\lambda_{i, 1:N}$.
- Each peak and point that lies on the x-axis is then formed as an array as $y_{i, 1:N}^{1:|b_i|}$ where $|b_i|$ is the number of distinct birth times for the $i$-th landscape.

## Images
- For each birth-death pair, subtract the birth from the death as $$ T(b_i, d_i) = (b_i, d_i-b_i) = (b_i, p_i)$$ which transforms the persistence diagram from the birth-death coordinates to birth-lifetime coordinates. 
- We can define a kernel and weighting for each persistence image as well.
- For the $k$-th persistence diagram, $I_{i,j}^k$ denotes the $i,j$-th pixel of the image and flatten the image into a 1-dimensional vector. 
- If there are $N$ persistence diagrams, then we will produce a matrix of size $(N, n_x\times n_y)$ where $n_x$ and $n_y$ denotes the number of pixels of the persistence image. 