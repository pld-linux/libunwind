Summary:	libunwind - a (mostly) platform-independent unwind API
Summary(pl):	libunwind - (prawie) niezale�ne od platformy API do rozwijania
Name:		libunwind
Version:	0.98.4
Release:	1
License:	MIT
Group:		Libraries
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/%{name}-%{version}.tar.gz
# Source0-md5:	5ba6d6b92e4a6c84f9d986ea3cbeb5b3
URL:		http://www.hpl.hp.com/research/linux/libunwind/
%ifarch amd64
BuildRequires:	sed >= 4.0
%endif
ExclusiveArch:	%{ix86} amd64 hppa ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of the libunwind project is to define a portable and
efficient C programming interface (API) to determine the call-chain
of a program.
 
%description -l pl
Celem projektu libunwind jest zdefiniowanie przeno�nego i wydajnego
API w j�zyku C do okre�lania �a�cucha wywo�a� w programie.

%package devel
Summary:	Header files for libunwind library
Summary(pl):	Pliki nag��wkowe biblioteki libunwind
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libunwind library.

%description devel -l pl
Pliki nag��wkowe biblioteki libunwind.

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

%ifarch amd64
# workaround - don't use protected due to gas/584
sed -i -e 's/__attribute__((visibility ("protected")))//' include/internal.h
%endif

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
