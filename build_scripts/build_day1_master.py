import json, copy, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_nb(name):
    with open(f"{REPO}/{name}") as f:
        return json.load(f)


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": text.splitlines(keepends=True)}


def reset_cells(module_num):
    """A clean-slate boundary between modules. Each module notebook already
    re-imports and re-loads everything it needs from scratch (verified: mod1-4
    all do this in their own first code cell), so clearing the namespace here
    is safe. Several variable names (img, img_gray, props, ptf, ...) are
    reused across modules; without this, rerunning an earlier module's cells
    out of order could leave stale values that a later module silently picks
    up instead of erroring."""
    return [
        md(f"*Starting Module {module_num} fresh: the cell below clears all "
           f"variables from the previous module before continuing, matching "
           f"how these notebooks behaved when run standalone in their own kernel.*"),
        code("%reset -f"),
    ]


HEADER_RE = re.compile(r"^(#+)(\s+)(.*)$")


def tag_module_headers(cells, module_num):
    """Prepend 'Module N – ' to every markdown heading that doesn't already
    say 'Module' in it, so a heading is self-explanatory out of context.
    Only touches heading lines; leaves all other cell content untouched.
    Mutates in-memory copies only -- never written back to the source
    module notebooks on disk."""
    for cell in cells:
        if cell["cell_type"] != "markdown":
            continue
        new_source = []
        for line in cell["source"]:
            has_newline = line.endswith("\n")
            body = line[:-1] if has_newline else line
            m = HEADER_RE.match(body)
            if m and "module" not in m.group(3).lower():
                hashes, space, text = m.groups()
                line = f"{hashes}{space}Module {module_num} – {text}"
                if has_newline:
                    line += "\n"
            new_source.append(line)
        cell["source"] = new_source


def drop_empty_cells(cells):
    """Drop cells with no content at all (blank trailing cells left over in
    the source notebooks). There's no lesson substance to preserve in an
    empty cell, so this doesn't touch lesson content."""
    return [c for c in cells if "".join(c["source"]).strip() != ""]


nb_template = load_nb("mod1_image_manipulation.ipynb")  # for nbformat/metadata
mod1 = load_nb("mod1_image_manipulation.ipynb")["cells"]
mod2 = load_nb("mod2_region_finding.ipynb")["cells"]
mod3 = load_nb("mod3_feature_extraction.ipynb")["cells"]
mod4 = load_nb("mod4_ensemble_margin.ipynb")["cells"]

mod1 = drop_empty_cells(mod1)
mod2 = drop_empty_cells(mod2)
mod3 = drop_empty_cells(mod3)
mod4 = drop_empty_cells(mod4)

tag_module_headers(mod1, 1)
tag_module_headers(mod2, 2)
tag_module_headers(mod3, 3)
tag_module_headers(mod4, 4)

cells = []

# ====================================================================
# TITLE
# ====================================================================
cells.append(md("""\
# Computer Vision Workshop — Day 1

### Image processing → ensemble & margin classifiers

Over the next two days we'll go from raw pixels to trained classifiers, using plankton imagery from
the [Scripps Plankton Camera System](https://aslopubs.onlinelibrary.wiley.com/doi/full/10.1002/lom3.10394)
and [ZooScan](https://sites.google.com/view/piqv/), plus a terrestrial dataset
([Ohio Small Animals](https://lila.science/datasets/ohio-small-animals/)) later in the course.
"""))

cells.append(md("""\
## Getting started on the DSP

1. Connect to the NOC VPN
2. Open the DSP JupyterHub: [notebooks.noc.ac.uk/hub/spawn](https://notebooks.noc.ac.uk/hub/spawn)
3. From the Launcher, open a **Terminal**
"""))

cells.append(md("""\
## Clone the workshop materials

In the terminal:

> ```bash
> mkdir workshops
> cd workshops
> git clone https://github.com/NOC-OI/computer-vision-workshop.git
> cd computer-vision-workshop
> ```
"""))

cells.append(md("""\
## Set up the environment

Still in the `computer-vision-workshop` folder:

> ```bash
> conda env create -n cv-workshop -f environment.yaml
> ```

> ```bash
> python -m ipykernel install --user --name cv-workshop
> ```

- Takes a few minutes
- The `cv-workshop` kernel then appears in your Jupyter Launcher — select it for this notebook
"""))

