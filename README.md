# arpe

# Docker Deplyoment
## Build Container
docker build -t arpe .
## Run Container 
docker run -e env=prod -p 8050:8050 arpe 

# Podman Deplyoment
## Build Container
podman build -t arpe .
## Run Container 
podman run -e env=prod -p 8050:8050 arpe 

# Run local
´´´
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python appV2.py
´´´

# History
## 2024-10
The code has been enhanced to process files in parallel. Additionally, logic has been implemented in the user interface to indicate when duplicate files or non-.s2p files are uploaded.

Testfiles folder was expanded with 50 s2p files for mass testing. 

Error issue when corrupt file existing -  TBD
