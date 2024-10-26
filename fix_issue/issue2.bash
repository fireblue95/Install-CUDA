# https://github.com/fireblue95/Install-CUDA/issues/4


sudo find / -name "libcublas.so*" -not -path "*/docker/*" -not -path "*/pypoetry/*" -not -path "*/python*/*"

# Please modify the cuda version which you installed.
cd /usr/local/cuda-12.6/targets/x86_64-linux/lib

ls -l libcublas.so*

# Please modify the cuda version which you installed.
sudo ln -s libcublas.so.12.6.3.3 libcublas.so.11
sudo ln -s libcublasLt.so.12.6.3.3 libcublasLt.so.11

ls -l libcublas.so*
cd /usr/src/cudnn_samples_v8/mnistCUDNN

sudo make clean
sudo make -j$(nproc)
./mnistCUDNN
