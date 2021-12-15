# nlp_simple_qa
**CS 6320 Natural Language Processing Class Project**

## Authors
|        Developer        | GitHub                                         |
|:-----------------------:|------------------------------------------------|
|    Prajjwal Bhargava    |   [@prajjwal1](https://github.com/prajjwal1)   |
|        Caleb Hoff       | [@CrunchyCat](https://github.com/CrunchyCat)   |

## Setup
### Dependencies
1. This project requires installation of Pytorch. If you've a CUDA compatible GPU, install the GPU version of Pytorch, otherwise CPU.
For installation instructions, head over to [pytorch.org](https://pytorch.org).

1. This project requires installation of Solr.
For installation instructions, head over to [solr.apache.org](https://solr.apache.org/downloads.html).

1. The rest of the dependencies can be installed with `pip3 install -r requirements.txt`.

> Be sure to have Solr running & properly configured, use `solr e -schemaless`

> When you're done, you can stop the solr using `solr stop -all`

## Use
To run the program on sample data and compute accuracy, run
For task 1
```
$ python3 main.py --task_id 1
```
For task 2
```
$ python3 main.py --task_id 2
```
It will print out all the statistics

For task 3
```
$ python3 main.py --task_id 3 --file_path sample_test.txt
```
