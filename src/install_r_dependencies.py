import os
import sys
import subprocess

def check_r_installation():
    try:
        subprocess.run(["R", "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        print("R is not installed on this system. Skipping R library installation.")
        return False

def install_bioc_manager():
    try:
        subprocess.run(["R", "-e", "install.packages('BiocManager')"], check=True)
    except subprocess.CalledProcessError:
        print("An error occurred while installing 'BiocManager'.")
        sys.exit(1)

def install_r_library(library):
    try:
        print(f"Installing R library '{library}'...")
        # Use ask=FALSE to skip prompts and dependencies=TRUE to install all deps
        result = subprocess.run(["R", "-e",
                                f"BiocManager::install('{library}', update=FALSE, ask=FALSE, dependencies=TRUE)"],
                              check=True, capture_output=True, text=True)
        print(f"R library '{library}' installation output:")
        print(result.stdout)
        if result.stderr:
            print(f"Warnings/errors during installation:")
            print(result.stderr)

        # Verify installation by trying to load the library
        print(f"Verifying '{library}' can be loaded...")
        verify_result = subprocess.run(["R", "-e", f"library('{library}')"],
                                      check=True, capture_output=True, text=True)
        print(f"✓ R library '{library}' verified successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR installing R library '{library}':")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        sys.exit(1)

def install_r_package_version(package, version):
    """Install a specific version of an R package from CRAN archives"""
    try:
        print(f"Installing R package '{package}' version {version}...")
        url = f"https://cran.r-project.org/src/contrib/Archive/{package}/{package}_{version}.tar.gz"
        result = subprocess.run(
            ["R", "-e", f"install.packages('{url}', repos=NULL, type='source')"],
            check=True, capture_output=True, text=True
        )
        print(f"R package '{package}' v{version} installation output:")
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")

        # Verify
        print(f"Verifying '{package}' can be loaded...")
        verify_result = subprocess.run(["R", "-e", f"library('{package}')"],
                                      check=True, capture_output=True, text=True)
        print(f"✓ R package '{package}' v{version} verified successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR installing R package '{package}' v{version}:")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        sys.exit(1)

def install_cran_package(package):
    """Install a package from CRAN using install.packages()"""
    try:
        print(f"Installing CRAN package '{package}'...")
        result = subprocess.run(
            ["R", "-e", f"install.packages('{package}', repos='https://cloud.r-project.org', dependencies=TRUE)"],
            check=True, capture_output=True, text=True
        )
        print(f"CRAN package '{package}' installation output:")
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")

        # Verify
        print(f"Verifying '{package}' can be loaded...")
        verify_result = subprocess.run(["R", "-e", f"library('{package}')"],
                                      check=True, capture_output=True, text=True)
        print(f"✓ CRAN package '{package}' verified successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR installing CRAN package '{package}':")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    if check_r_installation():
        # Check R version
        result = subprocess.run(["R", "--version"], capture_output=True, text=True)
        print("R version info:")
        print(result.stdout.split('\n')[0])
        print()

        install_bioc_manager()

        # Install Hmisc from CRAN (WGCNA dependency)
        # This requires R >= 4.2.0
        install_cran_package('Hmisc')

        # Install WGCNA and limma via BiocManager
        for library in ['WGCNA', 'limma']:
            install_r_library(library)