# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define peclname %{lua:

name = "php-pecl-spidermonkey"

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

Summary: PECL package for spidermonkey
Name: %{peclname}
Version: 0.1.2
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/spidermonkey
Source: http://pecl.php.net/get/spidermonkey-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}, js
BuildRequires: php%{_dbg}, php%{_dbg}-devel, js-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
This PHP extension allows you to embed Mozilla's JavaScript engine
Spidermonkey in PHP.

%prep
%setup -n spidermonkey-%{version}

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

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/spidermonkey.ini << 'EOF'
; Enable spidermonkey extension
extension=spidermonkey.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/spidermonkey.ini << 'EOF'
; Enable spidermonkey extension
extension=spidermonkey.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/spidermonkey.ini << 'EOF'
; Enable spidermonkey extension
extension=spidermonkey.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/spidermonkey.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/spidermonkey.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/spidermonkey.ini
%{php_extdir}/spidermonkey.so

%changelog
* Mon Jul  6 2009 Clay Loveless <clay@killersoft.com>
- Initial release 0.1.2


