mkdir -p docker_projects
cd docker_projects

### RetroRules
git clone https://github.com/Galaxy-SynBioCAD/RetroRules.git
cd RetroRules
docker build -t brsynth/retrorules-standalone .
cd ..

### RetroPath2
git clone docker build -t brsynth/retropath2-standalone .
cd RetroPath2
docker build -t brsynth/retropath2-standalone .
cd ..

### rp2paths 
git clone docker build -t brsynth/rp2paths-standalone .
cd rp2paths
docker build -t brsynth/rp2paths-standalone .
cd ..

### rpBase
git clone https://github.com/Galaxy-SynBioCAD/rpBase.git
rp rpBase
docker build -t brsynth/rpbase .
cd ..

### rpCache
git clone https://github.com/Galaxy-SynBioCAD/rpCache.git
cd rpCache
docker build -t brsynth/rpcache .
cd ..

### rpMakeSource
git clone https://github.com/Galaxy-SynBioCAD/rpMakeSource.git

### rpExtractSink
git clone https://github.com/Galaxy-SynBioCAD/rpExtractSink.git
cd rpExtractSink
docker build -t brsynth/rpextractsink-standalone .
cd ..

### rpReader
git clone https://github.com/Galaxy-SynBioCAD/rpReader.git
cd rpReader
docker build -t brsynth/rpreader-standalone -f Dockerfile .
cd ..

### rpCofactors
git clone https://github.com/Galaxy-SynBioCAD/rpCofactors.git
cd rpCofactors
docker build -t brsynth/rpcofactors-standalone .
cd ..

### rpFBA
git clone https://github.com/Galaxy-SynBioCAD/rpFBA.git
cd rpFBA
docker build -t brsynth/rpfba-standalone -f Dockerfile .
cd ..

### rpThermo
git clone https://github.com/Galaxy-SynBioCAD/rpThermo.git
cd rpThermo 

if [ ! -f "license.cxl" ]; then
    echo "license.cxl does not exist. Need Marvin licence for the tool to work."
fi


if ! find . -name 'marvin_linux_*' -printf 1 -quit | grep -q 1
    echo "Need a local .deb version of the Marvin software"
fi

docker build -t brsynth/rthermo-standalone -f Dockerfile .
cd ..

### rpGlobalScore
git clone https://github.com/Galaxy-SynBioCAD/rpGlobalScore.git
cd rpGlobalScore
docker build -t brsynth/rpglobalscore-standalone -f Dockerfile .
cd ..

### rpReport
git clone https://github.com/Galaxy-SynBioCAD/rpReport.git
cd rpReport
docker build -t brsynth/rpglobalscore-standalone -f Dockerfile .
cd ..

### rpVisualiser
git clone https://github.com/Galaxy-SynBioCAD/rpVisualiser.git
cd rpVisualiser
docker build -t brsynth/rpvisualiser-standalone:dev .
cd ..

cd ..
### Copy all the docker run files
cp docker_projects/RetroRules/run.py run_retrorules.py
cp docker_projects/RetroPath2/run.py run_retropath2.py
cp docker_projects/rp2paths/run.py run_rp2paths.py
cp docker_projects/rpReader/run.py run_rpreader.py
cp docker_projects/rpCofactors/run.py run_rpcofactors.py
cp docker_projects/rpThermo/run.py run_rpthermo.py
cp docker_projects/rpGlobalScore/run.py run_rpglobalscore.py
cp docker_projects/rpReport/run.py run_rpreport.py
cp docker_projects/rpVisualiser/run.py run_rpvisualiser.py
