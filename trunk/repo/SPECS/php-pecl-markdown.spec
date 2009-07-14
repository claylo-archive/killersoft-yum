# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%define php_config_opts %(php-config --configuration-options 2>/dev/null)
%define peclname %{lua:

name = "php-pecl-markdown"

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

Summary: PECL package for Markdown
Name: %{peclname}
Version: 0.1.0
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/markdown
Source: http://pecl.php.net/get/markdown-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php%{_dbg}
BuildRequires: php%{_dbg}
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
Markdown is an extension to parse a Markdown text, from a string or a file.

%prep
%setup -n markdown-%{version}

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

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/markdown.ini << 'EOF'
; Enable markdown extension
extension=markdown.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/markdown.ini << 'EOF'
; Enable markdown extension
extension=markdown.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/markdown.ini << 'EOF'
; Enable markdown extension
extension=markdown.so
EOF

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc COPYING CREDITS EXPERIMENTAL
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/markdown.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/markdown.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/markdown.ini
%{php_extdir}/markdown.so

%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Initial release 0.1.0


