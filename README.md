# <u>dsa</u>
![DSA](./assets/dsa-intro-picture.jpg)

### Introduction.
This __repository__ intent is to learn Data Structures and Algorithms (DSA). I'm using [Programiz](https://www.programiz.com/dsa) as my guide in this jungle. Algorithm complexity studies will also be part of this project, this involves.
 - __Time__ Complexity
 - __Space__ Complexity

On top of this, asynptotic notations will be covered and how they vary from algorithm to algorithm.

Extra topics to be covered include dynamic programming and code profiling, it's gonna be a long one.

#### Goal of this project.
- Learn data structures and algorithms.
- Learn how to analyze algorithms and data sturctures in terms of
  - __Time__ complexity
  - __Space__ complexity
- Learn and understand the different measures of DSA, these are
  - __Big-O__ notation
  - __Omega__ notation
  - __Theta__ notation
- Learn more techniques for documentation using markdown
- Learn the basics for code profiling
- Learn how to do benchmarks

### Languages.
Main Languages in this project include:
- __Python__ - for quick implementations.
- __C__ - deeper understanding of safety.
- __C++__ - also for deeper understanding of safety and edge cases.

This means, some algorithms will be implemented in multiple languages simultaneously for contrast from language to language.

### Project Structure.
This project is divided into three parts.
- [Data Structures](./data_structures/index.md)
- [Algorithms](./algorithms/index.md)
- [Extras](./extras/index.md)

The `extras` part is meant for algorithms that are either more advanced or cannot be classified as a data structure or an algorithm.

### Naming.
For all data structures an algorithms implementations, the naming for their respective files will done using the template `{dsa_name}.{lang_extension}` where `dsa_name` is the name of the dsa implementation and `lang_extension` shows in which language the implementation is in. Example: for the merge sort algorithm implemented in python, the file name will be `merge_sort.py`.

All code will be divided into two parts, a `test` file containing the testable imlementation of an algorithm and a `logic source` file containg the actual implementation of the dsa.

The test file will be named `main.(py|cpp|c)` while the dsa logic files for `c/c++` will be stored in an include folder and for `py`, a package for that `part` will be created to hold all the different implementations.

The actual testing will be done in different functions in the `test` file.

#### Disclaimer.
These data structures and algorithms are neither meant to be most efficient nor production ready, they are simply my gateway into more efficient problem solving techniques and code design.
