# TODO
# - use name like: nvidia-71xx and nvidia-96xx, nvidia-173xx.
# - solve this (shouldn't there be some obsoletes?):
#   error: xorg-driver-video-nvidia-169.12-3.i686 (cnfl Mesa-libGL) conflicts with installed Mesa-libGL-7.0.3-2.i686
#   error: xorg-driver-video-nvidia-169.12-3.i686 (cnfl Mesa-libGL) conflicts with installed Mesa-libGL-7.0.3-2.i686
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# without kernel packages
%bcond_without	userspace	# don't build userspace programs
%bcond_with	multigl		# package libGL and libglx.so in a way allowing concurrent install with nvidia/fglrx drivers
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif
%define		no_install_post_check_so	1

%define		pname		xorg-driver-video-nvidia-legacy3
%define		rel		5

Summary:	Linux Drivers for nVidia GeForce/Quadro Chips (173.14.xx series)
Summary(hu.UTF-8):	Linux meghajtók nVidia GeForce/Quadro chipekhez
Summary(pl.UTF-8):	Sterowniki do kart graficznych nVidia GeForce/Quadro
Name:		%{pname}%{_alt_kernel}
Version:	173.14.30
Release:	%{rel}%{?with_multigl:.mgl}
License:	nVidia Binary
Group:		X11
Source0:	ftp://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}-pkg0.run
# Source0-md5:	665f9f730c18ab24a997e0e14b863262
Source1:	ftp://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-pkg0.run
# Source1-md5:	8c47463ae14a2f742d0fa00160456745
Source2:	%{pname}-xinitrc.sh
Patch0:		X11-driver-nvidia-GL.patch
Patch1:		X11-driver-nvidia-legacy-desktop.patch
URL:		http://www.nvidia.com/object/unix.html
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
%endif
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 10.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Provides:	xorg-xserver-module(glx)
Obsoletes:	XFree86-driver-nvidia
Obsoletes:	XFree86-nvidia
Conflicts:	XFree86-OpenGL-devel <= 4.2.0-3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLcore.so.1

%description
This driver set adds improved 2D functionality to the Xorg X server as
well as high performance OpenGL acceleration, AGP support, support for
most flat panels, and 2D multiple monitor support. Supported hardware:
modern NVIDIA GeForce (from GeForce2 MX) and Quadro (Quadro4 and up)
based graphics accelerators.

The older graphics chips are unsupported:
- NV1 and RIVA 128/128ZX chips are supported in the base Xorg install
  (nv driver)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 are suported by -legacy
  drivers.

%description -l hu.UTF-8
Ez a meghajtó kibővíti az Xorg X szerver 2D működését OpenGL
gyorsítással, AGP támogatással és támogatja a több monitort.
Támogatott hardverek: modern NVIDIA GeForce (GeForce2 MX-től) és
Quadro (Quadro4 és újabbak) alapú grafikai gyorsítók.

A régekbbi grafikus chipek nem támogatottak:
- NV1 és RIVA 128/128ZX chipek az alap Xorg telepítéssel (nv meghajtó)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 a -legacy driverekkel
  támogatottak.

%description -l pl.UTF-8
Usprawnione sterowniki dla kart graficznych nVidia do serwera Xorg,
dające wysokowydajną akcelerację OpenGL, obsługę AGP i wielu monitorów
2D. Obsługują w miarę nowe karty NVIDIA GeForce (od wersji GeForce2
MX) oraz Quadro (od wersji Quadro4).

Starsze układy graficzne nie są obsługiwane przez ten pakiet:
- NV1 i RIVA 128/128ZX są obsługiwane przez sterownik nv z Xorg
- TNT/TNT2/GeForce 256/GeForce 2 Ultra/Quadro 2 są obsługiwane przez
  sterowniki -legacy

%package libs
Summary:	OpenGL (GL and GLX) Nvidia libraries
Summary(pl.UTF-8):	Biblioteki OpenGL (GL i GLX) Nvidia
Group:		X11/Development/Libraries
#Requires:	%{pname} = %{epoch}:%{version}-%{rel}
Provides:	OpenGL = 2.1
Provides:	OpenGL-GLX = 1.4
%if %{without multigl}
Obsoletes:	Mesa
%endif
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0
%if %{without multigl}
Conflicts:	Mesa-libGL
%endif

%description libs
NVIDIA OpenGL (GL and GLX only) implementation libraries.

