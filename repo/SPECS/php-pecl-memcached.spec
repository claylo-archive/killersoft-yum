# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define _dbg %{nil}
%define peclname %{lua:

name = "php-pecl-memcached"

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

Summary: PECL package for memcached
Name: %{peclname}
Version: 1.0.0
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/memcached
Source: http://pecl.php.net/get/memcached-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}
BuildRequires: php%{_dbg}, php%{_dbg}-devel, memcached-devel, libmemcached-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
This extension uses libmemcached library to provide API for communicating 
with memcached servers.

%prep
%setup -n memcached-%{version}


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
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cgi.d/extensions
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cli.d/extensions

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/memcached.ini << 'EOF'
; Enable memcached extension
extension=memcached.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/memcached.ini << 'EOF'
; Enable memcached extension
extension=memcached.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/memcached.ini << 'EOF'
; Enable memcached extension
extension=memcached.so
EOF

%clean
%{__rm} -rf %{buildroot}

# CREDITS  ChangeLog  EXPERIMENTAL  LICENSE  README.markdown  config.m4  config.w32  memcached-api.php  php_memcached.c  php_memcached.h
%files
%defattr(-, root, root, 0755)
%doc CREDITS ChangeLog EXPERIMENTAL LICENSE README.markdown
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/memcached.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/memcached.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/memcached.ini
%{php_extdir}/memcached.so


%changelog
* Wed Jul  8 2009 Clay Loveless <clay@killersoft.com>
- Initial release
