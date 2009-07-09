# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

Summary: PECL package providing tracing and profiling functionality
Name: php-pecl-xdebug
Version: 2.0.4
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/xdebug
Source: http://pecl.php.net/get/xdebug-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
BuildRequires: php, php-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
The Xdebug extension helps you debugging your script by providing a lot of
valuable debug information. Xdebug can provide the following:

- stack and function traces in error messages with:
- full parameter display for user defined functions
- function name, file name and line indications
- support for member functions
- memory allocation
- protection for infinite recursions
- profiling information for PHP scripts
- code coverage analysis
- capabilities to debug your scripts interactively with a debug client


%prep
%setup -n xdebug-%{version}


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

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/xdebug.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_extdir}/xdebug.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/xdebug.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_extdir}/xdebug.so
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/xdebug.ini << 'EOF'
; Enable xdebug extension module
zend_extension=%{php_extdir}/xdebug.so
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc CREDITS README LICENSE
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/xdebug.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/xdebug.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/xdebug.ini
%{php_extdir}/xdebug.so


%changelog
* Thu Jul  9 2009 Clay Loveless <clay@killersoft.com>
- Rebuilding for multiple config locations

* Tue Jan 06 2009 Rob Richards <rob@mashery.com>
- Update to 2.0.4

* Wed Apr 23 2008 Rob Richards <rob@mashery.com>
- Initial release 2.0.3
