# $Id$

Summary: Killersoft release file and package configuration
Name: killersoft-release
Version: 0.1
Release: 1
License: GPL
Group: System Environment/Base
URL: http://code.google.com/p/killersoft-yum/

Packager: Clay Loveless <clay@killersoft.com>
Vendor: Killersoft Yum Repository, http://yum.killersoft.com/

Source0: mirrors-killersoft
Source1: RPM-GPG-KEY-killersoft
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Killersoft Yum Repository release installation. This package contains apt,
yum and smart configuration for the Killersoft RPM Repository, as well as
the public GPG keys used to sign them.

%prep
%setup -c

%{?el5:name='Red Hat Enterprise'; version='5'; path="redhat/el"}

%{__cat} <<EOF >killersoft.apt
# Name: RPMforge RPM Repository for $name $version
# URL: http://code.google.com/p/killersoft-yum/
#rpm http://yum.killersoft.com $path\$(VERSION)/en/\$(ARCH)
repomd http://yum.killersoft.com $path\$(VERSION)/en/\$(ARCH)
EOF

%{__cat} <<EOF >killersoft.smart
# Name: Killersoft RPM Repository for $name $version - %{_arch}
# URL: http://code.google.com/p/killersoft-yum/
[killersoft]
name = Extra packages from Killersoft for $name $version - %{_arch}
baseurl = http://yum.killersoft.com/$path$version/en/%{_arch}
type = rpm-md
EOF

%{__cat} <<EOF >killersoft.yum
# Name: Killersoft RPM Repository for $name $version
# URL: http://code.google.com/p/killersoft-yum/
[killersoft]
name = $name \$releasever - Killersoft
mirrorlist=http://cdn.killersoft.com/rpm/mirrors-killersoft
#mirrorlist = file:///etc/yum.repos.d/mirrors-killersoft
enabled = 1
protect = 0
gpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-killersoft
gpgcheck = 1
# set metadata to expire faster then main
metadata_expire=30
priority=10
tolerant=1
retries=10
EOF

%{__cat} <<EOF >killersoft.up2date
# Name: Killersoft RPM Repository for $name $version - %{_arch}
# URL: http://code.google.com/p/killersoft-yum/
#
# Add the following line to /etc/sysconfig/rhn/sources
#
#       yum killersoft http://yum.killersoft.com/$path$version/en/%{_arch}
# or
#       apt killersoft http://yum.killersoft.com $path$version/en/%{_arch}
EOF

for mirror in $(%{__cat} %{SOURCE0}); do
    echo "$mirror/$path$version/en/\$ARCH"
done >mirrors-killersoft.yum

%build

%install
%{__rm} -rf %{buildroot}
%{__cp} -a %{SOURCE1} .
%{__install} -Dp -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-killersoft
%{__install} -Dp -m0644 killersoft.apt %{buildroot}%{_sysconfdir}/apt/sources.list.d/killersoft.list
%{__install} -Dp -m0644 killersoft.smart %{buildroot}%{_sysconfdir}/smart/channels/killersoft.channel
%{__install} -Dp -m0644 killersoft.up2date %{buildroot}%{_sysconfdir}/sysconfig/rhn/sources.killersoft.txt
%{__install} -Dp -m0644 killersoft.yum %{buildroot}%{_sysconfdir}/yum.repos.d/killersoft.repo
%{__install} -Dp -m0644 mirrors-killersoft.yum %{buildroot}%{_sysconfdir}/yum.repos.d/mirrors-killersoft

%clean
%{__rm} -rf %{buildroot}

%post
%if %{!?_without_rpmpubkey:1}0
rpm -q gpg-pubkey-d6259790-4a2f09d0 &>/dev/null || rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-killersoft || :
%endif

%files
%defattr(-, root, root, 0755)
%doc mirrors-killersoft.yum RPM-GPG-KEY-killersoft killersoft.*
%if %{!?_without_rpmpubkey:1}0
%pubkey RPM-GPG-KEY-killersoft
%endif
%dir %{_sysconfdir}/apt/
%dir %{_sysconfdir}/apt/sources.list.d/
%config(noreplace) %{_sysconfdir}/apt/sources.list.d/killersoft.list
%dir %{_sysconfdir}/smart/
%dir %{_sysconfdir}/smart/channels/
%config(noreplace) %{_sysconfdir}/smart/channels/killersoft.channel
%dir %{_sysconfdir}/sysconfig/rhn/
%config %{_sysconfdir}/sysconfig/rhn/sources.killersoft.txt
%dir %{_sysconfdir}/yum.repos.d/
%config(noreplace) %{_sysconfdir}/yum.repos.d/killersoft.repo
%config %{_sysconfdir}/yum.repos.d/mirrors-killersoft
%dir %{_sysconfdir}/pki/rpm-gpg/
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-killersoft

%changelog
* Thu Jun 11 2009 Clay Loveless <clay@killersoft.com> - 0.1-1
- Initial package. Based entirely off Dag's excellent rpmforge-releases