%description libs -l pl.UTF-8
Implementacja OpenGL (tylko GL i GLX) firmy NVIDIA.

%package devel
Summary:	OpenGL (GL and GLX) header files
Summary(hu.UTF-8):	OpenGL (GL és GLX) fejléc fájlok
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGL (GL i GLX)
Group:		X11/Development/Libraries
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Provides:	OpenGL-GLX-devel = 1.4
Provides:	OpenGL-devel = 2.1
Obsoletes:	X11-OpenGL-devel-base
Obsoletes:	XFree86-OpenGL-devel-base
Obsoletes:	XFree86-driver-nvidia-devel
Conflicts:	XFree86-OpenGL-devel < 4.3.99.902-0.3

%description devel
OpenGL header files (GL and GLX only) for NVIDIA OpenGL
implementation.

%description devel -l hu.UTF-8
OpenGL fejléc fájlok (csak GL és GLX) NVIDIA OpenGL implementációhoz.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenGL (tylko GL i GLX) dla implementacji OpenGL
firmy NVIDIA.

%package static
Summary:	Static XvMCNVIDIA library
Summary(hu.UTF-8):	Statikus XwMCNVIDIA könyvtár
Summary(pl.UTF-8):	Statyczna biblioteka XvMCNVIDIA
Group:		X11/Development/Libraries
Requires:	%{pname}-devel = %{epoch}:%{version}-%{rel}

%description static
Static XvMCNVIDIA library.

%description static -l hu.UTF-8
Statikus XwMCNVIDIA könyvtár.

%description static -l pl.UTF-8
Statyczna biblioteka XvMCNVIDIA.

%package doc
Summary:	Documentation for NVIDIA Graphics Driver
Group:		Documentation

%description doc
NVIDIA Accelerated Linux Graphics Driver README and Installation
Guide.

%package progs
Summary:	Tools for advanced control of nVidia graphic cards
Summary(hu.UTF-8):	Eszközök az nVidia grafikus kártyák beállításához
Summary(pl.UTF-8):	Narzędzia do zarządzania kartami graficznymi nVidia
Group:		Applications/System
Requires:	%{pname} = %{epoch}:%{version}-%{rel}
Suggests:	pkgconfig
Obsoletes:	XFree86-driver-nvidia-progs

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l hu.UTF-8
Eszközök az nVidia grafikus kártyák beállításához.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%package -n kernel%{_alt_kernel}-video-nvidia-legacy3
Summary:	nVidia kernel module for nVidia Architecture support
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung
Summary(hu.UTF-8):	nVidia Architektúra támogatás Linux kernelhez.
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
%{?with_dist_kernel:%requires_releq_kernel}
Requires:	%{pname} = %{epoch}:%{version}-%{rel}
Provides:	X11-driver-nvidia(kernel)
Obsoletes:	XFree86-nvidia-kernel

%description -n kernel%{_alt_kernel}-video-nvidia-legacy3
nVidia Architecture support for Linux kernel.

%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l de.UTF-8
Die nVidia-Architektur-Unterstützung für den Linux-Kern.

%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l hu.UTF-8
nVidia Architektúra támogatás Linux kernelhez.

%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l pl.UTF-8
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez
sterownik nVidii dla Xorg/XFree86.

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86*-%{version}-pkg*
%ifarch %{ix86}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86-%{version}-pkg0
%else
/bin/sh %{SOURCE1} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{version}-pkg0
%endif
%patch0 -p1
%patch1 -p1
echo 'EXTRA_CFLAGS += -Wno-pointer-arith -Wno-sign-compare -Wno-unused' >> usr/src/nv/Makefile.kbuild

%build
%if %{with kernel}
cd usr/src/nv
ln -sf Makefile.kbuild Makefile
cat >> Makefile <<'EOF'

$(obj)/nv-kernel.o: $(src)/nv-kernel.o.bin
	cp $< $@
EOF
mv nv-kernel.o{,.bin}
%build_kernel_modules -m nvidia
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,extensions} \
	$RPM_BUILD_ROOT{%{_includedir}/GL,%{_libdir},%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/etc/X11/xinit/xinitrc.d}
%if %{with multigl}
install -d $RPM_BUILD_ROOT{%{_libdir}/nvidia,%{_sysconfdir}/ld.so.conf.d}
%endif