cells.append(md("""\
## How this notebook works

- Presentation sections (like this one) give context. Code + exercise sections are the hands-on
  modules — unchanged from the standalone module notebooks.
- Run code cells with **Shift+Enter**.
- Code cells have a grey background; output appears directly below.
- Some exercises give you pseudo-code scaffolding to fill in yourself.
"""))

cells.append(md("""\
## Today's plan — "classical" computer vision

1. Image manipulation
2. Region finding (segmentation)
3. Feature extraction
4. Ensemble and margin classifiers

Each stage builds on the last, leading up to classifying an object from an image.
"""))

# ====================================================================
# WHAT IS COMPUTER VISION (from intro_talk)
# ====================================================================
cells.append(md("""\
## What is computer vision?

- A subfield of AI: teach a computer to understand 2D data
- Called "vision" mostly because images are the common test case

**In scope for this workshop:**
- Supervised classification
- Feature selection
- Ensemble / margin classifiers
- Convolutional neural networks

**Out of scope:**
- Dataset construction & annotation best practices
- Unsupervised models
- Generative AI
"""))

cells.append(md("""\
## A few common computer vision tasks

- **Classification** — assign a single label to an image ("what is this?")
- **Object detection** — locate and label multiple objects within an image
- **Segmentation** — classify an image down to the pixel level

The same image can have many valid labels depending on the task: a photo of a giraffe could be
*giraffe*, *animal*, *outdoors*, or *Southern giraffe* — depending on what the classifier was built
to do.
"""))

cells.append(md("""\
## Classification, in practice

<img src="assets/slides/intro/classification_giraffe.jpg" width="420" alt="A giraffe looking directly at the camera">

*Giraffe? Animal? Outdoors? Southern giraffe? All correct — it depends on the task.*
"""))

cells.append(md("""\
## Segmentation, in practice

<img src="assets/slides/intro/segmentation_horse.png" width="600" alt="A photo of a running horse next to its pixel-level segmentation mask">

*Classifying every pixel: "horse" vs. "not horse."*
"""))

cells.append(md("""\
## Where computer vision shows up in ocean science

- **Acoustics** — classifying humpback whale vocalizations from spectrogram "images" (Google AI, 2018)
- **Imaging** — counting and identifying marine organisms from towed-camera and UAV imagery
  (Orenstein et al., 2025)
- **Ecology** — species identification from field photos, e.g. BioCLIP (Stevens et al., 2024, CVPR)
"""))

cells.append(md("""\
## Acoustics as images

<img src="assets/slides/intro/acoustics_spectrogram.png" width="620" alt="Spectrograms of humpback whale calls with a detected call highlighted in yellow">

*A spectrogram is just an image — the same CV tools apply (Google AI, 2018).*
"""))

cells.append(md("""\
## Detecting and segmenting marine organisms

<img src="assets/slides/intro/ocean_imaging_orenstein2025.jpg" width="700" alt="Four underwater imaging examples: benthic organism segmentation, deep-sea object detection, fish detection near a wreck, and jellyfish segmentation">

*Detection and segmentation across imaging platforms — benthic habitat, deep sea, wrecks, midwater
(Orenstein et al., 2025).*
"""))

cells.append(md("""\
## Species ID from field photos

<img src="assets/slides/intro/ecological_imaging_bioclip.jpg" width="620" alt="A plankton image alongside a bar chart of BioCLIP's predicted class probabilities, topped by Ciliate mix">

*BioCLIP's top prediction for this plankton image (Stevens et al., 2024, CVPR).*
"""))

cells.append(md("""\
## How do we produce a model?
"""))

cells.append(md("""\
### High-level steps to train a supervised CV model

1. Define the problem you want to solve
2. Find labeled data
3. Choose an architecture (model type) and a framework (software library)
4. Download model weights (if not training from scratch)
5. Split your data into training and validation sets
6. Train
7. Test, measure performance, and keep evaluating over time
"""))

cells.append(md("""\
### Choosing an architecture and framework

- Larger architectures take longer to train and run — budget can rule some out
- A good starting point: whatever a similar published problem used
- Normal to try several architectures in parallel and compare
- Framework choice is often constrained by:
  - What your collaborators use
  - What your chosen architecture supports
  - Which documentation "clicks" for you
"""))

