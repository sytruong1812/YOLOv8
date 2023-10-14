
1. Tai onnxruntime_gpu:

    Vao trang web nay: https://elinux.org/Jetson_Zoo#ONNX_Runtime
    chon version theo Jetpack OS tren jetson

    Vidu: Jetpack 4.6

        wget https://nvidia.box.com/shared/static/pmsqsiaw4pg9qrbeckcbymho6c01jj4z.whl -O onnxruntime_gpu-1.11.0-cp36-cp36m-linux_aarch64.whl
        pip3 install onnxruntime_gpu-1.10.0-cp36-cp36m-linux_aarch64.whl

2. Fix loi cai onnxruntime_gpu:

    - Thieu thu vien numpy:
        pip3 install 'https://github.com/jetson-nano-wheels/python3.6-numpy-1.19.4/releases/download/v0.0.2/numpy-1.19.4-cp36-cp36m-linux_aarch64.whl'

    - Thieu thu vien yaml:
        pip3 install PyYAML
    
    - Thieu libopenlas:
        sudo apt-get install libopenblas-dev
    
    - Thieu protobuf:
        pip3 install protobuf==3.19.6

    - Thieu argparse:
        pip3 install argparse

3. Run

    cd to autoCar folder

    python3 ./run.py
    python3 ./run.py --showCamera True