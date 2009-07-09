# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

Summary: PECL package for working with geoip
Name: php-pecl-geoip
Version: 1.0.7
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/geoip
Source: http://pecl.php.net/get/geoip-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php, GeoIP
BuildRequires: php, php-devel, GeoIP-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
This PHP extension allows you to find the location of an IP address 
- City, State, Country, Longitude, Latitude, and other information as all, 
such as ISP and connection type. For more info, please visit Maxmind's website.

%prep
%setup -n geoip-%{version}


%build
# Workaround for broken old phpize on 64 bits
%{__cat} %{_bindir}/phpize | sed 's|/lib/|/%{_lib}/|g' > phpize && sh phpize
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.mod.d/extensions
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cli.d/extensions
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cgi.d/extensions

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/geoip.ini << 'EOF'
; Enable geoip extension module
extension=geoip.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/geoip.ini << 'EOF'
; Enable geoip extension module
extension=geoip.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/geoip.ini << 'EOF'
; Enable geoip extension module
extension=geoip.so
EOF

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc README ChangeLog
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/geoip.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/geoip.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/geoip.ini
%{php_extdir}/geoip.so


%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Initial 1.0.7 build w/multi-sapi configs.
