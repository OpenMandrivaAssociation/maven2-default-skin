# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define bname           maven-default-skin
%define section         free

Summary:        A Maven site skin
Name:           maven2-default-skin
Version:        1.0
Release:        %mkrel 2.0.2
Epoch:		0
Group:          Development/Java
License:        Apache 2.0 License
URL:            http://maven.apache.org
BuildArch:      noarch
Source0:        %{bname}-%{version}.tar.gz
# svn export http://svn.apache.org/repos/asf/maven/skins/tags/maven-default-skin-1.0

Source1:        maven-skins.pom
Source2:        %{name}-settings.xml

Patch0:		maven2-default-skin-pom_xml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  jpackage-utils >= 0:1.7.1
BuildRequires:  java-rpmbuild
BuildRequires:  maven2 >= 0:2.0.4
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven-surefire-plugin
BuildRequires:  saxon
BuildRequires:  saxon-scripts
BuildRequires:  java >= 0:1.4.2
Requires:  maven2 >= 0:2.0.4

%description
Maven site default skin.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n %{bname}-%{version}

%patch0 -b .sav

%build
cp %{SOURCE2} maven2-settings.xml

sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/m2_repo/repository</url>|g" maven2-settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" maven2-settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/m2_repo/repository</url>|g" maven2-settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" maven2-settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" maven2-settings.xml

mkdir -p m2_repo/repository/JPP/maven2/default_poms
cp %{SOURCE1} m2_repo/repository/JPP/maven2/default_poms/org.apache.maven.skins-maven-skins.pom

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

MVN=/usr/bin/mvn-jpp
export M2SETTINGS=$(pwd)/maven2-settings.xml
export MAVEN_REPO_LOCAL=`pwd`/m2_repo/repository
export MAVEN_OPTS="-Dmaven.repo.local=$MAVEN_REPO_LOCAL -Dmaven2.jpp.mode=true -Dmaven.test.failure.ignore=true -Djava.awt.headless=true"
${MVN} -s ${M2SETTINGS} ${MAVEN_OPTS} install

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/maven2
install -m 0644 target/default-skin-%{version}.jar \
	$RPM_BUILD_ROOT%{_javadir}/maven2/default-skin-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}/maven2
   ln -fs default-skin-%{version}.jar default-skin.jar
popd
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 0644 pom.xml \
$RPM_BUILD_ROOT%{_datadir}/maven2/poms/org.apache.maven.skins-maven-default-skin.pom

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%{_javadir}/maven2/*
%{_datadir}/maven2/poms/*
