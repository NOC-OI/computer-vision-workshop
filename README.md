# NOC Computer Vision Workshop
## Sept. 23-25, 2025

Author: Eric Orenstein (National Oceanography Centre)

This set of notebooks is designed to introduce ocean scientists to computer vision tools for working with image and image-like data. The [original material](https://github.com/eor314/pogo_bioobs19_imaging) was developed for the [Partnership for Observing the Global Ocean's](https://oceandecade.org/actions/partnership-for-observation-of-the-global-ocean-pogo/) [2019 Workshop on Machine Learning and Artifical Intelligence in Biological Observations](https://pogo-ocean.org/capacity-development/activity-related-workshop/pogo-workshop-on-machine-learning-and-artificial-intelligence-in-biological-oceanographic-observations/) by [Eric Orenstein](https://eor314.github.io/) and [Simon-Martin Schroder](https://orcid.org/0000-0002-6603-9907) (University of Kiel). 

Participants will learn basic concepts in computer vision, from manipulating individiual images to semantic classification with convolutional neural networks. The material focuses on plankton images collected with the [Scripps Plankton Camera System](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1002/lom3.10394) and the [ZooScan](https://sites.google.com/view/piqv/). Later lessons use the [LILA BC Ohio Small Animals](https://lila.science/datasets/ohio-small-animals/) dataset to introduce the commonly used COCO data format and advanced techniques. Each module treats different, related topics but can be used independent of one another. 

These data sets have all been preloaded on the NOC Data Science Platform (DSP). There are some hard coded file paths that assume you are running the examples on the DSP. 


## Setup instructions

### Configure the Conda Environment

All of the notebooks require you to use the supplied Conda environment. This is pre-installed on the DSP in `/groups/cv-workshop/cv-workshop-env/`. 

### Install the Conda Environment yourself

If you need to install the Conda environment yourself (e.g. if you are not using the DSP) then clone this git repository and run:

`conda create -n cv-workshop -f envrionment.yaml`

#### Installing on a scratch drive on JASMIN

On JASMIN you migth want to install the environment on a scratch drive to avoid using your filestore quota. JASMIN has several scratch filesystems, some are intended for processes which write in parallel and some are intended for processes which don't. You can use the non-parallel version for this environment, this is located in `/work/scratch-nopw2`. 

If you haven't previously used this scratch drive, create a directory for yourself:

`mkdir /work/scratch-nopw2/${USER}`

`conda env create -p /work/scratch-nopw2/${USER}/computer-vision-workshop-env/ -f environment.yaml`

We now have the environment installed, but if we want to use the JASMIN Notebook service we need to tell the notebook service where to find the Conda environment. Running this command will create this link and add a new icon to the Jupyter launcher for the workshop. It should also appear as an option when opening any of the notebooks. 

`conda run -p /work/scratch-nopw2/${USER}/cv-workshop-env/ python -m ipykernel install --user --name computer-vision-workshop`

### Alter the data path in your code

Change `DATASET_PATH` to  `/work/scratch-nopw2/colinsau/cv-workshop/SPC_manual_labels` in `mod5_resnet_feature_extractor.ipynb`.

In `mod6_fine_tuning.ipynb` change `TRAINING_PATH` and `VALIDATION_PATH` to "/work/scratch-nopw2/colinsau/cv-workshop/ZooScan/train"

