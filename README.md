# neuro/tensor datatype validator

Brainlife uses this code to validate and normalize input datasets uploaded by users to make sure that the content and format of the data matches the specified Brainlife datatype.

Currently this App performs following checks

* check that FA, MD, RD, and AD are available.
* check dimensions of nifti files.

This service is not meant to be executed outside Brainlife.

### Authors
- Javier Guaje (jrguajeg@iu.edu)
- Soichi Hayashi (hayashis@iu.edu)

### Project directors
- Franco Pestilli (franpest@indiana.edu)

### Funding 
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
