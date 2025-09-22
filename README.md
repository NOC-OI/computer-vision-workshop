# NOC Computer Vision Workshop
## Sept. 23-25, 2025

Author: Eric Orenstein (National Oceanography Centre)

This set of notebooks is designed to introduce ocean scientists to computer vision tools for working with image and image-like data. The [original material](https://github.com/eor314/pogo_bioobs19_imaging) was developed for the [Partnership for Observing the Global Ocean's](https://oceandecade.org/actions/partnership-for-observation-of-the-global-ocean-pogo/) [2019 Workshop on Machine Learning and Artifical Intelligence in Biological Observations](https://pogo-ocean.org/capacity-development/activity-related-workshop/pogo-workshop-on-machine-learning-and-artificial-intelligence-in-biological-oceanographic-observations/) by [Eric Orenstein](https://eor314.github.io/) and [Simon-Martin Schroder](https://orcid.org/0000-0002-6603-9907) (University of Kiel). 

Participants will learn basic concepts in computer vision, from manipulating individiual images to semantic classification with convolutional neural networks. The material focuses on plankton images collected with the [Scripps Plankton Camera System](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1002/lom3.10394) and the [ZooScan](https://sites.google.com/view/piqv/). Later lessons use the [LILA BC Ohio Small Animals](https://lila.science/datasets/ohio-small-animals/) dataset to introduce the commonly used COCO data format and advanced techniques. Each module treats different, related topics but can be used independent of one another. 

The data sets have all been preloaded on the NOC Data Science Platform (DSP). There are some hard coded file paths that assume you are running the examples on the DSP. 

### Environment set up
This set of notebooks uses the compute enviroment described in `environment.yaml`. To [create the environment on the DSP](https://nocacuk.gitlab.io/ocean-informatics/data-science-platform/user-documentation/using-conda.html#), open a terminal from the Launcher and run: 

```
$ conda env create -n <env name> -f new_enviroment.yml
```

to create a new named environment from the configuration file. To make the environment visible to your Jupyter notebooks run: 

```
$ python -m ipykernel install --user --name <your environment name>
```

Within a few minutes, the environment should appear in your Jupyter launcher. 