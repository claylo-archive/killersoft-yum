Notes and version control for the public Killersoft Yum repository.

The Cliff's Notes to making use of the repository:

```
rpm --import http://cdn.killersoft.com/rpm/RPM-GPG-KEY.killersoft.txt
yum install yum-priorities
rpm -Uvh http://yum.killersoft.com/redhat/el5/en/noarch/killersoft-release-0.3-1.noarch.rpm
yum update
```

Foundational repositories:

[rpmforge](https://rpmrepo.org/RPMforge/Using)

[epel](http://fedoraproject.org/wiki/EPEL)

[centos](http://wiki.centos.org/AdditionalResources/Repositories)

The Killersoft yum repository has been designed with the best intentions of playing well with the other repositories it's based upon. If you find any issues, [please open a ticket](http://code.google.com/p/killersoft-yum/issues/list).