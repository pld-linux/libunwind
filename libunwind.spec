Summary:	libunwind - a (mostly) platform-independent unwind API
Summary(pl):	libunwind - (prawie) niezale�ne od platformy API do rozwijania
Name:		libunwind
Version:	0.98.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	ftp://ftp.hpl.hp.com/pub/linux-ia64/%{name}-%{version}.tar.gz
# Source0-md5:	a145a46003930b6382a11b125eef4cb4
Patch0:		%{name}-gcc4.patch
URL:		http://www.hpl.hp.com/research/linux/libunwind/
%ifarch %{x8664}
BuildRequires:	binutils >= 2:2.15.94.0.2.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.213
ExclusiveArch:	%{ix86} %{x8664} hppa ia64
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
%patch0 -p1

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
