**Seam Carver implementation in Python**

This project was made for a contest for a college course (not a coding competition; it was based around math applications).

I made the API for graphs at first for a course I took on summer vacation, took the chance when I saw that this was one of the proposed ideas, and improved on it.
As expected, most of the time I worked on optimizing the code.

**Seam Carving**

This is a method for image compression; it uses graphs to find a'seam' or a shortest path from a source node in a graph to its sink node, the shortest path, as in the path with the least significance in the image, which can be removed without too much difference made. It is a lossy type in image compression methods.

**Graphs**

A linear algebra application used in many popular laws, such as Kirchoff's, it is used to perform calculations on matrices that represent circuits, for example.
In CS, they are used in many algorithms, and in fields such as image processing, we typically aim to put them in arrays in a manner we can reach all connected nodes to any node we
access by its index.

![Graph](https://miro.medium.com/v2/resize:fit:1400/0*sNR5Q8ciD79RHYiM.png)
(Taken from Linear Algebra Explained Through Graph Theory, Towards Data Science)


![Graph](https://drive.google.com/file/d/1BaKkWhCj6wMCTCwfrZn6lNyyasxIKga_/view?usp=drive_link)
(Taken from Princeton's Algorithms course, 2nd part)

We will place nodes according to the number of pixels in the image we are working on and connect the top most pixels with the bottom, each node with three under it, while the top most row itself is connected to the source, which counts as our starting point, and the bottom most are all connected to the sink, which is our end.



I used Dijkstra's algorithm to find the shortest path, with the energy difference between two pixels (in both forward and backward seam carving) as the distance between each node. You can find more about it here.

https://www.datacamp.com/tutorial/dijkstra-algorithm-in-python

Lastly, and as expected with Python, I will be explaining some of the optimizations I made:

1. An energy map to calculate the energy between two nodes at the first iteration and preserve it by passing the graph itself with every iteration to a new graph.
2: Only recalculate the energy of nodes that are affected by the removal of the seam.
Finally, I tried to preserve the adjacency list by recalculating the numbers of the graph so the change with width and height would sync with the numbers of the nodes; however, this did not seem to be of any benefit, so I kept the code for it unused.

After all this, the results were no where as good as vectorized implementations; after all, this was not a coding implementation, so time and optimization were just a matter of me being stubborn (not like we got a high rank at the end anyway (for reasons unrelated to the code).

**Benchmarks**

To give you an idea of how much it takes with images, here are some images we took; all were taken in Cairo University, in the faculty of engineering's campus in Cairo.

![Zed](https://drive.google.com/file/d/1E8LhCVH9fOmvRreTyR-CMBnziKu2vcdm/view?usp=drive_link)

![Zedb](https://drive.google.com/file/d/19a87qHgHn03COnGTEO7fT3Cbb8WwVXPC/view?usp=drive_link)
Backwards energy.

![Zedf](https://drive.google.com/file/d/17ledPLNGAw1x28qitv15f3vSOWylc_j_/view?usp=drive_link)
Forwards energy.

**Forward** Took 23 min and 6 sec aprox.
**Backward** Took 10 min and 6 sec.


The original image was 1305 x 593, both carved 300 times vertically.


![trial2](https://github.com/user-attachments/assets/b8f1040d-4006-492d-a087-e465c747982c)

![4b(9,09,16)250](https://github.com/user-attachments/assets/38e95e75-d38b-4f8b-b8a1-c15c99a64be7)
Backwards energy.

![4f(20,27,28)250](https://github.com/user-attachments/assets/3e5f665b-d87c-4a30-b7c5-b9ac57c536f9)
Forwards energy.

**Forward** Took 20 min and 27 sec.
**Backward** It took 9 minutes and 9 seconds.


The original image was 1080 x 810, both carved 250 times horizontally.


The following image was not taken on campus; I found it in another implementation for seam carving.


![rain](https://github.com/user-attachments/assets/ce97fe88-ed7b-48cf-a804-e92888bab07c)

With our energy table, I can easily modify the energy to make them so high the algorithm will never include them or so low they will be removed instantly.
Here's one where I make a part high energy.


![photo_2023-11-14_16-44-05](https://github.com/user-attachments/assets/284528e7-9376-4269-9377-45f0332078a4)


Here's one where I made the ball low energy.

![trial9](https://github.com/user-attachments/assets/a99d8cf6-3c5d-4950-9902-8041d5cc8bc9)


![10f(2,23,15,4)800](https://github.com/user-attachments/assets/f8f06f80-a16b-40d4-a43f-089cb849fb45)

(It took 2 hours, 23 minutes, and 15 seconds to remove 800 seams from this 1600 x 1200 image. **Ouch**)

