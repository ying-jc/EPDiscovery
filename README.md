# EPDiscovery
A stacking-based ensemble classifier for the discovery of prokaryotic efflux proteins from sequence information

## Installation  
Clone EPDiscovery by  
```
$ git clone https://github.com/ying-jc/EPDiscovery.git
```  
or
Download EPDiscovery (ZIP file), move it to a directory where the user wants it installed, and uncompress it.

## Requirements  
EPDiscovery is an open-source Python-based tool, which operates depending on the Python environment. Currently, EPDiscovery has only been tested on the Linux system with Python version 3.9.18. Before running EPDiscovery, the user should make sure all the following packages are installed in their Python environment: click, joblib, numpy, pandas, and scikit-learn. These packages can be easily installed using pip by
```
$ pip install -r requirements.txt
```
In addition, since EPDiscovery makes predictions based on the results of iFeature program, it is also necessary to install [iFeature](https://github.com/Superzchen/iFeature "iFeature") and meet its operational requirements.

## Usage  
### Options  
For details of all options, run:  
```
$ python EPDiscovery.py --help

Usage: EPDiscovery.py [OPTIONS]

  EPDiscovery: A stacking-based ensemble classifier for the discovery of
  prokaryotic efflux proteins from sequence information

Options:
  --conf TEXT              Configuration file in plain text format. (Required)

  --seq TEXT               Protein sequence file in fasta format. (Required)

  --cutoff FLOAT RANGE     Cutoff value for binary classification. [Default:
                           0.672] (Optional)  [0<=x<=1]

  --n_proc INTEGER RANGE   Number of processes used for feature extraction.
                           [Default: 1] (Optional)  [x>=1]

  --terminal [True|False]  Output result to the terminal. [Default: True]
                           (Optional)

  --out TEXT               The name of the output file in tab-delimited text
                           format. (Optional)

  --help                   Show this message and exit.
```  

### Notes  
#### Sequence of input
The input to EPDiscovery can be any number of protein sequences in FASTA format. The sequence must not contain the blurred disabilities (such as "X", "Z", "B", "J", "O", "U", and "*"), and the length must be greater than 30aa.

#### Result of output
EPDiscovery outputs the results to the terminal by default. The user can specify the name of the output file to save the results to a CSV file. In the results, the first column represents the sequence name, the second column represents the estimated probability of an efflux protein for the corresponding sequence, and the third column represents the classification according to the provided cutoff value.

#### Configuration file
The configuration file must be specified to tell the EPDiscovery where the iFeature and classifiers are located. A template of the configuration file can be found in the directory of EPDiscovery.

#### Number of processes
Increasing the number of processes can effectively shorten the running time of feature extraction. 

## An example  
All files in the commands can be found in the directory of EPDiscovery.  
* Set up the configuration file.

* Locate to the example folder:
```
$ cd EPDiscovery/example
```
* Run the following command to predict the sequences in the example with the default settings:
```
$ python ../EPDiscovery.py --conf ../config.txt --seq example.fa
```
Note that if the user is not running the program under the EPDiscovery folder, the path to EPDiscovery.py and config.txt needs to be provided.

## Citation  
A stacking-based ensemble classifier for the discovery of prokaryotic efflux proteins from sequence information. (Under review)
