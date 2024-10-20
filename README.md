# arpe

# Build Container
docker build -t arpe .

docker run -p 8050:8050 arpe

# History
## 2024-10
The code has been enhanced to process files in parallel. Additionally, logic has been implemented in the user interface to indicate when duplicate files or non-.s2p files are uploaded.

Testfiles folder was expanded with 50 s2p files for mass testing. 

Error issue when corrupt file existing -  TBD
