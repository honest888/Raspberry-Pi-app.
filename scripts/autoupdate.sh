#!/bin/sh

cd ~
sudo rm -r Savvyvan-AutoUpdate
git clone https://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@github.com/bankmil/Savvyvan-AutoUpdate.git
cd Savvyvan-AutoUpdate
cd lite2.1
sudo chmod +x updatenow.sh
./updatenow.sh
