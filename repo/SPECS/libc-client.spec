# $Id$
%define soname		c-client
%define somajver	1

Summary: C-client mail access routines for IMAP and POP protocols
Name: libc-client
Version: 2007e
Release: 2
License: University of Washington Free-Fork License
Group: System Environment/Daemons
URL: http://www.washington.edu/imap/

Source0: ftp://ftp.cac.washington.edu/mail/imap-%{version}.tar.gz

Buildroot: %{_tmppath}/%{name}-%{version}-root

BuildPrereq: krb5-devel, openssl-devel, pam-devel
# DO NOT REMOVE THIS PAM HEADER DEPENDANCY OR FACE THE WRATH
BuildPreReq: /usr/include/security/pam_modules.h
Requires: pam >= 0.59

%description
C-client is a common API for accessing mailboxes. It is used internally by
the popular PINE mail reader, the University of Washington's IMAP server
and PHP.

%package devel
Summary: Development tools for programs which will use the IMAP library.
Group: Development/Libraries
Conflicts: imap-devel
Requires: libc-client = %{version}-%{release}

%description devel
The c-client-devel package contains the header files and static libraries
for developing programs which will use the C-client common API.

%prep
%setup -q -n imap-%{version}
chmod -R u+w .

%build
# Set EXTRACFLAGS here instead of in imap-2000-redhat.patch (#20760)
EXTRACFLAGS="$EXTRACFLAGS -DDISABLE_POP_PROXY=1 -DIGNORE_LOCK_EACCES_ERRORS=1"
EXTRACFLAGS="$EXTRACFLAGS -I/usr/include/openssl"
EXTRACFLAGS="$EXTRACFLAGS -fPIC -fno-strict-aliasing"
EXTRACFLAGS="$EXTRACFLAGS -Wall -Wno-pointer-sign -Wno-parentheses"

make lnp \
EXTRACFLAGS="$EXTRACFLAGS" \
EXTRALDFLAGS="$EXTRALDFLAGS" \
EXTRAAUTHENTICATORS=gss \
IP6=4 \
# This line needs to be here.
#SSLTYPE=unix \

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m 644 ./c-client/c-client.a $RPM_BUILD_ROOT%{_libdir}/
ln -s c-client.a  $RPM_BUILD_ROOT%{_libdir}/libc-client.a

mkdir -p $RPM_BUILD_ROOT%{_includedir}/imap
install -m 644 ./c-client/*.h $RPM_BUILD_ROOT%{_includedir}/imap
# Added linkage.c to fix (#34658) <mharris>
install -m 644 ./c-client/linkage.c $RPM_BUILD_ROOT%{_includedir}/imap
install -m 644 ./src/osdep/tops-20/shortsym.h $RPM_BUILD_ROOT%{_includedir}/imap

# php friendly install
mkdir -p $RPM_BUILD_ROOT/usr/imap-%{version}/lib
mkdir -p $RPM_BUILD_ROOT/usr/imap-%{version}/include
install -m 644 -T ./c-client/c-client.a $RPM_BUILD_ROOT/usr/imap-%{version}/lib/libc-client.a
install -m 644 ./c-client/*.c $RPM_BUILD_ROOT/usr/imap-%{version}/lib
install -m 644 ./c-client/*.h $RPM_BUILD_ROOT/usr/imap-%{version}/include

#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/ssl/certs

# don't ship quite so many docs
rm -rf docs/rfc docs/FAQ.txt

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README docs/RELNOTES docs/*.txt
%doc docs/CONFIG docs/SSLBUILD
%{_libdir}/libc-client.a

%files devel
%defattr(-,root,root)
%doc docs/*
%{_includedir}/imap
%{_libdir}/c-client.a
%{_libdir}/libc-client.a
$RPM_BUILD_ROOT/usr/imap-%{version}

%changelog
* Thu Jul  2 2009 Clay Loveless <clay@killersoft.com>
- Added separate devel directory based on PHP docs
  http://www.php.net/manual/en/imap.requirements.php

* Sun Jun 28 2009 Clay Loveless <clay@killersoft.com>
- Updated to release 2007e

* Tue Apr 22 2008 Rob Richards <rob@mashery.com> - 2006k-2.4
- Initial release 2006k