cells.append(md("""\
### What we'll focus on

**Today — classical machine learning:** hand-engineered features feeding **ensemble or margin
classifiers**.

- **Training:** draw features from labeled images, fit a classifier
- **Testing:** draw the same features from unseen images, check performance

**Tomorrow — convolutional neural networks:** learn features directly from images instead.
"""))

cells.append(md("""\
### A first look: convolutional neural networks

- Learn features directly from labeled images — no hand-engineering
- Simplest architectures are a series of filters
- Filter shapes and weights are learned during training
- Require input images to all be the same size

<img src="assets/slides/intro/cnn_diagram.png" width="700" alt="Diagram of a CNN: a copepod image passing through several convolutional feature-map layers narrowing toward an output">
"""))

cells.append(md("""\
### A word of caution: distribution shift

Every automated classifier assumes training and test data are drawn from the same distribution.
In practice, that's hard to guarantee:

- Organism distributions can change over time or space
- New classes (or noise) can appear; others can disappear
- Different instruments and conditions behave differently

Keep this in mind as we build and evaluate classifiers: how you split data, what counts as
"success," and how you'd notice a model has failed are all open questions we'll return to.
"""))

cells.append(md("""\
### Distribution shift, in practice

A ResNet classifier's counts of one plankton class, plotted against manual counts of the same
samples over three years:

<img src="assets/slides/intro/distribution_shift_example.png" width="560" alt="Plot of prevalence over time for a plankton class, comparing a ResNet classifier to manual counts, with a red box highlighting a period where they diverge">

- For most of the time series — including a bloom peak in mid-2016 — the model tracks the manual
  counts closely
- In late 2017 (red boxes), the model starts consistently over-counting relative to the manual
  count
- The cause: novel-looking objects (inset photos) that resemble the target class closely enough to
  fool a model trained on the earlier distribution

(Orenstein et al., 2020)
"""))

# ====================================================================
# IMAGE PROCESSING INTRO (general, day1 slides 4-11)
# ====================================================================
cells.append(md("""\
## Modules 1–3: image processing & computer vision

Image processing is a subfield of signal processing that treats an image as a 2D signal:

- **Manipulation** — resizing, warping, other transforms (Module 1)
- **Filtering** — edge detection, region finding (Modules 2–3)

Many Photoshop-style features are built on exactly these ideas.
"""))

cells.append(md("""\
## Further reading

- *Digital Image Processing*, 4th ed. — Gonzalez & Woods (Pearson)
- *Computer Vision: A Modern Approach*, 2nd ed. — Forsyth & Ponce (Pearson)
- *Computer Vision: Algorithms and Applications* — Szeliski (Springer), free at
  [szeliski.org/Book](http://szeliski.org/Book/)
"""))

# ====================================================================
# MODULE 1
# ====================================================================
cells.append(md("""\
# 📘 Module 1: Image manipulation

**Goals:**
- Get comfortable manipulating images in Python
- Learn a few common image transformations
- Understand how transformations subtly change an image's appearance — this matters again later,
  once we feed images into deep nets
"""))

cells.append(md("""\
## Images are matrices of values

- A digital image is a matrix of numbers
- In an 8-bit gray scale image, each pixel's value (its "gray level") ranges from 0 (black) to
  255 (white)
- Some sensors have greater bit depth and represent gray levels more precisely

<img src="assets/slides/day1/gray_level_ramp.png" width="380" alt="Gray level ramp from 0 (black) to 255 (white)">
"""))

cells.append(md("""\
## Color images are 3D matrices

- One 2D layer ("channel") per color
- Each channel on its own is just a gray scale image

<img src="assets/slides/day1/channel_all_split_mod1_s23.png" width="620" alt="An RGB plankton image (928, 1736, 3) split into separate Red, Green, and Blue channels, each (928, 1736)">
"""))

cells.append(md("""\
## Affine transforms

Most transforms in this module are **affine transforms**: 2D transforms that map a pixel at one
point to another, while preserving parallel lines in the image.

- Translation
- Rotation
- Resizing (scaling)
- Warping
"""))

