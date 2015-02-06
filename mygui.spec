%define		major 3
%define		libname %mklibname %{name} %{major}
%define		devname %mklibname %{name} -d

Summary:	Fast, simple and flexible GUI library for Ogre
Name:		mygui
Version:	3.2.0
Release:	4
Group:		System/Libraries
# UnitTests include agg-2.4, which is under a BSD variant (not built or installed here)
License:	LGPLv3+
URL:		http://mygui.info/
Source0:	http://downloads.sourceforge.net/my-gui/MyGUI_%{version}.zip
Patch0:		MyGUI3.2-linkage.patch
# Get find poco from ogre
Patch3:		mygui-add-findpoco.patch
Patch5:		MyGUI-3.2.0-cmake-svn.patch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(OIS)
BuildRequires:	pkgconfig(OGRE)
BuildRequires:	pkgconfig(uuid)

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
Requires:	pkgconfig(OIS)
Requires:	pkgconfig(OGRE)

%description -n %{devname}
The %{devname} package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Development documentation for MyGUI
Group:		Development/C++
BuildArch:	noarch

%description	doc
The %{name}-doc package contains reference documentation for
developing applications that use %{name}.

%prep
%setup -q -n MyGUI_%{version}
%patch0 -p1
%patch3 -p0
%patch5 -p1 -b .svn
# Fix eol 
sed -i 's/\r//' COPYING.LESSER

%build
# Plugins are windows only atm
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DMYGUI_INSTALL_PDB:INTERNAL=FALSE \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DMYGUI_BUILD_PLUGINS:BOOL=OFF \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags}" \
    -DCMAKE_SKIP_RPATH:BOOL=ON
%make
# Generate doxygen documentation
pushd Docs
doxygen
rm -f html/installdox
popd

%install
%makeinstall_std

%ifarch x86_64
    mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
    sed -i s,/lib,/lib64, %{buildroot}%{_libdir}/pkgconfig/MYGUI.pc
%endif

# Remove sample showing plugin usage
for file in bin/Demo_* ; do
  install -Dp -m 755 $file %{buildroot}%{_libdir}/MYGUI/Demos/`basename $file`
done

# Copy Media files
mkdir -p %{buildroot}%{_datadir}/MYGUI/
cp -a Media %{buildroot}%{_datadir}/MYGUI/

# Strip away unittests Media
rm -rf %{buildroot}%{_datadir}/MYGUI/Media/UnitTests

# Remove CMake stuff from Media
rm -f %{buildroot}%{_datadir}/MYGUI/Media/CMakeLists.txt

%files
%doc COPYING.LESSER
%dir %{_libdir}/MYGUI/
%{_libdir}/MYGUI/*
%dir %{_datadir}/MYGUI/Media
%{_datadir}/MYGUI/Media/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%doc Docs/html

