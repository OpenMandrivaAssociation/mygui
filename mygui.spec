%define		major 3
%define		name mygui
%define		libname %mklibname %{name} %{major}
%define		develname %mklibname %{name} -d

Name:		%{name}
Version:	3.2
Release:	%mkrel 1
Summary:	Fast, simple and flexible GUI library for Ogre
Group:		System/Libraries
# UnitTests include agg-2.4, which is under a BSD variant (not built or installed here)
License:	LGPLv3+
URL:		http://mygui.info/
Source0:	http://downloads.sourceforge.net/my-gui/MyGUI%{version}.tar.bz2
# Get find poco from ogre
Patch3:		mygui-add-findpoco.patch
Patch5:		MyGUI3.2-cmake-svn.patch
BuildRequires:	freetype-devel
BuildRequires:	ois-devel
BuildRequires:	ogre-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	cmake
BuildRequires:	libuuid-devel

%description
MyGUI is a GUI library for Ogre Rendering Engine which aims to be fast,
flexible and simple in using.

%package -n %{libname}
Summary:	Fast, simple and flexible GUI library for Ogre
Group:		System/Libraries

%description -n %{libname}
MyGUI is a GUI library for Ogre Rendering Engine which aims to be fast,
flexible and simple in using.


%package -n %{develname}
Summary:	Development files for MyGUI
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	ois-devel
Requires:	ogre-devel

%description -n %{develname}
The %{develname} package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Development documentation for MyGUI
Group:		Development/C++
BuildArch:	noarch

%description	doc
The %{name}-doc package contains reference documentation for
developing applications that use %{name}.

%prep
%setup -q -n MyGUI%{version}
%patch3 -p0
%patch5 -p1 -b .svn
# Fix eol 
sed -i 's/\r//' COPYING.LESSER

%build
# Plugins are windows only atm
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=/usr \
    -DMYGUI_INSTALL_PDB:INTERNAL=FALSE -DCMAKE_BUILD_TYPE:STRING=Release \
    -DMYGUI_BUILD_PLUGINS:BOOL=OFF -DCMAKE_CXX_FLAGS_RELEASE= \
    -DCMAKE_SKIP_RPATH:BOOL=ON
%make
# Generate doxygen documentation
pushd Docs
doxygen
rm -f html/installdox
popd

%install
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING.LESSER
%dir %{_libdir}/MYGUI/
%{_libdir}/MYGUI/*
%dir %{_datadir}/MYGUI/Media
%{_datadir}/MYGUI/Media/*

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%doc Docs/html

