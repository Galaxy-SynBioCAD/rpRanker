# rpRanker

Command line interface to the retrosynthesis and pathway analysis pipeline found in the [Galaxy-SynBioCAD](https://galaxy-synbiocad.org/) platform.

## Getting Started

Pull and build the dockers following required for running the pipeline:
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

WARNING: This will take approximately 35GB of disk space

## Dependencies

* Base Docker Image: [rpBase](https://github.com/Galaxy-SynBioCAD/rpBase)
* rpCache Docker Image: [rpCache](https://github.com/Galaxy-SynBioCAD/rpCache)

## Installing

To build all the dockers locally:

```
bash build_all.sh
```

Untar the GEM SBML models files:

```
tar -xf models.tar.xz
```

## Running

### Deep RetroPath2.0

Run RetroPath2.0 looping throught the different available models for a given organism, and reducing complexity if RetroPath2.0 does not find a solution. Use the script deep_rp2.py to run it. Warning that this can take a long time and special attention must be given to the timeout parameter and the allocated RAM usage for the docker image when constructng it.

### Analysis Pipeline

Run the pathway analysis pipeline from the results of RetroPath2.0

### Prediction Pipeline

Combine the above two scripts to predict and analyse the resulting pathways.

## Versioning

v0.1

## Authors

* **Melchior du Lac**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
