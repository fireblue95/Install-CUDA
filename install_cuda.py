import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


class InstallCuda:
    # ----------------------------------------------------------------
    # Verison

    CUDA_VERSION = "11.7.1"

    CUDNN_VERSION = "8.5.0"
    CUDNN_USE_LINUX = False
    CUDNN_INSTALL_SAMPLE = False

    VERSION_INDEX_MAP = {
        '2404': 1,
        '2204': 2,
        '2004': 3,
        '1804': 4
    }

    # Verison
    # ----------------------------------------------------------------
    # ----------------------------------------------------------------
    # Install or remove

    DRIVER_REMOVE = False
    CUDA_REMOVE = False
    CUDNN_REMOVE = False

    CUDA_INSTALL = True
    CUDNN_INSTALL = True

    REMOVE_CMD = '--uninstall'

    TEMP_BUILD_DIR = Path('__build__temp__')

    # Install or remove
    # ----------------------------------------------------------------

    def __init__(self):
        self.init_params()

        self.run()

    @staticmethod
    def read_cfg(cfg_path: str) -> List[str]:
        data = []
        with open(cfg_path, 'r') as f:
            for x in f.readlines():
                data.append(x.strip().split(', '))

        return data

    def init_params(self) -> None:

        self.cuda_title = ['CUDA VERSION'] + [f'Ubuntu {x}' for x in self.VERSION_INDEX_MAP] + \
            ['DRIVER VERSION']

        self.cuda_info = self.read_cfg('cuda.txt')

        self.cudnn_title = ['CUDNN VERSION', 'CUDA VERSION'] + [f'Ubuntu {x}' for x in self.VERSION_INDEX_MAP] + \
            ['VERSION LEVEL']

        self.cudnn_info = self.read_cfg('cudnn.txt')

        command = 'cat /etc/lsb-release | grep DISTRIB_RELEASE | cut -d = -f 2'
        self.ubuntu_version = subprocess.run(
            command, shell=True, capture_output=True, text=True).stdout.strip().replace('.', '')

        assert self.ubuntu_version in [
            '2404', '2204', '2004', '1804'], f'Unsupport Ubuntu VERSION: {self.ubuntu_version} Only support [ 2404 | 2204 | 2004 | 1804 ]'

        self.index_cuda_version = self.VERSION_INDEX_MAP.get(
            self.ubuntu_version)
        self.index_cudnn_version = self.index_cuda_version + 1

    def filter_version(self, info: List[str], index: int) -> Dict[str, List[str]]:
        filted_version = {}

        if index is not None:
            for i in info:
                if i[index] == 'O':
                    filted_version.update({i[0]: i[1:]})
        return filted_version

    def choice_version(self, title: List[str], filted_version: Dict[str, List[str]], version: str) -> None:
        print(
            f'{"#" * 34} {version.split("_")[0]} VERSION {"#" * 41 if version.split("_")[0] == "CUDA" else "#" * 55}')
        # print title
        print(''.join(f'{x:^15s}' for x in title))

        # print content of version
        for k, v in filted_version.items():
            print(f'{k:^15}' + ''.join(f'{j:^15}' for j in v))

        print(
            f'{"#" * 34} {version.split("_")[0]} VERSION {"#" * 41 if version.split("_")[0] == "CUDA" else "#" * 55}')

        # Choice the version
        while True:
            var = input(
                f'Choice {version.split("_")[0]} VERSION [ Default {getattr(self, version)} ]: ')
            if var in filted_version:
                setattr(self, version, var)
                break
            elif var == '':
                break
            else:
                print(f'The version {var} not found.')

    def choice_other(self) -> None:

        # ----------------------------------------------------------------
        # CUDNN use Linux file

        while True:
            var = input(
                f"Install CUDNN LINUX .tar FILE?\n( If no will install .deb FILE )\n[ Default {'yes' if self.CUDNN_USE_LINUX == True else 'no'} ] (y/n):")

            if var.lower() in ['yes', 'y']:
                self.CUDNN_USE_LINUX = True

            if var.lower() in ['yes', 'y', 'no', 'n', '']:
                break

        # CUDNN use Linux file
        # ----------------------------------------------------------------
        # ----------------------------------------------------------------
        # CUDNN INSTALL SAMPLE

        while True:
            var = input(
                f"Install CUDNN SAMPLE? [ Default {'yes' if self.CUDNN_INSTALL_SAMPLE == True else 'no'} ] (y/n):")

            if var.lower() in ['yes', 'y']:
                self.CUDNN_INSTALL_SAMPLE = True

            if var.lower() in ['yes', 'y', 'no', 'n', '']:
                break

        # CUDNN INSTALL SAMPLE
        # ----------------------------------------------------------------

    def show_choose(self) -> None:
        print('#' * 30)
        print('Version')
        print(f"{'CUDA':<18}:\t{self.CUDA_VERSION}\n"
              f"{'CUDNN':<18}:\t{self.CUDNN_VERSION}\n"
              f"{'CUDNN file':<18}:\t{'.tar' if self.CUDNN_USE_LINUX is True else '.deb'}\n"
              f"{'CUDNN use Sample':<18}:\t{'yes' if self.CUDNN_INSTALL_SAMPLE is True else 'no'}")
        print('#' * 30)

    def run(self) -> None:
        self.curr_path = os.getcwd()

        self.filted_cuda_version = self.filter_version(
            self.cuda_info, self.index_cuda_version)
        self.filted_cudnn_version = self.filter_version(
            self.cudnn_info, self.index_cudnn_version)

        if len(sys.argv) == 1 or sys.argv[1] != self.REMOVE_CMD:
            self.choice_version(
                self.cuda_title, self.filted_cuda_version, 'CUDA_VERSION')

            self.choice_version(
                self.cudnn_title, self.filted_cudnn_version, 'CUDNN_VERSION')

            self.choice_other()

            self.show_choose()

        self.check_exists()

        if not self.CUDA_INSTALL and not self.CUDNN_INSTALL:
            exit()

        if self.TEMP_BUILD_DIR.exists():
            shutil.rmtree(self.TEMP_BUILD_DIR)
        self.TEMP_BUILD_DIR.mkdir(parents=True, exist_ok=True)

        os.chdir(self.TEMP_BUILD_DIR)

        self.remove_driver()

        self.remove_cuda()

        self.remove_cudnn()

        os.chdir(self.curr_path)

        if self.TEMP_BUILD_DIR.exists():
            shutil.rmtree(self.TEMP_BUILD_DIR)

        self.run_bash('sudo apt update')

        if len(sys.argv) > 1 and sys.argv[1] == self.REMOVE_CMD:
            print('Uninstall Complete.')
            exit()

        self.install_Cuda()

        self.install_cudnn()

        print('=' * 30)
        self.run_bash('nvidia-smi')
        print('=' * 30)

        self.run_bash('nvcc -V')
        print('=' * 30)

        if Path("/usr/local/cuda/include/cudnn_version.h").exists():
            self.run_bash(
                'cat /usr/local/cuda/include/cudnn_version.h | grep MAJOR -A 2')
        else:
            self.run_bash('dpkg -l | grep cudnn')
        print("Done.")

    def install_Cuda(self) -> None:
        self.CUDA_VERSION_MAJOR, self.CUDA_VERSION_MINOR, self.CUDA_VERSION_PATCHLEVEL = self.CUDA_VERSION.split(
            '.')

        if self.CUDA_INSTALL:
            self.DRIVER_VERSION = self.filted_cuda_version[self.CUDA_VERSION][-1]

            print(f'Installing driver: {self.DRIVER_VERSION}')

            self.CUDA_PIN_FILENAME = Path(
                f'cuda-ubuntu{self.ubuntu_version}.pin')

            if self.CUDA_PIN_FILENAME.exists():
                print('=' * 30)
                print(
                    f'CUDA PIN Installation File Exists: {self.CUDA_PIN_FILENAME}')
                print('=' * 30)
            else:
                self.run_bash(
                    f'wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu{self.ubuntu_version}/x86_64/{self.CUDA_PIN_FILENAME}')

            self.run_bash(
                f'sudo mv {self.CUDA_PIN_FILENAME} /etc/apt/preferences.d/cuda-repository-pin-600')

            self.CUDA_FILENAME = Path(
                f"cuda-repo-ubuntu{self.ubuntu_version}-{self.CUDA_VERSION_MAJOR}-{self.CUDA_VERSION_MINOR}-local_{self.CUDA_VERSION}-{self.DRIVER_VERSION}-1_amd64.deb")

            if self.CUDA_FILENAME.exists():
                print('=' * 30)
                print(f"CUDA Installation File Exists: {self.CUDA_FILENAME}")
                print('=' * 30)
            else:
                self.run_bash(
                    f'wget https://developer.download.nvidia.com/compute/cuda/{self.CUDA_VERSION}/local_installers/{self.CUDA_FILENAME}')

            self.run_bash(f'sudo dpkg -i {self.CUDA_FILENAME}')

            if int(self.CUDA_VERSION_MAJOR) <= 11 and int(self.CUDA_VERSION_MINOR) <= 6:
                self.run_bash(
                    f'sudo apt-key add /var/cuda-repo-ubuntu{self.ubuntu_version}-{self.CUDA_VERSION_MAJOR}-{self.CUDA_VERSION_MINOR}-local/*.pub')
            else:
                self.run_bash(
                    f'sudo cp /var/cuda-repo-ubuntu{self.ubuntu_version}-{self.CUDA_VERSION_MAJOR}-{self.CUDA_VERSION_MINOR}-local/cuda-*-keyring.gpg /usr/share/keyrings/')

            self.run_bash('sudo apt-get update')

            if self.CUDA_VERSION_MAJOR == 12 and self.CUDA_VERSION_MINOR >= 3:
                package_name = f'cuda-toolkit-{self.CUDA_VERSION_MAJOR}-{self.CUDA_VERSION_MINOR}'
            else:
                package_name = 'cuda'
            self.run_bash(f'sudo apt-get install -y {package_name}')

            # Add CUDA env path
            CUDA_ENV_PATH = f"export PATH=/usr/local/cuda-{self.CUDA_VERSION_MAJOR}.{self.CUDA_VERSION_MINOR}/bin:\$PATH"
            CUDA_ENV_LIB_PATH = f"export LD_LIBRARY_PATH=/usr/local/cuda-{self.CUDA_VERSION_MAJOR}.{self.CUDA_VERSION_MINOR}/lib64:\$LD_LIBRARY_PATH"

            BASHRC_FILE = '~/.bashrc'

            CHECK_CUDA_ENV_PATH = self.get_text(
                f'grep -c "{CUDA_ENV_PATH}" {BASHRC_FILE}')
            CHECK_CUDA_ENV_LIB_PATH = self.get_text(
                f'grep -c "{CUDA_ENV_LIB_PATH}" {BASHRC_FILE}')

            if int(CHECK_CUDA_ENV_PATH) == 0:
                self.run_bash(
                    f'echo "# SETTING CUDA ENVIRONMENT" >> {BASHRC_FILE}')
                self.run_bash(f'echo {CUDA_ENV_PATH} >> {BASHRC_FILE}')

            if int(CHECK_CUDA_ENV_LIB_PATH) == 0:
                self.run_bash(
                    f'echo "# SETTING CUDA ENVIRONMENT" >> {BASHRC_FILE}')
                self.run_bash(f'echo {CUDA_ENV_LIB_PATH} >> {BASHRC_FILE}')

            # self.run_bash(f'exec bash')
            # self.run_bash(f'source {os.path.expanduser(BASHRC_FILE)}')

    def install_cudnn(self) -> None:
        if self.CUDNN_INSTALL:
            self.CUDNN_VERSION_MAJOR, self.CUDNN_VERSION_MINOR, self.CUDNN_VERSION_PATCHLEVEL = self.CUDNN_VERSION.split(
                '.')

            CUDNN_PAGE_VERSION = self.filted_cudnn_version[self.CUDNN_VERSION][0]
            CUDNN_VERSION_LEVEL = self.filted_cudnn_version[self.CUDNN_VERSION][-1]

            if self.CUDNN_USE_LINUX:
                # Use Linux .tar file.
                if int(self.CUDNN_VERSION_MAJOR) <= 8 and int(self.CUDNN_VERSION_MINOR) <= 4:
                    CUDNN_FILENAME_NO_EXT = f"cudnn-linux-x86_64-{self.CUDNN_VERSION}.{CUDNN_VERSION_LEVEL}_cuda{CUDNN_PAGE_VERSION}-archive"
                    CUDNN_FILENAME = f"{CUDNN_FILENAME_NO_EXT}.tar.xz"
                else:
                    CUDNN_FILENAME_NO_EXT = f"cudnn-linux-x86_64-{self.CUDNN_VERSION}.{CUDNN_VERSION_LEVEL}_cuda11-archive"
                    CUDNN_FILENAME = f"{CUDNN_FILENAME_NO_EXT}.tar.xz"
            else:
                # Use .deb file.
                CUDNN_FILENAME = f"cudnn-local-repo-ubuntu{self.ubuntu_version}-{self.CUDNN_VERSION}.{CUDNN_VERSION_LEVEL}_1.0-1_amd64.deb"
            CUDNN_LIB_NAME = f"{self.CUDNN_VERSION}.{CUDNN_VERSION_LEVEL}-1+cuda{CUDNN_PAGE_VERSION}"

            if Path(CUDNN_FILENAME).exists():
                print('=' * 30)
                print(f"CUDNN Installation File Exists: {CUDNN_FILENAME}")
                print('=' * 30)
            else:
                self.run_bash(
                    f'wget https://developer.download.nvidia.com/compute/redist/cudnn/v{self.CUDNN_VERSION}/local_installers/{CUDNN_PAGE_VERSION}/{CUDNN_FILENAME}')

            if self.CUDNN_USE_LINUX:
                self.run_bash(f'tar -xvf {CUDNN_FILENAME}')
                self.run_bash(
                    f'sudo cp {CUDNN_FILENAME_NO_EXT}/include/cudnn*.h /usr/local/cuda/include')
                self.run_bash(
                    f'sudo cp -P {CUDNN_FILENAME_NO_EXT}/lib/libcudnn* /usr/local/cuda/lib64')
                self.run_bash(
                    f'sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*')
                self.run_bash(f'sudo rm -rf {CUDNN_FILENAME_NO_EXT}')
            else:
                self.run_bash(f'sudo dpkg -i {CUDNN_FILENAME}')
                if self.CUDNN_VERSION == '8.4.0':
                    self.run_bash(
                        f'sudo apt-key add /var/cudnn-local-repo-ubuntu{self.ubuntu_version}-{self.CUDNN_VERSION}.{CUDNN_VERSION_LEVEL}/*.pub')
                else:
                    self.run_bash(
                        f'sudo cp /var/cudnn-local-repo-*/cudnn-local-*-keyring.gpg /usr/share/keyrings/')

                self.run_bash(f'sudo apt-get update')
                self.run_bash(f'sudo apt-get install -y \
                    libcudnn8={CUDNN_LIB_NAME} \
                    libcudnn8-dev={CUDNN_LIB_NAME}')

                if self.CUDNN_INSTALL_SAMPLE:
                    self.run_bash(f'sudo apt-get install -y \
                        libfreeimage3 \
                        libfreeimage-dev \
                        libcudnn8-samples={CUDNN_LIB_NAME}')

                    tmp_path = glob.glob('/usr/src/cudnn*/mnistCUDNN')
                    if tmp_path:

                        os.chdir(tmp_path[0])

                        self.run_bash(f'sudo make clean')
                        self.run_bash(f'sudo make -j$(nproc)')
                        self.run_bash(f'./mnistCUDNN')
                    else:
                        print(f'Path not found: /usr/src/cudnn*/mnistCUDNN')
                    os.chdir(self.curr_path)

    def run_bash(self, cmd) -> None:
        subprocess.run(
            cmd, shell=True, capture_output=False, text=True)

    def remove_driver(self) -> None:
        if self.DRIVER_REMOVE:
            self.run_bash(f'sudo apt remove --autoremove --purge -y *nvidia*')

            if Path('/usr/bin/nvidia-uninstall').exists():
                self.run_bash('sudo nvidia-uninstall --silent')

    def remove_cuda(self) -> None:
        if self.CUDA_REMOVE:
            if int(self.get_text('dpkg -l | grep -c cuda')) > 0:
                self.run_bash('sudo apt remove --autoremove --purge -y cuda*')
            self.run_bash('''sudo rm -rf /usr/local/cuda* \
        /usr/share/keyrings/cuda* \
        /etc/apt/sources.list.d/cuda*''')

            if int(self.get_text('dpkg -l | grep cuda | grep -c repo-')) > 0:
                self.run_bash(
                    "sudo dpkg -P $(dpkg -l | grep cuda | grep repo- | awk '{print $2}')")

    def remove_cudnn(self) -> None:
        if self.CUDNN_REMOVE:
            if int(self.get_text('dpkg -l | grep -c libcudnn')) > 0:
                self.run_bash(
                    'sudo apt remove --autoremove --purge -y libcudnn*')

            if int(self.get_text('dpkg -l | grep -c cudnn')) > 0:
                self.run_bash('sudo apt remove --autoremove --purge -y cudnn*')

            if int(self.get_text('sudo apt-key list | grep -c "7FA2 AF80"')) > 0:
                self.run_bash('sudo apt-key del "7FA2 AF80"')

            self.run_bash('''sudo rm -rf /usr/src/cudnn* \
        /usr/local/cuda/include/cudnn*.h \
        /usr/local/cuda/lib64/libcudnn* \
        /usr/share/keyrings/cudnn* \
        /etc/apt/sources.list.d/cudnn*''')

            if int(self.get_text('dpkg -l | grep cudnn | grep -c repo-')) > 0:
                self.run_bash(
                    "sudo dpkg -P $(dpkg -l | grep cudnn | grep repo- | awk '{print $2}')")

    def check_exists(self) -> None:
        self.check_driver_exists()

        self.check_cuda_exists()

    def get_text(self, cmd: str) -> str:
        return subprocess.run(
            cmd, shell=True, capture_output=True, text=True).stdout.strip()

    def check_driver_exists(self) -> None:
        # Condition
        c1 = self.get_text('dpkg -l | grep -c nvidia-driver')
        c2 = Path('/usr/bin/nvidia-smi').exists()
        c3 = Path('/usr/bin/nvidia-uninstall').exists()

        if len(sys.argv) > 1 and sys.argv[1] == self.REMOVE_CMD:
            msg = 'remove'
        else:
            msg = 'reinstall'

        if int(c1) > 0 or c2 or c3:
            print('=' * 30)
            print(f'Nvidia-Driver Exists! You want to keep or {msg}?')
            while True:
                var = input(f'[ Default Keep ] (k/r):')

                if var.lower() in ['remove', 'r']:
                    self.DRIVER_REMOVE = True

                if var.lower() in ['keep', 'k', 'remove', 'r', '']:
                    break

    def check_cuda_exists(self) -> None:
        c1 = Path('/usr/local/cuda').exists()
        c2 = self.get_text(
            'dpkg -l | grep cuda | grep -v -E "(repo-|TensorRT)" | wc -l')
        c3 = self.get_text('ls /usr/share/keyrings | grep -c cuda')
        c4 = self.get_text('ls /etc/apt/sources.list.d | grep -c cuda')

        if len(sys.argv) > 1 and sys.argv[1] == self.REMOVE_CMD:
            msg = 'remove'
        else:
            msg = 'reinstall'

        if c1 or int(c2) > 0 or int(c3) > 0 or int(c4) > 0:
            print('=' * 30)
            print(f'CUDA Exists! You want to keep or {msg}?')
            print(f'If remove will remove CUDA and CUDNN')
            while True:
                var = input('[ Default keep ] (k/r):')

                if var in ['remove', 'r']:
                    self.CUDA_REMOVE = True
                    self.CUDNN_REMOVE = True
                    break
                elif var in ['keep', 'k', '']:
                    self.CUDA_REMOVE = False
                    self.CUDA_INSTALL = False
                    break

            self.check_cudnn_exists()

    def check_cudnn_exists(self) -> None:
        # ----------------------------------------------------------------
        # Check CUDNN

        cc1 = Path('/usr/local/cuda/include/cudnn_version.h').exists()
        cc2 = self.get_text('dpkg -l | grep cudnn | grep -v repo- | wc -l')
        cc3 = self.get_text('ls /usr/share/keyrings | grep -c cudnn')
        cc4 = self.get_text('ls /etc/apt/sources.list.d | grep -c cudnn')
        cc5 = self.get_text('ls /usr/src | grep -c cudnn')
        cc6 = self.get_text('sudo apt-key list | grep -c "7FA2 AF80"')

        condi = cc1 or int(cc2) > 0 or int(cc3) > 0 or int(cc4) > 0 \
            or int(cc5) > 0 or int(cc6) > 0

        # Check CUDNN
        # ----------------------------------------------------------------

        # ----------------------------------------------------------------
        # Ask remove or keep CUDNN

        if len(sys.argv) > 1 and sys.argv[1] == self.REMOVE_CMD:
            msg = 'remove'
        else:
            msg = 'reinstall'

        if not self.CUDA_REMOVE and condi:
            print('=' * 30)
            print(f'CUDNN Exists! You want to keep or {msg}?')

            while True:

                var = input('[ Default keep ] (k/r):')
                if msg == 'reinstall' and var in ['reinstall', 'r']:
                    self.CUDNN_REMOVE = True
                    self.CUDNN_INSTALL = True
                    break
                elif var in ['remove', 'r']:
                    self.CUDNN_REMOVE = True
                    self.CUDNN_INSTALL = False
                    break
                elif var in ['keep', 'k', '']:
                    self.CUDNN_REMOVE = False
                    self.CUDNN_INSTALL = False
                    break

        # Ask remove or keep CUDNN
        # ----------------------------------------------------------------


if __name__ == '__main__':
    app = InstallCuda()