cells.append(md("""\
## The transform equation

Every affine transform can be written as the same matrix equation:

$$\\begin{bmatrix} x_{new} \\\\ y_{new} \\end{bmatrix} = A \\times \\begin{bmatrix} x_{orig} \\\\ y_{orig} \\end{bmatrix} + B$$

- $A$ and $B$ take different forms depending on the transform
- e.g. $A$ = identity matrix, $B$ = a constant offset → pure translation

[Further reading on affine transforms](https://homepages.inf.ed.ac.uk/rbf/HIPR2/affine.htm)
"""))

cells.append(md("""\
## Perspective transforms

- More general than affine transforms
- Preserve straight lines, but *not* parallel ones
- Can digitally mimic the effect of zooming
- Covered at the end of this module

[Further reading on perspective warps](http://alumni.media.mit.edu/~maov/classes/comp_photo_vision08f/lect/08_image_warps.pdf)
"""))

cells.append(md("""\
The module below covers pixel indexing, gray scale conversion, and all of these transforms in
code — you'll need them later for data augmentation.

---
"""))
cells.extend(mod1)

# ====================================================================
# MODULE 2
# ====================================================================
cells.append(md("""\
# 📘 Module 2: Segmentation and region finding

Segmentation selects the objects of interest out of a full frame.

- **Uniform background** (e.g. plankton microscopy) — comparatively easy
- **Structured background** (e.g. benthic habitat) — far more complex, still an active research
  problem
"""))

cells.append(md("""\
## Filtering as convolution

A small kernel slides across the image; each position's output is a weighted combination of the
pixels underneath it.

<img src="assets/slides/day1/convolution_filter.gif" width="420" alt="Animation of a 3x3 mean filter kernel sliding across an image and producing one output value per position">

*Courtesy of University of Calgary.*
"""))

cells.append(md("""\
## Morphological clean-up

A structuring element sweeps over the mask; any pixel it touches gets added to the foreground —
one of the "clean-up" steps used after thresholding.

<img src="assets/slides/day1/dilation_animation.gif" width="300" alt="Animation of morphological dilation: a cross-shaped structuring element sweeping over a grid, adding a pixel wherever it touches an existing foreground pixel">

*Dilation, using a cross-shaped structuring element. Courtesy: Poonam Kshirsagar.*
"""))

cells.append(md("""\
## Module 2 – When backgrounds get complicated

Structured backgrounds — benthic habitat imagery is the classic example — break the simple
threshold-and-clean pipeline.

<img src="assets/slides/day1/benthic_coral_example.png" width="420" alt="Underwater photo of a structured coral reef habitat, illustrating a complex segmentation background">

*No single threshold separates "coral" from "not coral" here (Steffens et al., 2019).*
"""))

cells.append(md("""\
## Strategies for complex backgrounds

- **Point annotation** — randomly sample points, classify a small neighborhood around each to
  estimate coverage (e.g. [CoralNet](https://coralnet.ucsd.edu/); Steffens et al., 2019)
- **Stereo image pairs** — fully automated segmentation (King et al., 2018), though even the best
  method only got ~66% of pixels correct across all classes
- **[deep-segments](https://github.com/andrewcking/deep-segments)** — King et al.'s tool using ML
  to speed up human ground-truthing
"""))

cells.append(md("""\
## How well does automated segmentation work?

<img src="assets/slides/day1/king_et_al_segmentation.png" width="700" alt="Comparison of ground truth coral segmentation against FCN8s, Dilation8, DilationMod, and DeepLab v2 automated methods">

*Ground truth vs. four automated methods on the same benthic image (King et al., 2018) — even the
best only partially agrees with ground truth.*

---
"""))
cells.extend(reset_cells(2))
cells.extend(mod2)

# ====================================================================
# MODULE 3
# ====================================================================
cells.append(md("""\
# 📘 Module 3: Feature extraction

- Once objects are selected, we collect measurements about them
- A form of **dimensionality reduction**: thousands of raw pixels → a compact vector of metrics,
  `[x1, x2, x3, ...]`
- Which metrics work best takes trial and error
"""))

