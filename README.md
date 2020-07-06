# rpRanker

Command line interface of the retrosynthesis and pathway analysis pipeline found in the [Galaxy-SynBioCAD](https://galaxy-synbiocad.org/) platform.

## Getting Started

To run the pipeline, the following projects are required:
- [RetroPath2.0](https://github.com/Galaxy-SynBioCAD/RetroPath2)
- [rp2paths](https://github.com/Galaxy-SynBioCAD/rp2paths)
- [RetroRules](https://github.com/Galaxy-SynBioCAD/RetroRules)
- [rpReader](https://github.com/Galaxy-SynBioCAD/rpReader)
- [rpCofactors](https://github.com/Galaxy-SynBioCAD/rpCofactors)
- [rpThermo](https://github.com/Galaxy-SynBioCAD/rpThermo)
- [rpFBA](https://github.com/Galaxy-SynBioCAD/rpFBA)
- [rpExtractSink](https://github.com/Galaxy-SynBioCAD/rpExtractSink)
- [rpGlobalScore](https://github.com/Galaxy-SynBioCAD/rpGlobalScore)
- [rpReport](https://github.com/Galaxy-SynBioCAD/rpReport)
- [rpVisualiser](https://github.com/Galaxy-SynBioCAD/rpVisualiser)

## Installing

First thing to do is to untar the GEM SBML models files:

```
tar -xf models.tar.xz
```

By default, running any of the scripts will attempt to download the docker images from DockerHub directly. If you would like to build the dockers yourself or change the hardcoded settings, see the next section.

### Build the dockers and changing the default parameters

If you encounter a problem with downloading the DockerHub, then we suggest that you build the images directly on your machine, using the following script:

```
sh build_all.sh
```

WARNING: This will take approximately 35GB of disk space

This will create a folder at the root of the directory, will download the GitHub project and build the dockers in the right order.

Note that the the default hard coded configurations of the tools are the following:
- RetroPath2.0: Maximal RAM usage of 30.0 GB
- RP2paths: Maximal RAM usage of 30.0 GB

To change those default parameters, change line 36 in rpTool.py in the RetroPath2.0 project, and line 23 in rpTool.py in the rp2paths project.

## Running

All these scripts will create a folder with the results of the predictions and/or analysis.

### Deep RetroPath2.0

NOTE: this script is intented to be used for people with limitted computer resourses, that have the time, that do not necessarialy know how to define all the parameters, and that would like to find the highest number of solutions using RetroPath2.0. It would indeed be better to use a larger coputational power with well defined inputs. Furthermore, depending on the target the script may take a few days to execute.

RetroPath2.0 contains a lot of different tweaks and parameterisations, such as:
- Reaction Rules diameters
- TopX solutions kept at each iterations
- Molecular weight filters
- Maximal lenght of the pathways

To the non-experts it, may difficult to know what are the right parameterisation of RetroPath2.0. To this end, the following script is proposed that aids the more novice users of the tool to find solutions for the production of a molecule of interest in E.coli S.Cervisae, P.Putida, B.Subtilis and Y.Lipolityca (these models have been modified to work well with the pipeline). It essentially runs the script reducing the complexity of the required solution when the more complex parameterisation that would require more RAM, or longer execution time that is allowed to find a solution. The maximal length of the pathways is progressively reduced, the TopX is also reduced, the diamters of the rules are reduced and finally different models for a given organism are tested. The user may also set the partial_results flag to return partial results, that is, when the exploration of the network is interupted due to lack of RAM or time, but where some solutions are still found.

```
python deep_rp2.py -inchi "InChI=1S/C6H6O4/c7-5(8)3-1-2-4-6(9)10/h1-4H,(H,7,8)(H,9,10)/b3-1+,4-2+" -organism e_coli
```

### Analysis Pipeline

Once RetroPath2.0 produces a solution, this script runs the whole analyis pipeline to rank the pathways and <ins>suggests</ins> the best performing pathways in an organism of choice. Note that the "deep RetroPath2.0" outputs a file called "model.sbml" of the model organism in which RetroPath2.0 found a solution. Note: "max_rp_steps" is the maximal number of steps are run in RetroPath2.0:

```
python analysis_pipeline.py -rp2_pathways rp_pathways.csv -gem_sbml model.sbml -max_rp_steps 3 
```

### Prediction Pipeline

Combine the above two scripts to predict and analyse heterologous pathways in an organism of choice

```
python prediction_pipeline.py -inchi "InChI=1S/C6H6O4/c7-5(8)3-1-2-4-6(9)10/h1-4H,(H,7,8)(H,9,10)/b3-1+,4-2+" -organism e_coli
```

## Version

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
