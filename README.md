# PM4Sand_driver_auto
## Scripts that produce multiple PM4Sand drivers for different loading paths, batch files for running them in FLAC, and post-processing codes for plotting

### Structure

- Five folder structure
- PM4Sand* folders contain drivers and processing* folder contains post-processing and plotting files
- Each PM4Sand* folder provides the ability to create multiple FLAC *.fis drivers that cover various parameters and are named accordingly. A batch*.fis file is also produced that can be directly called in FLAC that will run them all and produce txts with results in the same folder.
- Each plotting*.py file in the "processing_plotting" folder will process different drivers and produce Figures. Decode python file contains useful functions for all and ucdavis.mplstyle is used for figure styling.

### Driver details
#### PM4Sand_Cyclic_DSS_drained_batch
Produces strain controlled drained Direct Simple Shear drivers. Each driver features five elements, each at a different overburden. User can select relative densities. Options for exercising at a range of strains for a certain number of cycles at each one (will produce Modulus Reduction and Damping curves) or applying uniform cycles at the same shear strains for multiple cycles (will produce volumetric response). This can be controlled by the "volumetric" parameter.

#### PM4Sand_Cyclic_DSS_undrained_batch
Produces stress controlled undrained Direct Simple Shear drivers. Each driver features five elements, each at a different CSR. Middle element is exercised under the CRR of the relative density (set internally in DSS_cyclic_undrained.fis). User can select relative densities, overburdens, static shear stress bias values, and Ko values.

#### PM4Sand_Monotonic_batch
Produces drained and undrained monotonic Direct Simple Shear (DSS) and Plane Strain Compression (PSC) drivers. Each driver features five elements, each at a different overburden. User can select driver type, density, drainage condition.

#### PM4Sand_Reconsolidation_batch
Produces stress controlled undrained Direct Simple Shear drivers. Each driver features five elements, all exercised under the CRR of the relative density (set internally in DSS_cyclic_undrained.fis). Each element reaches a certain strain (that populates the x-axis of the Reconsolidation plot - example figure 4.21 in PM4Sand manual) and is let reconsolidate afterwards.

### Original versions of processing and plotting files created by M-P Kippen in the framework of the PM4Sand3D development

---

Please send your comments, bugs, issues and features to add to [Katerina Ziotopoulou] at katerinaziot@gmail.com.
