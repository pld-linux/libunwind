Summary:	libunwind - a (mostly) platform-independent unwind API
Summary(pl):	libunwind - (prawie) niezale¿ne od platformy API do rozwijania
Name:		libunwind
Version:	0.98.3
Release:	1
License:	MIT
Group:		Libraries
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/%{name}-%{version}.tar.gz
# Source0-md5:	e6daa3498b80c00888276fb5292f18bd
URL:		http://www.hpl.hp.com/research/linux/libunwind/
ExclusiveArch:	%{ix86} amd64 hppa ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of the libunwind project is to define a portable and
efficient C programming interface (API) to determine the call-chain
of a program.
 
%description -l pl
Celem projektu libunwind jest zdefiniowanie przeno¶nego i wydajnego
API w jêzyku C do okre¶lania ³añcucha wywo³añ w programie.

%package devel
Summary:	Header files for libunwind library
Summary(pl):	Pliki nag³ówkowe biblioteki libunwind
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libunwind library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libunwind.

%package static
Summary:	Static libunwind library
Summary(pl):	Statyczna biblioteka libunwind
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libunwind library.

%description static -l pl
Statyczna biblioteka libunwind.

%prep
%setup -q

%build
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
%attr(755,root,root) %{_libdir}/libunwind*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunwind*.so
%{_libdir}/libunwind*.la
%{_includedir}/*unwind*.h
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libunwind*.a
