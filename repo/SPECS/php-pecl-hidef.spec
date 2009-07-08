# $Id$
%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)

Summary: PECL package for hidef
Name: php-pecl-hidef
Version: 0.1.1
Release: 1
License: PHP
Group: Development/Languages
URL: http://pecl.php.net/package/hidef
Source: http://pecl.php.net/get/hidef-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: php
BuildRequires: php, php-devel
# Required by phpize
BuildRequires: autoconf213, automake, libtool, gcc-c++

%description
This PHP extension allows definition of user defined constants in simple ini
files, which are then processed like internal constants, without any of 
the usual performance penalties.

%prep
%setup -n hidef-%{version}


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
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.mod.d/extensions/hidef.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/hidef.d
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.cli.d/extensions/hidef.d

%{__cat} > %{buildroot}%{_sysconfdir}/php.mod.d/extensions/hidef.ini << 'EOF'
; Enable hidef extension
extension=hidef.so
hidef.ini_path=%{_sysconfdir}/php.mod.d/extensions/hidef.d/
hidef.data_path=%{_sysconfdir}/php.mod.d/extensions/hidef.d/
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cli.d/extensions/hidef.ini << 'EOF'
; Enable hidef extension
extension=hidef.so
hidef.ini_path=%{_sysconfdir}/php.cli.d/extensions/hidef.d/
hidef.data_path=%{_sysconfdir}/php.cli.d/extensions/hidef.d/
EOF
%{__cat} > %{buildroot}%{_sysconfdir}/php.cgi.d/extensions/hidef.ini << 'EOF'
; Enable hidef extension
extension=hidef.so
hidef.ini_path=%{_sysconfdir}/php.cgi.d/extensions/hidef.d/
hidef.data_path=%{_sysconfdir}/php.cgi.d/extensions/hidef.d/
EOF

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc INSTALL
%dir %{_sysconfdir}/php.mod.d/extensions/hidef.d
%dir %{_sysconfdir}/php.cli.d/extensions/hidef.d
%dir %{_sysconfdir}/php.cgi.d/extensions/hidef.d
%config(noreplace) %{_sysconfdir}/php.mod.d/extensions/hidef.ini
%config(noreplace) %{_sysconfdir}/php.cli.d/extensions/hidef.ini
%config(noreplace) %{_sysconfdir}/php.cgi.d/extensions/hidef.ini
%{php_extdir}/hidef.so


%changelog
* Wed Jul  8 2009 Clay Loveless <clay@killersoft.com>
- Added cli/cgi/mod_php config dirs

* Tue Jan 06 2009 Rob Richards <rob@mashery.com>
- Update to 0.1.1

* Wed Aug 27 2008 Rob Richards <rob@mashery.com>
- Add mashery.ini and contents

* Wed May 30 2008 Clay Loveless <clay@mashery.com>
- Initial build 0.1.0
