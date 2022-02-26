
#!/bin/bash

# Generate and read version info
python3 ./versionInfoGen.py
VERSION=$(<file_name_version)
PKGNAME=VGC_Analyze_${VERSION}_deb_linux

# Bundle app files
python3 bundle.py

# Change to build directory
mkdir ./build
cd ./build
mkdir ./build
cd ./build

# Create .deb folder structure
mkdir ${PKGNAME}
mkdir ${PKGNAME}/usr
mkdir ${PKGNAME}/usr/local
mkdir ${PKGNAME}/usr/local/bin
mkdir ${PKGNAME}/usr/local/lib
mkdir ${PKGNAME}/usr/share
mkdir ${PKGNAME}/usr/share/applications

# Copy app files to .deb structure lib
cp -r ../dist/bundle/pack/VGC_Analyze ${PKGNAME}/usr/local/lib

# Copy start script to .deb structe bin
cp ../../vgcanalyze ${PKGNAME}/usr/local/bin

# Copy .desktop application file to .deb structure
cp ../../vgcanalyze.desktop ${PKGNAME}/usr/share/applications

# Create metadata
mkdir ${PKGNAME}/DEBIAN

echo -e "Package: vgcanalyze\n"\
"Version: "${VERSION}"\n"\
"Section: base\n"\
"Priority: optional\n"\
"Architecture: amd64\n"\
"Depends: python3-tk, python3-pil, python3-pil.imagetk, python3-matplotlib\n"\
"Maintainer: x211321\n"\
"Description: A visual VGCollect.com data analyzer\n"\
"Homepage: https://github.com/x211321/VGC_Analyze" > ${PKGNAME}/DEBIAN/control

# Build .deb package
dpkg-deb --build ${PKGNAME}

# Copy package to dist folder
mv ${PKGNAME}.deb ../dist