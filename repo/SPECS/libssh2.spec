# $Id: libssh2.spec 10547 2008-08-24 00:23:35Z clay $
Summary: Library implementing the SSH2 protocol
Name: libssh2
Version: 1.1
Release: 1
License: BSD
Group: System Environment/Libraries
URL: http://www.libssh2.org/

Source: http://dl.sf.net/sourceforge/libssh2/libssh2-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: pkgconfig, openssl-devel, zlib-devel

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup

#%{__perl} -pi.orig -e 's|/lib\b|/%{_lib}|g;' configure Makefile.in */Makefile.in

%build
%configure \
    --with-openssl=/usr --with-zlib=/usr
#%{__make} %{?_smp_mflags} CFLAGS="%{optflags} -pipe -I../include/ -fPIC"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING HACKING NEWS README
%{_libdir}/libssh2.so.*

%files devel
%defattr(-, root, root, 0755)
%doc example/
%doc %{_mandir}/man3/*.3*
%{_libdir}/libssh2.so
%{_libdir}/libssh2.a
%{_includedir}/libssh2*.h
%exclude %{_libdir}/libssh2.la

%changelog
* Sat Jun 27 2009 Clay Loveless <clay@killersoft.com>
- Upgraded to 1.1

* Mon Apr 21 2008 Dag Rob Richards <rob@mashery.com> - 0.17-1
- Release 0.17.