cells.append(md("""\
## Morphological features

Shape information: major axis, minor axis, equivalent spherical diameter, solidity, Hu moments...

<img src="assets/slides/day1/morphology_axes.png" width="500" alt="A copepod with its major axis drawn as a line and equivalent spherical diameter drawn as a circle of the same area">

*Major axis (line) and equivalent spherical diameter — a circle with the same area as the region
(green).*
"""))

cells.append(md("""\
## Texture features: GLCM

The Gray Level Co-occurrence Matrix summarizes how often pairs of pixel values co-occur at a given
angle and distance.

<img src="assets/slides/day1/glcm_angles.png" width="320" alt="Diagram of the eight GLCM angles (0-315 degrees) radiating from a central pixel">
"""))

cells.append(md("""\
## From one region to a feature matrix

- Each region → a vector of numbers
- Do this for every region, across every image → a feature **matrix** (rows = images, columns =
  features)
- This is exactly the input Module 4's classifiers expect

<img src="assets/slides/day1/feature_matrix.png" width="620" alt="Several organism images each mapped to a row of a feature matrix, indexed by image (rows) and feature (columns)">

---
"""))
cells.extend(reset_cells(3))
cells.extend(mod3)

# ====================================================================
# MODULE 4
# ====================================================================
cells.append(md("""\
# 📘 Module 4: Ensemble and margin classifiers

Finally — machine learning! Using the metrics from Module 3, we'll train two types of classifiers:

- **Support Vector Machine** (a *margin* classifier)
- **Random Forest** (an *ensemble* classifier)

*(Further reading: Pattern Classification, 3rd ed. — Duda, Hart & Stork, Wiley-Interscience.)*
"""))

cells.append(md("""\
## Module 4 – Building intuition: fruit fly or porcupine?

Imagine classifying images into porcupine, fruit fly, or fish:

<img src="assets/slides/day1/trio_porcupine_fly_fish.jpg" width="700" alt="A porcupine, a close-up of a fruit fly's head, and a pufferfish, side by side">

What could we measure about each image that would help tell them apart?
"""))

cells.append(md("""\
## One feature: eye size relative to body

Plot a histogram of this feature across many labeled images. For two classes, a single dividing
line does a reasonable job:

<img src="assets/slides/day1/histogram_2class.png" width="420" alt="Histogram of porcupine and fruit fly images by eye-to-body-size ratio, showing two separable peaks">
"""))

cells.append(md("""\
## Adding a third class breaks it

<img src="assets/slides/day1/histogram_3class.png" width="420" alt="Histogram of porcupine, fruit fly, and fish images by eye-to-body-size ratio, showing three overlapping peaks that a single threshold cannot separate">

One feature — and even one dividing line — is no longer enough.
"""))

cells.append(md("""\
## Two features: a 2D feature space

Module 3 gave us many features, not just one. Add a second (say, *shape*), and each image becomes
a point in 2D space:

<img src="assets/slides/day1/feature_space_scatter.png" width="480" alt="Scatter plot of porcupine, fruit fly, and fish images plotted by shape versus eye-to-body size ratio, forming three separable clusters">

Now we can draw lines — or in higher dimensions, hyperplanes — that separate the classes. That's
exactly what both classifiers below do, using every feature Module 3 extracted, not just two.
"""))

cells.append(md("""\
The module below fits each classifier (support vector machine, then random forest) using
`sklearn`, including how to read a confusion matrix and where each one tends to get confused.

---
"""))
cells.extend(reset_cells(4))
cells.extend(mod4[:27])  # data prep + SVM + the "Ensemble classifiers" theory cell

# ------------------------------------------------------------------
# Module 4 - supplementary diagram right after the notebook introduces
# random forests, since the notebook doesn't otherwise include one
# ------------------------------------------------------------------
cells.append(md("""\
<img src="assets/slides/day1/random_forest_diagram.png" width="600" alt="Diagram of a random forest: many decision trees each vote a class, combined by majority vote into a final class">
"""))
cells.extend(mod4[27:])

# ====================================================================
# Assemble notebook
# ====================================================================
nb_out = copy.deepcopy(nb_template)
nb_out["cells"] = cells

with open(f"{REPO}/day1_master.ipynb", "w") as f:
    json.dump(nb_out, f, indent=1)

print(f"day1_master.ipynb written with {len(cells)} cells")
