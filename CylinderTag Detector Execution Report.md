# CylinderTag Detector Execution Report

This document details the process of setting up and running the CylinderTag detector on the `test.bmp` image, as requested. The raw pose data has been extracted as proof of successful execution.

## 1. Environment Setup

The first step was to prepare the environment for building and running the detector.

### 1.1. Cloning the Repository

The CylinderTag repository was cloned from GitHub using the following command:

```bash
gh repo clone wsakobe/CylinderTag
```

### 1.2. Installing Dependencies

The `README.md` file indicated that OpenCV 4 and Ceres 2 were required. These were installed using `apt-get`:

```bash
sudo apt-get update
sudo apt-get install -y libopencv-dev libceres-dev cmake g++
```

## 2. Build Process

With the dependencies installed, the project was built using CMake and make.

### 2.1. CMake Configuration

A build directory was created and CMake was run to configure the project:

```bash
cd /home/ubuntu/CylinderTag
rm -rf build && mkdir build && cd build
cmake ..
```

### 2.2. Compilation

The project was then compiled using `make`. A small modification to the source code was necessary to resolve a missing header file issue (`opencv2/gapi/core.hpp`). The problematic line in `/home/ubuntu/CylinderTag/header/config.h` was commented out.

```bash
make -j$(nproc)
```

## 3. Execution and Output

To run the detector on the `test.bmp` image, the `main.cpp` file was modified to call `read_from_image("../test.bmp")` instead of `read_from_video("../test.avi")`. The code was also modified to print the raw pose data to the console.

### 3.1. Running the Detector

The detector was executed from the `build` directory:

```bash
./CylinderTag
```

### 3.2. Raw Pose Data

The following raw pose data was captured from the detector's output. This data represents the rotation (rvec) and translation (tvec) of each detected marker in the `test.bmp` image.

```
========== RAW POSE DATA OUTPUT ==========
Number of markers detected: 5

Marker ID: 5
Rotation Vector (rvec):
[0.4243708278919906;
 -0.5806630785025672;
 -0.2926798669788483]
Translation Vector (tvec):
[351.7946034709514;
 80.76462945366663;
 374.7367983968973]

Marker ID: 0
Rotation Vector (rvec):
[0.3942440669727758;
 0.3276895786214882;
 0.3045078949029997]
Translation Vector (tvec):
[-258.4665054788763;
 108.2018235513302;
 282.0376447078306]

Marker ID: 1
Rotation Vector (rvec):
[0.2138473420184894;
 -2.335834928348474;
 -1.500557417545226]
Translation Vector (tvec):
[281.8551480660349;
 -498.7212850633603;
 945.9397598193249]

Marker ID: 3
Rotation Vector (rvec):
[-0.9418378053024814;
 0.4708881220755439;
 1.493002000532229]
Translation Vector (tvec):
[40.57284039038122;
 -234.2562115950678;
 530.2952443802789]

Marker ID: 2
Rotation Vector (rvec):
[-0.8611423333725159;
 0.06475315319496097;
 -0.7600695033937491]
Translation Vector (tvec):
[-63.1378679889357;
 -159.9109503210157;
 472.0094289129118]
==========================================
```

## 4. Conclusion

The CylinderTag detector was successfully built and executed on the `test.bmp` image. The raw pose data has been extracted and documented as requested, demonstrating a successful run of the detector. The process has been documented in this report for your reference.
