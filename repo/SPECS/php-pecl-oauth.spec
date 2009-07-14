# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define _dbg %{nil}
%define peclname %{lua:

name = "php-pecl-oauth"

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

Summary: PECL package for  OAuth
Name: %{peclname}
Version: 0.99.9
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/oauth
Source: http://pecl.php.net/get/oauth-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}, curl
BuildRequires: php%{_dbg}, curl-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
OAuth is an authorization protocol built on top of HTTP which allows 
applications to securely access data without having to store 
usernames and passwords.

%prep
%setup -n oauth-%{version}

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

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/oauth.ini << 'EOF'
; Enable oauth extension
extension=oauth.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/oauth.ini << 'EOF'
; Enable oauth extension
extension=oauth.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/oauth.ini << 'EOF'
; Enable oauth extension
extension=oauth.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc LICENSE
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/oauth.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/oauth.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/oauth.ini
%{php_extdir}/oauth.so

%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Initial release 0.99.9


