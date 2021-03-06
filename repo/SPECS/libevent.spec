# $Id$
Name:           libevent
Version:        1.4.12
Release:        1
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://monkey.org/~provos/libevent/
Source0:        http://monkey.org/~provos/libevent-%{version}-stable.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-stable-%{release}-root-%(%{__id_u} -n)

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}-%{version}-stable

%build
%configure \
    --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make verify

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*

%files devel
%defattr(-,root,root,0755)
%doc sample/*.c
%{_includedir}/event.h
%{_includedir}/evdns.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_includedir}/event-config.h
%{_libdir}/libevent*

%{_bindir}/event_rpcgen.py
%exclude %{_bindir}/event_rpcgen.pyc
%exclude %{_bindir}/event_rpcgen.pyo

%{_mandir}/man3/*

%changelog
* Tue Aug 11 2009 Clay Loveless <clay@killersoft.com>
- Updated for version 1.4.12-stable

* Sun Jun 28 2009 Clay Loveless <clay@killersoft.com>
- Updated for version 1.4.11-stable

* Tue Apr 22 2008 Rob Richards <rob@mashery.com> - 1.3e-3
- rebuild for centos

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3e-2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Steve Dickson <steved@redhat.com> 1.3e-1
- Updated to latest stable upstream version 1.3e

* Fri Mar  9 2007 Steve Dickson <steved@redhat.com> 1.3b-1
- Updated to latest upstream version 1.3b
- Incorporated Merge Review comments (bz 226002)
- Increased the polling timeout (bz 204990)

* Tue Feb 20 2007 Steve Dickson <steved@redhat.com> 1.2a-1
- Updated to latest upstream version 1.2a

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> - 1.1a-3
- rebuild (#177697)

* Mon Jul 04 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-2
- Removed unnecessary -r from rm

* Fri Jun 17 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-1
- Upstream update

* Wed Jun 08 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-2
- Added some docs
- Moved "make verify" into %%check

* Mon Jun 06 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-1
- Initial build for Fedora Extras, based on the package
  by Dag Wieers
