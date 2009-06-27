# $Id: c-ares.spec 10547 2008-08-24 00:23:35Z clay $
Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.6.0
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://c-ares.haxx.se/
Source0: http://c-ares.haxx.se/c-ares-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named 'ares', written 
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and static libraries needed to
compile applications or shared objects that use c-ares.

%prep
%setup -q

%build
%configure --enable-shared
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libcares.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libcares.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README README.cares CHANGES NEWS AUTHORS TODO RELEASE-NOTES
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/ares_*

%changelog
* Fri Jun 26 2009 Clay Loveless <clay@killersoft.com> 1.6.0-1
- Updated to 1.6.0

* Mon Apr 21 2008 Rob Richards <rob@mashery.com> 1.5.1-1
- Initial build 1.5.1
