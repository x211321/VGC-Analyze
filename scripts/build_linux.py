#!/usr/bin/env python3

import os
import sys
import shutil
import tarfile
from zipfile import ZipFile


# Import version file from main project
sys.path.append("../")
from lib.Version import VERSION

BASE_DIR   = ""

BUILD_DIR  = "build"
DIST_DIR   = "dist"
BUNDLE_DIR = "VGC_Analyze_v" + VERSION


PKG_DIR    = "vgcanalyze"
PKG_NAME   = "vgcanalyze"
PKG_DESC   = "A visual VGCollect.com data analyzer"
PKG_URL    = "https://github.com/x211321/VGC_Analyze"


TMPPGK_DIR = BUNDLE_DIR + "_tmp"



def build():
    # Setup build environment
    init()

    # Copy files to bundle dir
    create_app_bundle()

    # Create package file structure
    create_package_file_structure()

    # Build .deb package
    build_deb("python3-tk, python3-pil, python3-pil.imagetk, python3-matplotlib", "deb")

    # Build Fedora .rpm package
    build_rpm("python3-tkinter, python3-pillow, python3-pillow-tk, python3-matplotlib", "fedora")

    # Build openSUSE Leap .rpm package
    #build_rpm("", "openSUSE_Leap")

    # Build openSUSE Tumbleweed .rpm package
    #build_rpm("", "openSUSE_TW")

    # Build Arch/PKGBUILD package
    build_pkgbuild("'tk' 'python-pillow' 'python-matplotlib'", "PKGBUILD")



# Setup build environment
def init():
    global BASE_DIR

    # Find directory that contains this script
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # cd to base dir
    os.chdir(BASE_DIR)

    # Create build directory
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    os.makedirs(BUILD_DIR)

    # cd to build dir
    os.chdir(BUILD_DIR)

    # Create dist dir
    os.makedirs(DIST_DIR)



##########################
# Copy files to bundle dir
def create_app_bundle():
    # Create bundle dir
    if os.path.exists(BUNDLE_DIR):
        shutil.rmtree(BUNDLE_DIR)

    if not os.path.exists(BUNDLE_DIR):
        os.makedirs(BUNDLE_DIR)

    shutil.copytree("../../assets/", BUNDLE_DIR + "/assets/")
    shutil.copytree("../../gui/", BUNDLE_DIR + "/gui/")
    shutil.copytree("../../lib/", BUNDLE_DIR + "/lib/")
    shutil.copy("../../VGC_Analyze.py", BUNDLE_DIR + "/VGC_Analyze.py")

    shutil.rmtree(BUNDLE_DIR + "/gui/__pycache__/")
    shutil.rmtree(BUNDLE_DIR + "/gui/popups/__pycache__/")
    shutil.rmtree(BUNDLE_DIR + "/lib/__pycache__/")

    # Create zip file
    zip = ZipFile(DIST_DIR + "/" + BUNDLE_DIR+"_script.zip", "w")

    for root, dirs, files in os.walk(BUNDLE_DIR):
        for f in files:
            zip.write(os.path.join(root, f))

    zip.close()



##################################################
# Create file structure for .deb and .rpm packages
def create_package_file_structure():
    os.makedirs(os.path.join(TMPPGK_DIR, "usr/bin"))
    os.makedirs(os.path.join(TMPPGK_DIR, "usr/share/applications"))
    os.makedirs(os.path.join(TMPPGK_DIR, "usr/share/icons/hicolor/128x128/apps/"))

    # Copy previously bundled files to file structure / lib
    shutil.copytree(BUNDLE_DIR + "/", os.path.join(TMPPGK_DIR, "usr/lib/" + PKG_DIR + "/"))

    # Copy start script to file structure / bin
    shutil.copy("../" + PKG_DIR, os.path.join(TMPPGK_DIR, "usr/bin/" + PKG_DIR))

    # Copy .desktop application file to file structure / applications
    shutil.copy("../" + PKG_DIR + ".desktop", os.path.join(TMPPGK_DIR, "usr/share/applications/" + PKG_DIR + ".desktop"))


#####################
# Create .deb package
def build_deb(dependencies, suffix):
    packageDir = BUNDLE_DIR + "_" + suffix

    os.makedirs(os.path.join(packageDir, "DEBIAN"))

    # Copy previously bundled files to .deb structure
    shutil.copytree(TMPPGK_DIR + "/usr", packageDir + "/usr")

    # Write metadata
    metaData =  "Package: " + PKG_NAME + "\n" \
                "Version: " + VERSION + "\n" \
                "Section: base\n" \
                "Priority: optional\n" \
                "Architecture: all\n" \
                "Depends: " + dependencies + "\n" \
                "Maintainer: x211321\n" \
                "Description: " + PKG_DESC + "\n" \
                "Homepage: " + PKG_URL + "\n"

    file = open (os.path.join(packageDir, "DEBIAN/control"), "w", encoding="utf-8")
    file.write(metaData)
    file.close()

    # Run dpkg-deb
    os.system("dpkg-deb --build " + packageDir)

    # Move package to dist dir
    shutil.move(packageDir + ".deb", DIST_DIR + "/")





