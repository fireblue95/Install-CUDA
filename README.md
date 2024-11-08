# Install-CUDA and CUDNN in Ubuntu
Use Script to Install CUDA, CUDNN

Last updated: 2024/11/05

## Support Version

### CUDA
| CUDA VERSION | Ubuntu 2404 | Ubuntu 2204 | Ubuntu 2004 | Ubuntu 1804 |   DRIVER VERSION   |
| :----------: | :---------: | :---------: | :---------: | :---------: | :----------------: |
|    12.6.2    |      O      |      O      |      O      |      X      |      560.35.03     |
|    12.6.1    |      O      |      O      |      O      |      X      |      560.35.03     |
|    12.6.0    |      O      |      O      |      O      |      X      |      560.28.03     |
|    12.5.1    |      X      |      O      |      O      |      X      |      555.42.06     |
|    12.5.0    |      X      |      O      |      O      |      X      |      555.42.02     |
|    12.4.1    |      X      |      O      |      O      |      X      |      550.54.15     |
|    12.4.0    |      X      |      O      |      O      |      X      |      550.54.14     |
|    12.3.2    |      X      |      O      |      O      |      X      |      545.23.08     |
|    12.3.1    |      X      |      O      |      O      |      X      |      545.23.08     |
|    12.3.0    |      X      |      O      |      O      |      X      |      545.23.06     |
|    12.2.2    |      X      |      O      |      O      |      X      |      535.104.05    |
|    12.2.1    |      X      |      O      |      O      |      X      |      535.86.10     |
|    12.2.0    |      X      |      O      |      O      |      X      |      535.54.03     |
|    12.1.1    |      X      |      O      |      O      |      O      |      530.30.02     |
|    12.1.0    |      X      |      O      |      O      |      O      |      530.30.02     |
|    12.0.1    |      X      |      O      |      O      |      O      |      525.85.12     |
|    12.0.0    |      X      |      O      |      O      |      O      |      525.60.13     |
|    11.8.0    |      X      |      O      |      O      |      O      |      520.61.05     |
|    11.7.1    |      X      |      O      |      O      |      O      |      515.65.01     |
|    11.7.0    |      X      |      O      |      O      |      O      |      515.43.04     |
|    11.6.2    |      X      |      X      |      O      |      O      |      510.47.03     |
|    11.6.1    |      X      |      X      |      O      |      O      |      510.47.03     |
|    11.6.0    |      X      |      X      |      O      |      O      |      510.39.01     |
|    11.5.2    |      X      |      X      |      O      |      O      |      495.29.05     |
|    11.5.1    |      X      |      X      |      O      |      O      |      495.29.05     |
|    11.5.0    |      X      |      X      |      O      |      O      |      495.29.05     |
|    11.4.4    |      X      |      X      |      O      |      O      |      470.82.01     |
|    11.4.3    |      X      |      X      |      O      |      O      |      470.82.01     |
|    11.4.2    |      X      |      X      |      O      |      O      |      470.57.02     |
|    11.4.1    |      X      |      X      |      O      |      O      |      470.57.02     |
|    11.4.0    |      X      |      X      |      O      |      O      |      470.42.01     |
|    11.3.1    |      X      |      X      |      O      |      O      |      465.19.01     |
|    11.3.0    |      X      |      X      |      O      |      O      |      465.19.01     |
|    11.2.2    |      X      |      X      |      O      |      O      |      460.32.03     |
|    11.2.1    |      X      |      X      |      O      |      O      |      460.32.03     |
|    11.2.0    |      X      |      X      |      O      |      O      |      460.27.04     |
|    11.1.1    |      X      |      X      |      O      |      O      |      455.32.00     |
|    11.1.0    |      X      |      X      |      O      |      O      |      455.23.05     |
|    11.0.3    |      X      |      X      |      O      |      O      |      450.51.06     |
|    11.0.2    |      X      |      X      |      O      |      O      |      450.51.05     |
|    11.0.1    |      X      |      X      |      X      |      O      |      450.36.06     |

### CUDNN
| CUDNN VERSION | CUDA VERSION | Ubuntu 2404 | Ubuntu 2204 | Ubuntu 2004 | Ubuntu 1804 | VERSION LEVEL |
| :-----------: | :----------: | :---------: | :---------: | :---------: | :---------: | :-----------: |
|     8.8.0     |     12.0     |      X      |      O      |      O      |      O      |       121     |
|     8.7.0     |     11.8     |      X      |      O      |      O      |      X      |       84      |
|     8.6.0     |     11.8     |      X      |      O      |      O      |      O      |       163     |
|     8.5.0     |     11.7     |      X      |      O      |      O      |      O      |       96      |
|     8.4.1     |     11.6     |      X      |      X      |      O      |      O      |       50      |
|     8.4.0     |     11.6     |      X      |      X      |      O      |      O      |       27      |
|     8.3.3     |     11.5     |      X      |      X      |      O      |      O      |       40      |
|     8.3.2     |     11.5     |      X      |      X      |      O      |      O      |       44      |
|     8.3.1     |     11.5     |      X      |      X      |      O      |      O      |       22      |

## Usage

```bash
./Install_CUDA.sh
```

or

```bash
python install_cuda.py
```

## Remove Only
Can remove `Nvidia-driver`, `CUDA`, `CUDNN`
```bash
./Install_CUDA.sh --uninstall
```

or

```bash
python install_cuda.py --uninstall
```

# IF you have the issue maybe can check
https://github.com/fireblue95/Install-CUDA/issues?q=is%3Aissue+is%3Aclosed
