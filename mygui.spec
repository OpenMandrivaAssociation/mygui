%define		major 3
%define		libname %mklibname %{name} %{major}
%define		devname %mklibname %{name} -d

%bcond_with ogre

Summary:	Fast, simple and flexible GUI library for Ogre
Name:		mygui
Version:	3.4.3
Release:	4
Group:		System/Libraries
# UnitTests include agg-2.4, which is under a BSD variant (not built or installed here)
License:	LGPLv3+
URL:		https://mygui.info/
Source0:	https://github.com/MyGUI/mygui/archive/refs/tags/MyGUI%{version}.tar.gz

Source1:	mygui.rpmlintrc
Patch0:		mygui-add-findpoco.patch
#Patch1:		mygui-3.2.2-FHS.patch 
#Patch2:		mygui-libCommon-fixup.patch
#Patch3:		mygui_multilib_cflags.patch
#Patch4:     MyGUI-lib_suffix.patch
Patch1:		mygui-3.4.2-SDL2_image-linkage.patch

BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(freetype2)
%if %{with ogre}
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:  ogre
BuildRequires:  ogre-samples
%else
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
%endif
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(x11)
%description
MyGUI is a GUI library for Ogre Rendering Engine which aims to be fast,
flexible and simple in using.

%package -n %{libname}
Summary:	Fast, simple and flexible GUI library for Ogre
Group:		System/Libraries

%description -n %{libname}
MyGUI is a GUI library for Ogre Rendering Engine which aims to be fast,
flexible and simple in using.

%package -n %{devname}
Summary:	Development files for MyGUI
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%if %{with ogre}
Requires:	pkgconfig(OIS)
Requires:	pkgconfig(OGRE)
%endif

%description -n %{devname}
The %{devname} package contains libraries and header files for
developing applications that use %{name}.

#package	doc
#Summary:	Development documentation for MyGUI
#Group:		Development/C++
#BuildArch:	noarch

#description	doc
#The %{name}-doc package contains reference documentation for
#developing applications that use %{name}.

%prep
%autosetup -p1 -n mygui-MyGUI%{version}

%build
export OGRE_LIBRARIES="`pkg-config --libs OGRE` -lboost_system"
# Plugins are windows only atm
%cmake \
    -DMYGUI_INSTALL_PDB:INTERNAL=FALSE \
    -DMYGUI_USE_FREETYPE=ON \
    -DMYGUI_DONT_USE_OBSOLETE=ON \
    -DMYGUI_BUILD_PLUGINS:BOOL=OFF \
    -DMYGUI_USE_STD_STRING_VIEW=ON \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags}" \
%if %{with ogre}
    -DOGRE_CONFIG_DIR=%{_datadir}/OGRE \
%else
    -DMYGUI_RENDERSYSTEM=7 \
%endif
    -DCMAKE_SKIP_RPATH:BOOL=ON \
    -G Ninja

%ninja_build
# Generate doxygen documentation
#pushd Docs
#doxygen
#rm -f html/installdox
#popd

%install
%ninja_install -C build

# Copy Media files
mkdir -p %{buildroot}%{_datadir}/MYGUI/
cp -a Media %{buildroot}%{_datadir}/MYGUI/

# Strip away unittests Media
rm -rf %{buildroot}%{_datadir}/MYGUI/Media/UnitTests

# Remove CMake stuff from Media
rm -f %{buildroot}%{_datadir}/MYGUI/Media/CMakeLists.txt

%files
%dir %{_datadir}/MYGUI/Media
%{_datadir}/MYGUI/Media/*

%files -n %{libname}
%{_libdir}/*.so.%{version}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#files doc
#doc build/Docs/html
