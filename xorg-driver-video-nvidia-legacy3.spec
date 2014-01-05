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
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

# The goal here is to have main, userspace, package built once with
# simple release number, and only rebuild kernel packages with kernel
# version as part of release number, without the need to bump release
# with every kernel change.
%if 0%{?_pld_builder:1} && %{with kernel} && %{with userspace}
%{error:kernel and userspace cannot be built at the same time on PLD builders}
exit 1
%endif

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%undefine	with_userspace
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		no_install_post_check_so	1

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel		3
%define		pname		xorg-driver-video-nvidia-legacy3
Summary:	Linux Drivers for nVidia GeForce/Quadro Chips (173.14.xx series)
Summary(hu.UTF-8):	Linux meghajtók nVidia GeForce/Quadro chipekhez
Summary(pl.UTF-8):	Sterowniki do kart graficznych nVidia GeForce/Quadro
Name:		%{pname}%{?_pld_builder:%{?with_kernel:-kernel}}%{_alt_kernel}
Version:	173.14.39
Release:	%{rel}%{?_pld_builder:%{?with_kernel:@%{_kernel_ver_str}}}
License:	nVidia Binary
Group:		X11
Source0:	http://us.download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}-pkg1.run
# Source0-md5:	bb98039d178cbfe6219c13993090017d
Source1:	http://us.download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}-pkg2.run
# Source1-md5:	d8a4aa520d0cc9e11cee8c4e94684fc6
Source2:	%{pname}-xinitrc.sh
Source3:	10-nvidia.conf
Source4:	10-nvidia-modules.conf
Patch0:		X11-driver-nvidia-GL.patch
Patch1:		X11-driver-nvidia-legacy-desktop.patch
Patch2:		nvidia-blacklist-vga-pmu-registers-195.patch
URL:		http://www.nvidia.com/object/unix.html
BuildRequires:	rpmbuild(macros) >= 1.678
%{?with_dist_kernel:%{expand:%kbrs}}
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	%{pname}-libs = %{epoch}:%{version}-%{rel}
Requires:	xorg-xserver-server
Requires:	xorg-xserver-server(videodrv-abi) <= 15.0
Requires:	xorg-xserver-server(videodrv-abi) >= 2.0
Provides:	xorg-driver-video
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
Obsoletes:	X11-OpenGL-core < 1:7.0.0
Obsoletes:	X11-OpenGL-libGL < 1:7.0.0
Obsoletes:	XFree86-OpenGL-core < 1:7.0.0
Obsoletes:	XFree86-OpenGL-libGL < 1:7.0.0

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
Requires:	%{pname} = %{epoch}:%{version}
Suggests:	pkgconfig
Obsoletes:	XFree86-driver-nvidia-progs

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l hu.UTF-8
Eszközök az nVidia grafikus kártyák beállításához.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-video-nvidia-legacy3\
Summary:	nVidia kernel module for nVidia Architecture support\
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung\
Summary(hu.UTF-8):	nVidia Architektúra támogatás Linux kernelhez\
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
Requires:	dev >= 2.7.7-10\
%if %{with dist_kernel}\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
%endif\
Requires:	%{pname} = %{epoch}:%{version}\
Provides:	X11-driver-nvidia(kernel)\
Obsoletes:	XFree86-nvidia-kernel\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy3\
nVidia Architecture support for Linux kernel.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l de.UTF-8\
Die nVidia-Architektur-Unterstützung für den Linux-Kern.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l hu.UTF-8\
nVidia Architektúra támogatás Linux kernelhez.\
\
%description -n kernel%{_alt_kernel}-video-nvidia-legacy3 -l pl.UTF-8\
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez\
sterownik nVidii dla Xorg/XFree86.\
\
%files -n kernel%{_alt_kernel}-video-nvidia-legacy3\
%defattr(644,root,root,755)\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
\
%post	-n kernel%{_alt_kernel}-video-nvidia-legacy3\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-video-nvidia-legacy3\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
cd usr/src/nv\
ln -sf Makefile.kbuild Makefile\
%{__make} SYSSRC=%{_kernelsrcdir} clean\
ln -sf Makefile.kbuild Makefile\
%{__make} SYSSRC=%{_kernelsrcdir} module\
cd ../../..\
%install_kernel_modules -D installed -m usr/src/nv/nvidia -d misc\
#cat >> Makefile <<'EOF'\
#\
#$(obj)/nv-kernel.o: $(src)/nv-kernel.o.bin\
#	cp $< $@\
#EOF\
#mv nv-kernel.o{,.bin}\
#build_kernel_modules -m nvidia\
%{nil}

