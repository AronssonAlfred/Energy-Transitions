Code for fitting growth models

fitting_log.py - Python code for Logistic growth model fitting

sample_data.csv - source data file for growth model fitting

file_format.txt – description of input and output file formats

When running the Python file, working directory should be set to one containing the respective 
data files (or path to the data file should be included in the Python file).

Modules necessary for running the code are numpy, scipy, and pandas – they should be installed 
on your computer.

Warning: (1) growths rates cannot be reliably estimated  when the inflection point is 
in the future (indicated Maturity < 0.5 - see file_format.txt). 
(2) The code has not been tested for data series starting around or above the inflection 
point (50% of asymptote for Logistic models ). 
Growth model parameters estimates for such data series may be unreliable. 
