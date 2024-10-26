# This script will fix the issue from this url
# https://github.com/fireblue95/Install-CUDA/issues/3

cd /usr/src/cudnn_samples_v8/mnistCUDNN
sudo sed -i 's/,$(SMS)/,$(filter-out 35,$(SMS))/g' Makefile

sudo make clean
sudo make -j$(nproc)
./mnistCUDNN