# ohnologuous genes parser

#### Output

The aim of this procedure is to retrieve pairs of ohnologuous genes from a Synmap analysis between two of the same genome.

#### Output
### 1- Synmap analysis
The first step is to perform a SynMap analysis (https://genomevolution.org/CoGe/SynMap.pl) and inputing two times the same genome (see SynMap doc). Then download the following file :

![alt text](https://github.com/ndaccord/ohnologuous_genes_parser/blob/master/images/synmap_output.png?raw=true)

### 2- *filter_ohnologuous_genes.py* use

#### Output
This script parses the DAGChainer output in order to retrieve pairs of ohnologuous genes which are inside large enough synteny windows to minimize noise.

#### Output
```bash
python filter_ohnologuous_genes.py input_file output_file min_window_size
```
* **input_file** : the DAGchainer output file shown above
* **output_file** : path to the output file
* **min_window_size** : minimum synteny window size (in **base pairs**) in which genes will be considered. On at least one chromosome, the size of the synteny link has to be superior or equal to this value.

#### Output
The output (**output_file** parameter) is a tab-separated file with the two following columns :
* **1** : first gene of the ohnologuous pair
* **2** : second gene of the ohnologuous pair
