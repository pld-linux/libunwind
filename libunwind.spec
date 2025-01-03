#
# Conditional build:
%bcond_with 	tests		# perform "make check" (fails randomly)
%bcond_without	doc		# man pages
%bcond_without	static_libs	# static libraries
#
Summary:	libunwind - a (mostly) platform-independent unwind API
Summary(pl.UTF-8):	libunwind - (prawie) niezależne od platformy API do rozwijania
Name:		libunwind
Version:	1.8.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/libunwind/libunwind/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	10c96118ff30b88c9eeb6eac8e75599d
Patch0:		%{name}-x32.patch
URL:		https://github.com/libunwind/libunwind
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
%ifarch %{x8664}
BuildRequires:	binutils >= 2:2.15.94.0.2.2
%endif
%{?with_doc:BuildRequires:	latex2man}
BuildRequires:	libtool >= 2:2.0
BuildRequires:	rpmbuild(macros) >= 1.527
BuildRequires:	xz-devel
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 hppa ia64 mips ppc ppc64 sh tilegx
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# some setjmp tricks expect non-redirected functions
%define		filterout_cpp	-D_FORTIFY_SOURCE=[0-9]+

# x86/x86_64/hppa/ia64
%ifarch	%{ix86}
%define	asuf	x86
%else
%ifarch	%{x8664} x32
%define	asuf	x86_64
%else
%ifarch	%{arm}
%define	asuf	arm
%else
%define	asuf	%{_target_cpu}
%endif
%endif
%endif

%description
The goal of the libunwind project is to define a portable and
efficient C programming interface (API) to determine the call-chain
of a program.

%description -l pl.UTF-8
Celem projektu libunwind jest zdefiniowanie przenośnego i wydajnego
API w języku C do określania łańcucha wywołań w programie.

%package devel
Summary:	Header files for libunwind library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libunwind
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	xz-devel%{?_isa}

%description devel
Header files for libunwind library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libunwind.

%package static
Summary:	Static libunwind library
Summary(pl.UTF-8):	Statyczna biblioteka libunwind
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libunwind library.

%description static -l pl.UTF-8
Statyczna biblioteka libunwind.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# what needs additional -fPIC? libtool already uses it for shared objects
%configure \
	CFLAGS="%{rpmcflags} -fPIC" \
	%{!?with_doc:--disable-documentation} \
	--disable-silent-rules \
	%{!?with_tests:--disable-tests} \
	%{__enable_disable static_libs static}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with tests}
# don't package test stuff
%{__rm} -r $RPM_BUILD_ROOT%{_libexecdir}/libunwind
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libunwind.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind.so.8
%attr(755,root,root) %{_libdir}/libunwind-coredump.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind-coredump.so.0
%attr(755,root,root) %{_libdir}/libunwind-ptrace.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind-ptrace.so.0
%attr(755,root,root) %{_libdir}/libunwind-setjmp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind-setjmp.so.0
%attr(755,root,root) %{_libdir}/libunwind-%{asuf}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind-%{asuf}.so.8

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunwind.so
%attr(755,root,root) %{_libdir}/libunwind-coredump.so
%attr(755,root,root) %{_libdir}/libunwind-generic.so
%attr(755,root,root) %{_libdir}/libunwind-ptrace.so
%attr(755,root,root) %{_libdir}/libunwind-setjmp.so
%attr(755,root,root) %{_libdir}/libunwind-%{asuf}.so
%{_libdir}/libunwind.la
%{_libdir}/libunwind-coredump.la
%{_libdir}/libunwind-ptrace.la
%{_libdir}/libunwind-setjmp.la
%{_libdir}/libunwind-%{asuf}.la
%{_includedir}/libunwind*.h
%{_includedir}/unwind.h
%{_pkgconfigdir}/libunwind.pc
%{_pkgconfigdir}/libunwind-coredump.pc
%{_pkgconfigdir}/libunwind-generic.pc
%{_pkgconfigdir}/libunwind-ptrace.pc
%{_pkgconfigdir}/libunwind-setjmp.pc
%if %{with doc}
%{_mandir}/man3/_U_dyn_*.3*
%{_mandir}/man3/libunwind*.3*
%{_mandir}/man3/unw_*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libunwind.a
%{_libdir}/libunwind-coredump.a
%{_libdir}/libunwind-generic.a
%{_libdir}/libunwind-ptrace.a
%{_libdir}/libunwind-setjmp.a
%{_libdir}/libunwind-%{asuf}.a
%endif