install -p usr/bin/nvidia-{settings,xconfig,bug-report.sh} $RPM_BUILD_ROOT%{_bindir}
cp -p usr/share/man/man1/nvidia-{settings,xconfig}.* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p usr/share/applications/nvidia-settings.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p usr/share/pixmaps/nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh

for f in \
	usr/lib/tls/libnvidia-tls.so.%{version}		\
	usr/lib/libnvidia-cfg.so.%{version}		\
	usr/lib/libGL{,core}.so.%{version}		\
	usr/X11R6/lib/libXvMCNVIDIA.so.%{version}	\
%if %{without multigl}
	usr/X11R6/lib/libXvMCNVIDIA.a			\
; do
	install $f $RPM_BUILD_ROOT%{_libdir}
done
%else
; do
	install -p $f $RPM_BUILD_ROOT%{_libdir}/nvidia
done
cp -p usr/X11R6/lib/libXvMCNVIDIA.a $RPM_BUILD_ROOT%{_libdir}
%endif

install -p usr/X11R6/lib/modules/extensions/libglx.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions
install -p usr/X11R6/lib/modules/drivers/nvidia_drv.so \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so.%{version}
install -p usr/X11R6/lib/modules/libnvidia-wfb.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules

cp -p usr/include/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL

ln -sf libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/libglx.so
ln -sf nvidia_drv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so

%if %{with multigl}
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf

# OpenGL ABI for Linux compatibility
ln -sf libGL.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf nvidia/libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so

ln -sf nvidia/libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libXvMCNVIDIA.so
ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libXvMCNVIDIA_dynamic.so.1
%else
# OpenGL ABI for Linux compatibility
ln -sf libGL.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so

ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libXvMCNVIDIA.so
ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libXvMCNVIDIA_dynamic.so.1
%endif
%endif

%if %{with kernel}
%install_kernel_modules -m usr/src/nv/nvidia -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << 'EOF'
NOTE: You must also install kernel module for this driver to work
  kernel-video-nvidia-legacy3-%{version}

EOF
/sbin/ldconfig -N %{_libdir}/xorg/modules/extensions
# until versioned SONAME is built for nvidia_drv.so, update symlink manually
ln -sf nvidia_drv.so.%{version} %{_libdir}/xorg/modules/drivers/nvidia_drv.so

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n kernel%{_alt_kernel}-video-nvidia-legacy3
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-nvidia-legacy3
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE
%doc usr/share/doc/{README.txt,NVIDIA_Changelog,XF86Config.sample}
%if %{with multigl}
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so.*
%attr(755,root,root) %ghost %{_libdir}/xorg/modules/extensions/libglx.so
%else
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/libglx.so.*
%attr(755,root,root) %ghost %{_libdir}/xorg/modules/extensions/libglx.so
%endif
%attr(755,root,root) %{_libdir}/xorg/modules/libnvidia-wfb.so.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so.*.*
%attr(755,root,root) %ghost %{_libdir}/xorg/modules/drivers/nvidia_drv.so

%files libs
%defattr(644,root,root,755)
%if %{with multigl}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/nvidia.conf
%dir %{_libdir}/nvidia
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libXvMCNVIDIA.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libXvMCNVIDIA_dynamic.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cfg.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-tls.so.*.*
%else
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
# symlink for binary apps which fail to conform Linux OpenGL ABI
# (and dlopen libGL.so instead of libGL.so.1)
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libGLcore.so.*.*
%attr(755,root,root) %{_libdir}/libXvMCNVIDIA.so.*.*
%attr(755,root,root) %{_libdir}/libXvMCNVIDIA_dynamic.so.1
%attr(755,root,root) %{_libdir}/libnvidia-cfg.so.*.*
%attr(755,root,root) %{_libdir}/libnvidia-tls.so.*.*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCNVIDIA.so
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%if %{with multigl}
%attr(755,root,root) %{_libdir}/libGL.so
%endif

%files static
%defattr(644,root,root,755)
%{_libdir}/libXvMCNVIDIA.a

%files doc
%defattr(644,root,root,755)
%doc usr/share/doc/html/*

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nvidia-settings
%attr(755,root,root) %{_bindir}/nvidia-xconfig
%attr(755,root,root) %{_bindir}/nvidia-bug-report.sh
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%{_desktopdir}/nvidia-settings.desktop
%{_mandir}/man1/nvidia-*
%{_pixmapsdir}/nvidia-settings.png
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-nvidia-legacy3
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
