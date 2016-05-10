#!/bin/sh

[ -d ~/rpmbuild/SOURCES ] || mkdir -p ~/rpmbuild/SOURCES
[ -d ~/rpmbuild/RPMS ] || mkdir -p ~/rpmbuild/RPMS
[ -d ~/rpmbuild/SRPMS ] || mkdir -p ~/rpmbuild/SRPMS

name=libdrm
version=`rpmspec --query --srpm --queryformat="%{version}" packaging/${name}.spec`
buildname=${name}-${version}

git archive --format=tar.gz --prefix=$buildname/ -o ~/rpmbuild/SOURCES/$buildname.tar.gz HEAD

rpmbuild -ba packaging/${name}.spec
