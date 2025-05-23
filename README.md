# Ravand Container: Versatile Docker Images for Python Development & Production

Welcome to the official container registry for **Ravand Base Images**. This repository provides a suite of meticulously crafted Docker images, optimized for both CPU and GPU (NVIDIA CUDA) environments, and tailored for various Python versions and operational modes (development and production).

Our goal is to offer developers and MLOps engineers a streamlined, reliable, and efficient starting point for their containerized applications. Whether you're building a lightweight CPU-based service or a demanding GPU-accelerated machine learning pipeline, Ravand Container has an image for you.

## Table of Contents

* [Why Ravand Container?](#why-ravand-container)
* [Available Docker Images](#available-docker-images)
    * [Image Tagging Convention](#image-tagging-convention)
* [How to Use](#how-to-use)
* [Key Features](#key-features)
* [Contributing](#contributing)

## Why Ravand Container?

* **Versatility**: Support for multiple Python versions (3.10, 3.11, 3.12).
* **Hardware Acceleration**: Options for both CPU-only and NVIDIA CUDA-enabled (cu124) GPU images.
* **Optimized Modes**: Separate `dev` (development) and `prod` (production) images with appropriate configurations.
* **Standardized Bases**: Built on proven base images like `debian:bullseye-slim` for CPU and `nvidia/cuda:12.9.0-cudnn-runtime-ubuntu24.04` for GPU.
* **Automated Builds**: Images are automatically built and pushed to GHCR.io via GitHub Actions, ensuring they are always up-to-date.
* **Transparent & Reproducible**: All Dockerfiles and build scripts are available in this repository.

## Available Docker Images

Below is a comprehensive list of all available Docker image tags. This table is automatically generated and updated whenever new images are built.

<!-- IMAGES_TABLE_START -->
For details on each image (base OS, Python version, GPU support, dev vs prod), please refer to the table above.

### Image Tagging Convention

Our image tags follow a consistent pattern:
`ghcr.io/ravand-ai/ravand-container:py<PYTHON_VERSION>-<EXTRA>-<MODE>`

* `<PYTHON_VERSION>`: e.g., `3.10`, `3.11`, `3.12`
* `<EXTRA>`: Specifies the hardware variant, e.g., `cpu`, `cu124` (for CUDA 12.4).
* `<MODE>`: Indicates the image type, `dev` for development or `prod` for production.

Example: `ghcr.io/ravand-ai/ravand-container:py3.11-cu124-prod`

## How to Use

To use an image, you can pull it directly from the GitHub Container Registry (GHCR).

Example for pulling the Python 3.11 CPU development image:
```bash
docker pull ghcr.io/ravand-ai/ravand-container:py3.11-cpu-dev
```
You can then use this image as a base for your `Dockerfile` or run it directly.
```Dockerfile
# Example Dockerfile
FROM ghcr.io/ravand-ai/ravand-container:py3.11-cpu-prod

# Add your application code
COPY . /app
WORKDIR /app

# Install any additional dependencies
# RUN pip install -r requirements.txt

CMD ["python", "your_app.py"]
```
## Key Features
- **Multiple Python Versions**: Support for Python 3.10, 3.11, and 3.12.
- **CPU and GPU Variants**:
  - `cpu`: General-purpose images based on _debian:bullseye-slim_.
  - `cu124`: Images for NVIDIA GPUs, based on `nvidia/cuda:12.9.0-cudnn-runtime-ubuntu24.04`, suitable for CUDA 12.4 compatible workloads.
- **Development vs. Production Modes**:
  - `dev` images: May include additional tools and libraries useful for development and debugging.
  - `prod` images: Optimized for size and performance for production deployments.
- **Standardized Environment**: Consistent environments across all image variants.

## Contributing
Contributions are welcome! If you have suggestions for improvements, new image variants, or bug fixes, please:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes.
4. Ensure any scripts or configurations are updated accordingly.
5. Submit a pull request with a clear description of your changes.