%{?with_kernel:%{expand:%kpkg}}

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86*-%{version}-pkg*
%ifarch %{ix86}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86-%{version}-pkg1
%else
/bin/sh %{SOURCE1} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{version}-pkg2
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{?with_kernel:%{expand:%bkpkg}}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/xorg/modules/{drivers,extensions/nvidia} \
	$RPM_BUILD_ROOT{%{_includedir}/GL,%{_libdir},%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},/etc/X11/xinit/xinitrc.d}
install -d $RPM_BUILD_ROOT{%{_libdir}/nvidia,%{_sysconfdir}/ld.so.conf.d}
install -d $RPM_BUILD_ROOT/etc/X11/xorg.conf.d

install -p usr/bin/nvidia-{settings,xconfig,bug-report.sh} $RPM_BUILD_ROOT%{_bindir}
cp -p usr/share/man/man1/nvidia-{settings,xconfig}.* $RPM_BUILD_ROOT%{_mandir}/man1
cp -p usr/share/applications/nvidia-settings.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p usr/share/pixmaps/nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh

install %{SOURCE3} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
install %{SOURCE4} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
sed -i -e 's|@@LIBDIR@@|%{_libdir}|g' $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/10-nvidia-modules.conf

for f in \
	usr/lib/tls/libnvidia-tls.so.%{version}		\
	usr/lib/libnvidia-cfg.so.%{version}		\
	usr/lib/libGL{,core}.so.%{version}		\
	usr/X11R6/lib/libXvMCNVIDIA.so.%{version}	\
	usr/X11R6/lib/libXvMCNVIDIA.a			\
; do
	install -p $f $RPM_BUILD_ROOT%{_libdir}/nvidia
done

install -p usr/X11R6/lib/modules/extensions/libglx.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia
install -p usr/X11R6/lib/modules/drivers/nvidia_drv.so \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so.%{version}
ln -s nvidia_drv.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/drivers/nvidia_drv.so
install -p usr/X11R6/lib/modules/libnvidia-wfb.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia

cp -p usr/include/GL/*.h $RPM_BUILD_ROOT%{_includedir}/GL

ln -sf libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libglx.so
ln -sf libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so

%ifarch %{x8664}
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia64.conf
%else
echo %{_libdir}/nvidia >$RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/nvidia.conf
%endif

# OpenGL ABI for Linux compatibility
ln -sf libGL.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so.1
ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/nvidia/libGL.so

ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libXvMCNVIDIA.so
ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/nvidia/libXvMCNVIDIA_dynamic.so.1

/sbin/ldconfig -n %{_libdir}/nvidia
/sbin/ldconfig -n %{_libdir}/xorg/modules/extensions/nvidia
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT
cp -a installed/* $RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
cat << 'EOF'
NOTE: You must also install kernel module for this driver to work
  kernel-video-nvidia-legacy3-%{version}

EOF

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE
%doc usr/share/doc/{README.txt,NVIDIA_Changelog,XF86Config.sample}
%dir %{_libdir}/xorg/modules/extensions/nvidia
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libglx.so
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so.*.*
%attr(755,root,root) %{_libdir}/xorg/modules/extensions/nvidia/libnvidia-wfb.so
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so.*
%attr(755,root,root) %{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
%{_sysconfdir}/X11/xorg.conf.d/10-nvidia-modules.conf

%files libs
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ld.so.conf.d/nvidia*.conf
%dir %{_libdir}/nvidia
%attr(755,root,root) %{_libdir}/nvidia/libGL.so.*.*
%attr(755,root,root) %ghost %{_libdir}/nvidia/libGL.so.1
%attr(755,root,root) %{_libdir}/nvidia/libGLcore.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libXvMCNVIDIA.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libXvMCNVIDIA_dynamic.so.1
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-cfg.so.*.*
%attr(755,root,root) %{_libdir}/nvidia/libnvidia-tls.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nvidia/libGL.so
%attr(755,root,root) %{_libdir}/nvidia/libXvMCNVIDIA.so
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h

%files static
%defattr(644,root,root,755)
%{_libdir}/nvidia/libXvMCNVIDIA.a

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
