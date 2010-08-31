Summary:	libunwind - a (mostly) platform-independent unwind API
Summary(pl.UTF-8):	libunwind - (prawie) niezależne od platformy API do rozwijania
Name:		libunwind
Version:	0.99
Release:	2
License:	MIT
Group:		Libraries
Source0:	http://download.savannah.gnu.org/releases/libunwind/%{name}-%{version}.tar.gz
# Source0-md5:	3e9ca08118e22165a7f07d01d61a2d0d
Patch0:		%{name}-disable-setjmp.patch
URL:		http://www.nongnu.org/libunwind/
BuildRequires:  autoconf
BuildRequires:  automake >= 1.6
%ifarch %{x8664}
BuildRequires:	binutils >= 2:2.15.94.0.2.2
%endif
BuildRequires:  libtool
BuildRequires:	rpmbuild(macros) >= 1.213
ExclusiveArch:	%{ix86} %{x8664} hppa ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# x86/x86_64/hppa/ia64
%ifarch	%{ix86}
%define	asuf	x86
%else
%ifarch	%{x8664}
%define	asuf	x86_64
%else
%define	asuf	%{_target_cpu}
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
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libunwind library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libunwind.

%package static
Summary:	Static libunwind library
Summary(pl.UTF-8):	Statyczna biblioteka libunwind
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libunwind library.

%description static -l pl.UTF-8
Statyczna biblioteka libunwind.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libunwind.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind.so.7
%attr(755,root,root) %{_libdir}/libunwind-%{asuf}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunwind-%{asuf}.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunwind.so
%attr(755,root,root) %{_libdir}/libunwind-generic.so
%attr(755,root,root) %{_libdir}/libunwind-%{asuf}.so
%{_libdir}/libunwind.la
%{_libdir}/libunwind-%{asuf}.la
# static-only
%{_libdir}/libunwind-ptrace.a
%{_includedir}/libunwind*.h
%{_includedir}/unwind.h
%{_mandir}/man3/_U_dyn_*.3*
%{_mandir}/man3/libunwind*.3*
%{_mandir}/man3/unw_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libunwind.a
%{_libdir}/libunwind-generic.a
%{_libdir}/libunwind-%{asuf}.a
