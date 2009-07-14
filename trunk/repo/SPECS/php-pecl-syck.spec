# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define _dbg %{nil}
%define peclname %{lua:

name = "php-pecl-syck"

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

Summary: PECL package for Syck
Name: %{peclname}
Version: 0.9.3
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/syck
Source: http://pecl.php.net/get/syck-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}, syck
BuildRequires: php%{_dbg}, php%{_dbg}-devel, syck-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
YAML-1.0 parser and emitter. YAML s a straightforward machine parsable data 
serialization format designed for human readability and interaction with 
scripting languages. YAML is optimized for data serialization, 
configuration settings, log files, Internet messaging and filtering.

%prep
%setup -n syck-%{version}

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

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/syck.ini << 'EOF'
; Enable syck extension
extension=syck.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/syck.ini << 'EOF'
; Enable syck extension
extension=syck.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/syck.ini << 'EOF'
; Enable syck extension
extension=syck.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGELOG TODO
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/syck.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/syck.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/syck.ini
%{php_extdir}/syck.so

%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Initial release 0.9.3


