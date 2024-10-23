import subprocess
import sys


class InstallCuda:
    CUDA_VERSION = "11.7.1"

    CUDNN_VERSION = "8.5.0"
    CUDNN_USE_LINUX = False
    CUDNN_INSTALL_SAMPLE = False

    def __init__(self):
        self.init_params()

        self.run()

    def init_params(self) -> None:

        self.cuda_title = ['CUDA VERSION', 'Ubuntu 2204',
                           'Ubuntu 2004', 'Ubuntu 1804', 'DRIVER VERSION']
        self.cuda_info = [
            ['11.8.0', 'O', 'O', 'O', '520.61.05'],
            ['11.7.1', 'O', 'O', 'O', '515.65.01'],
            ['11.7.0', 'O', 'O', 'O', '515.43.04'],
            ['11.6.2', 'X', 'O', 'O', '510.47.03'],
            ['11.6.1', 'X', 'O', 'O', '510.47.03'],
            ['11.6.0', 'X', 'O', 'O', '510.39.01'],
            ['11.5.2', 'X', 'O', 'O', '495.29.05'],
            ['11.5.1', 'X', 'O', 'O', '495.29.05'],
            ['11.5.0', 'X', 'O', 'O', '495.29.05'],
            ['11.4.4', 'X', 'O', 'O', '470.82.01'],
            ['11.4.3', 'X', 'O', 'O', '470.82.01'],
            ['11.4.2', 'X', 'O', 'O', '470.57.02'],
            ['11.4.1', 'X', 'O', 'O', '470.57.02'],
            ['11.4.0', 'X', 'O', 'O', '470.42.01'],
            ['11.3.1', 'X', 'O', 'O', '465.19.01'],
            ['11.3.0', 'X', 'O', 'O', '465.19.01'],
            ['11.2.2', 'X', 'O', 'O', '460.32.03'],
            ['11.2.1', 'X', 'O', 'O', '460.32.03'],
            ['11.2.0', 'X', 'O', 'O', '460.27.04'],
            ['11.1.1', 'X', 'O', 'O', '455.32.00'],
            ['11.1.0', 'X', 'O', 'O', '455.23.05'],
            ['11.0.3', 'X', 'O', 'O', '450.51.06'],
            ['11.0.2', 'X', 'O', 'O', '450.51.05'],
            ['11.0.1', 'X', 'X', 'O', '450.36.06']
        ]

        self.cudnn_title = ['CUDNN VERSION', 'CUDA VERSION', 'Ubuntu 2204',
                            'Ubuntu 2004', 'Ubuntu 1804', 'VERSION LEVEL']
        self.cudnn_info = [
            ['8.6.0', '11.8', 'O', 'O', 'O', '163'],
            ['8.5.0', '11.7', 'O', 'O', 'O', '96'],
            ['8.4.1', '11.6', 'X', 'O', 'O', '50'],
            ['8.4.0', '11.6', 'X', 'O', 'O', '27'],
            ['8.3.3', '11.5', 'X', 'O', 'O', '40'],
            ['8.3.2', '11.5', 'X', 'O', 'O', '44'],
            ['8.3.1', '11.5', 'X', 'O', 'O', '22'],
        ]

        # print(self.cuda_title)
        # for i in self.cuda_info:
        #     for j in i:
        #         print(f'{j:>12s}', end='')
        #     print()

        command = 'cat /etc/lsb-release | grep DISTRIB_RELEASE | cut -d = -f 2'
        self.ubuntu_version = subprocess.run(
            command, shell=True, capture_output=True, text=True).stdout.strip().replace('.', '')

        assert self.ubuntu_version in [
            '2204', '2004', '1804'], f'Unsupport Ubuntu VERSION: {self.ubuntu_version} Only support [ 2204 | 2004 | 1804 ]'

    def run(self) -> None:
        remove_cmd = '--uninstall'

        if len(sys.argv) > 1 and sys.argv[1] != remove_cmd:
            [print(f'{x:>15s}', end='') for x in self.cuda_title]
            print()
            for i in self.cuda_info:
                for j in i:
                    print(f'{j:>15s}', end='')
                print()


if __name__ == '__main__':
    app = InstallCuda()