#####################
# Create .rpm package
def build_rpm(dependencies, suffix):

    global BASE_DIR

    distDir    = os.path.join(BASE_DIR, BUILD_DIR, DIST_DIR, BUNDLE_DIR + "_" + suffix)
    packageDir = os.path.join(BASE_DIR, BUILD_DIR, BUNDLE_DIR + "_" + suffix)

    # Create SPECS directory
    os.makedirs(os.path.join(packageDir, "SPECS"))

    rpmProject = os.path.join(packageDir, "BUILDROOT/" + PKG_NAME + "-"+VERSION+"-1.noarch")

    # Copy previously bundled files to .rpm structure
    shutil.copytree(os.path.join(TMPPGK_DIR, "usr"), os.path.join(rpmProject, "usr"))

    # Write .rpm spec
    rpmspec = "Name:      " + PKG_NAME + "\n" \
              "Version:   " + VERSION + "\n" \
              "Release:   1\n" \
              "Summary:   Control RGB settings of the Acer-WMI kernel module\n" \
              "BuildArch: noarch\n" \
              "\n" \
              "License:   MIT\n" \
              "URL:       " + PKG_URL + "\n" \
              "\n" \
              "Requires:  " + dependencies + "\n" \
              "\n" \
              "%description\n" \
              + PKG_DESC + "\n" \
              "\n" \
              "%files\n"

    for root, dirs, files in os.walk(rpmProject):
        for f in files:
            rpmspec += os.path.join(root.replace(rpmProject, ""), f) + "\n"

    file = open (os.path.join(packageDir, "SPECS/rgb-config-acer-gkbbl-0.spec"), "w", encoding="utf-8")
    file.write(rpmspec)
    file.close()

    # Run rpmbuild
    os.system("rpmbuild --buildroot " + rpmProject + " --define \"_topdir " + os.path.join(BASE_DIR, BUILD_DIR, packageDir) + "\" -bb " + os.path.join(packageDir, "SPECS/rgb-config-acer-gkbbl-0.spec"))

    # Move .rpm package to dist folder
    for root, dirs, files in os.walk(os.path.join(packageDir, "RPMS/noarch/")):
        for f in files:
            shutil.move(os.path.join(root, f), distDir + ".rpm"),



#####################
# Create PKGBUILD
def build_pkgbuild(dependencies, suffix):
    packageDir = BUNDLE_DIR + "_" + suffix

    # Create directory
    os.makedirs(packageDir)

    # Create src tar bundle
    with tarfile.open(os.path.join(packageDir, "src") + ".tar.gz", "w:gz") as tar:
        for f in os.listdir(os.path.join(TMPPGK_DIR)):
            tar.add(os.path.join(os.path.join(TMPPGK_DIR), f), arcname=f)

    tar.close()

    # Write PKGBUILD
    pkgbuild =  'pkgname="' + PKG_NAME + '"\n' \
                'pkgver="' + VERSION + '"\n' \
                'pkgrel="1"\n' \
                'pkgdesc="' + PKG_DESC + '"\n' \
                'arch=("any")\n' \
                'depends=(' + dependencies + ')\n' \
                'license=("MIT")\n' \
                'source=("src.tar.gz")\n' \
                'sha512sums=("SKIP")\n' \
                'package() {\n' \
                '  mkdir -p "${pkgdir}/usr"\n' \
                '  cp -rf "${srcdir}/usr" "${pkgdir}/"\n' \
                '  chmod +x "${pkgdir}/usr/bin/' + PKG_DIR + '"\n' \
                '}\n'


    file = open (os.path.join(packageDir, "PKGBUILD"), "w", encoding="utf-8")
    file.write(pkgbuild)
    file.close()

    # Create pkgbuild tar bundle
    with tarfile.open(os.path.join(packageDir) + ".tar.gz", "w:gz") as tar:
        for root, dirs, files in os.walk(packageDir):
            for f in files:
                tar.add(os.path.join(root, f))

    tar.close()

    # Move package to dist dir
    shutil.move(packageDir + ".tar.gz", DIST_DIR + "/")


####################
# Run build function

build()
