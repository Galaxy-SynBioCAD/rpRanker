mkdir -p docker_projects
cd docker_projects

### RetroRules
git clone https://github.com/Galaxy-SynBioCAD/RetroRules.git
cd RetroRules
docker build -t brsynth/retrorules-standalone -f Dockerfile .
cd ..

### RetroPath2
git clone https://github.com/Galaxy-SynBioCAD/RetroPath2.git
cd RetroPath2
docker build -t brsynth/retropath2-standalone -f Dockerfile .
cd ..

### rp2paths 
git clone https://github.com/Galaxy-SynBioCAD/rp2paths.git
cd rp2paths
docker build -t brsynth/rp2paths-standalone -f Dockerfile .
cd ..

### rpBase
git clone https://github.com/Galaxy-SynBioCAD/rpBase.git
cd rpBase
docker build -t brsynth/rpbase -f Dockerfile .
cd ..

### rpCache
git clone https://github.com/Galaxy-SynBioCAD/rpCache.git
cd rpCache
docker build -t brsynth/rpcache -f Dockerfile .
cd ..

### rpExtractSink
git clone https://github.com/Galaxy-SynBioCAD/rpExtractSink.git
cd rpExtractSink
docker build -t brsynth/rpextractsink-standalone -f Dockerfile .
cd ..

### rpReader
git clone https://github.com/Galaxy-SynBioCAD/rpReader.git
cd rpReader
docker build -t brsynth/rpreader-standalone -f Dockerfile .
cd ..

### rpCofactors
git clone https://github.com/Galaxy-SynBioCAD/rpCofactors.git
cd rpCofactors
docker build -t brsynth/rpcofactors-standalone -f Dockerfile .
cd ..

### rpFBA
git clone https://github.com/Galaxy-SynBioCAD/rpFBA.git
cd rpFBA
docker build -t brsynth/rpfba-standalone -f Dockerfile .
cd ..

### rpThermo
git clone https://github.com/Galaxy-SynBioCAD/rpThermo.git
cd rpThermo 
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
docker build -t brsynth/rpvisualiser-standalone .
cd ..

cd ..
### Copy all the docker run files
cp docker_projects/RetroRules/run.py run_retrorules.py
cp docker_projects/RetroPath2/run.py run_retropath2.py
cp docker_projects/rp2paths/run.py run_rp2paths.py
cp docker_projects/rpReader/run_rp2.py run_rpreader.py
cp docker_projects/rpFBA/run.py run_rpfba.py
cp docker_projects/rpCofactors/run.py run_rpcofactors.py
cp docker_projects/rpThermo/run.py run_rpthermo.py
cp docker_projects/rpGlobalScore/run.py run_rpglobalscore.py
cp docker_projects/rpReport/run.py run_rpreport.py
cp docker_projects/rpVisualiser/run.py run_rpvisualiser.py
cp docker_projects/rpExtractSink/run.py run_rpextractsink.py
