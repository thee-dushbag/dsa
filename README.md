# <u>dsa</u><sub><sub>✨</sub></sub>

![DSA][dsa_picture]

### Introduction.
This __repository's__ intent is to learn _Data Structures_ and _Algorithms_ (**DSA**). I'm using [Programiz][programiz] as my guide in this jungle. Basic algorithm analysis will be part of this project.

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
- __Python__ - for quick implementations.
- __Markdown__ - for documentation.

### Project Structure.
This project is divided into three parts.
- [Data Structures][data_structures]
- [Algorithms][algorithms]
- [Extras][extras]

The `extras` part is meant for algorithms that are more advanced and mathematical.

### Naming.
For all data structures an algorithms implementations, the naming for their respective files will done using the template `{dsa_name}.{lang_extension}` where `dsa_name` is the name of the dsa implementation and `lang_extension` shows in which language the implementation is in. Example: for the merge sort algorithm implemented in python, the file name will be `merge_sort.py`.

All code will be divided into two parts, a `test` file containing the testable imlementation of an algorithm and a `logic source` file containg the actual implementation of the dsa. Python tests will be done using pytest.

The test file will be named `main.(py|cpp|c)` while the dsa logic files for `c/c++` will be stored in an include folder and for `py`, a package for that `part` will be created to hold all the different implementations.

The actual testing will be done in different functions in the `test` file.

###### <u>_Disclaimer._</u>
__*These data structures and algorithms are neither meant to be most efficient nor production ready, they are simply my gateway into more efficient problem solving techniques and code design.*__

[programiz]: https://www.programiz.com/dsa
[dsa_picture]: ./assets/dsa-intro-picture.jpg
[data_structures]: ./dsa/index.md
[algorithms]: ./algo/index.md
[extras]: ./extras/index.md
