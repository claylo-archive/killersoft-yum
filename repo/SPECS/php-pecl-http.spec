# $Id$
# yum install -y libssh2-devel openssl-devel libidn-devel openldap-devel c-ares-devel gnutls-devel curl-devel php-devel
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define _dbg %{nil}
%define peclname %{lua:

name = "php-pecl-http"

php_config_opts = rpm.expand("%{php_config_opts}")
if (string.find(php_config_opts, "--enable-debug", 1, true)) then
  name = "php-dbg" .. string.sub(name, 4)
end
print(name)
}
%{lua: 
current_name = rpm.expand("%{peclname}")
if (string.find(current_name, "-dbg", 1, true)) then
  rpm.define("_dbg -dbg")
end
}

Summary: PECL package to handle HTTP/HTTPS requests
Name: %{peclname}
Version: 1.6.3
Release: 3
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/pecl_http
Source: http://pecl.php.net/get/pecl_http-%{version}.tgz
Patch0: pecl_http-1.6.3.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}, curl
BuildRequires: php%{_dbg}, php%{_dbg}-devel, curl-devel, c-ares-devel, libidn-devel, openldap-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
This HTTP extension aims to provide a convenient and powerful 
set of functionality for one of PHPs major applications.

It eases handling of HTTP urls, dates, redirects, headers and 
messages, provides means for negotiation of clients preferred 
language and charset, as well as a convenient way to send any 
arbitrary data with caching and resuming capabilities.

It provides powerful request functionality, if built with CURL 
support. Parallel requests are available for PHP 5 and greater.


%prep
%setup -n pecl_http-%{version}
%patch0 -p1

%build
# Workaround for broken old phpize on 64 bits
%{__cat} %{_bindir}/phpize | sed 's|/lib/|/%{_lib}/|g' > phpize && sh phpize
%configure --with-http-curl-requests --with-http-curl-libevent --with-http-zlib-compression
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.mod.d/extensions
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cgi.d/extensions
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cli.d/extensions

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/http.ini << 'EOF'
; Enable http extension module
extension=http.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/http.ini << 'EOF'
; Enable http extension module
extension=http.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/http.ini << 'EOF'
; Enable http extension module
extension=http.so
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc CREDITS LICENSE
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/http.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/http.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/http.ini
%{php_extdir}/http.so
%{_includedir}/php/ext/http/*

%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Rebuild for Killersoft repo, added additional cli and mod_php configs

* Wed Mar 18 2009 Rob Richards <rob@mashery.com>
- Updated patch for mem corruption in http_message_api.c/http_message_object.c

* Tue Mar 17 2009 Rob Richards <rob@mashery.com>
- Update to release 1.6.3
- Apply patch for mem corruption in http_message_api.c/http_message_object.c

* Fri Dec 19 2008 Rob Richards <rob@mashery.com>
- Update to release 1.6.2
- Mashery patch no longer needed

* Fri Aug 22 2008 Rob Richards <rob@mashery.com>
- Apply patch for mem corrupt http_request_api.c, v 1.164

* Mon Aug 04 2008 Rob Richards <rob@mashery.com>
- Update to release 1.6.1

* Wed Apr 23 2008 Rob Richards <rob@mashery.com>
- Initial release 1.6.0
