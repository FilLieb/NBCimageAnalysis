# image analysis
This project is for students in the Neurobiochemistry Module ([SoSe26] Neurobiochemistry (MN-BC-SM08)) at the University of Cologne.

## overview
In a few days we will take a practical approach and learn basics of microscopy image display and automated image analysis. We will be using OMERO and Python for our approach and get to know key concepts in digital image processing.

## display publication ready microscopy images using Omero
The images you have acquired have been deposited on a server that is hosted by CECAD. To access this server directly from your computer, you need to download the software OMERO.insight, which you can find for your operating system by clicking on the badge below:

[![OMERO](https://img.shields.io/badge/OMERO-Open%20Microscopy-00acac?logo=microscope&logoColor=white)](https://www.openmicroscopy.org/omero/downloads/)

Once the software is downloaded and installed, run the software and you should see something that looks like this:

![Data pipeline overview](data/assets/omero_setup.png)


When you click on the wrench symbol (see above highlighted in yellow) add the following server name: omero-1.cecad.uni-koeln.de

Afterwards attempt to login using your uniKIM credentials. I will manually add ypu to the Neurobiochemistry Course and you will have access to your data from the confocal microscope sessions.

You can access the Omero webclient directly in your browser by clicking on the badge below:

[![OMERO](https://img.shields.io/badge/OMERO%20webclient-00acac?logo=microscope&logoColor=white)](https://omero.cecad.uni-koeln.de/webclient/login)

## notebooks
| # | Notebook | Description | Link |
|---|----------|-------------|------|
| 1 | first notebook  | new to Python? check out these basic functions... | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/FilLieb/NBCimageAnalysis/blob/master/learning/0_first_notebook.ipynb) |
| 2 | images in Python  | load and display images | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/FilLieb/NBCimageAnalysis/blob/master/learning/1_loading_and_display_images_tif.ipynb) |



## requirements
We will be using various packages that have been developed by others. 
