# $Id$
%define optflags -g -O2
Name:           memcached
Version:        1.4.0
Release:        1
Summary:        High Performance, Distributed Memory Object Cache

Group:          System Environment/Daemons
License:        BSD
URL:            http://www.danga.com/memcached/
Source0:        http://www.danga.com/memcached/dist/%{name}-%{version}-rc1.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libevent-devel
BuildRequires:  perl(Test::More)
Requires: initscripts
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service

%description
memcached is a high-performance, distributed memory object caching
system, generic in nature, but intended for use in speeding up dynamic
web applications by alleviating database load.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%prep
%setup -q -n %{name}-%{version}-rc1


%build
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
%configure --disable-dependency-tracking
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# remove memcached-debug
rm -f %{buildroot}/%{_bindir}/memcached-debug

# Perl script for monitoring memcached
install -Dp -m0755 scripts/memcached-tool %{buildroot}%{_bindir}/memcached-tool

# Init script
install -Dp -m0755 scripts/memcached.sysv %{buildroot}%{_initrddir}/memcached

# Default configs
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cat <<EOF >%{buildroot}/%{_sysconfdir}/sysconfig/%{name}
PORT="11211"
USER="nobody"
MAXCONN="1024"
CACHESIZE="64"
OPTIONS=""
EOF

# pid directory
mkdir -p %{buildroot}/%{_localstatedir}/run/memcached

%clean
rm -rf %{buildroot}


%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop > /dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0

%postun
if [ "$1" -ge 1 ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1
fi
exit 0


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO doc/CONTRIBUTORS doc/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(750,nobody,nobody) %{_localstatedir}/run/memcached
%{_bindir}/memcached-tool
%{_bindir}/memcached
%{_mandir}/man1/memcached.1*
%{_initrddir}/memcached

%files devel
%defattr(-,root,root,0755)
%{_includedir}/memcached/*.h



%changelog
* Tue Aug 11 2009 Clay Loveless <clay@killersoft.com> 1.4.0-1
- Updated to 1.4.0 release.

* Wed Jul  8 2009 Clay Loveless <clay@killersoft.com> 1.4.0-rc1-2
- Fixed file list between regular and devel packages

* Sun Jun 28 2009 Clay Loveless <clay@killersoft.com> 1.4.0-rc1-1
- Updated for 1.4.0-rc1

* Wed Jul  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-5
- Use /var/run/memcached/ directory to hold PID file

* Sat May 12 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-4
- Remove tabs from spec file, rpmlint reports no more errors

* Thu May 10 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-3
- Enable build-time regression tests
- add dependency on initscripts
- remove memcached-debug (not needed in dist)
- above suggestions from Bernard Johnson

* Mon May  7 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-2
- Tidyness improvements suggested by Ruben Kerkhof in bugzilla #238994

* Fri May  4 2007 Paul Lindner <lindner@inuus.com> - 1.2.2-1
- Initial spec file created via rpmdev-newspec