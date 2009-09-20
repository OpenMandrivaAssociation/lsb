%define compat_version 3.2
%define compat_version1 3.0
%define compat_version2 2.0

Summary: The skeleton package defining packages needed for LSB compliance
Name: lsb
Version: 4.0
Release: %mkrel 1
License: GPL
Group: System/Base
URL: http://www.linuxbase.org
Source0: tmpdirlsb.sh
Source1: install_initd
Source2: remove_initd

BuildRoot: %{_tmppath}/%{name}-%{version}-root
Exclusivearch: %{ix86} ppc x86_64

%define lsb_arch ia32
%ifarch x86_64
%define lsb_arch amd64
%endif
%ifarch ppc
%define lsb_arch ppc32
%endif

Requires: lsb-core
# former lsb-cxx
Requires: libstdc++6
# former lsb-graphics
Requires: libx11 libxext libxi libxt libxtst
Requires: libxft freetype2 libxrender
# package doesn't provide anything arch neutral
Requires: %mklibname mesagl 1

# former lsb-desktop
Requires: libxml2 libgtk+2 libpng
Requires: cairo libpango1.0 libfontconfig
Requires: qt3-common

# former lsb-qt4
Requires: qt4-common >= 4.2.3
Requires: qtopengllib >= 4.2.3
Requires: qtsvglib >= 4.2.3
Requires: qtnetworklib >= 4.2.3

# interpreted languages
Requires: perl perl-CGI python

# printing
Requires: libcups1 ghostscript foomatic-filters cups-common

Provides: lsb-noarch = %{version} 
Provides: lsb-%{lsb_arch} = %{version} 

Provides: lsb-noarch = %{compat_version}
Provides: lsb-%{lsb_arch} = %{compat_version} 
Provides: lsb-noarch = %{compat_version1}
Provides: lsb-%{lsb_arch} = %{compat_version1} 
Provides: lsb-cxx-noarch = %{compat_version}
Provides: lsb-cxx-%{lsb_arch} = %{compat_version}
Provides: lsb-graphics-noarch = %{compat_version}
Provides: lsb-graphics-%{lsb_arch} = %{compat_version}

Provides: lsb-qt4-noarch = %{version}
Provides: lsb-qt4-%{lsb_arch} = %{version}

Conflicts: lsb-release < 2.0-2mdk

Provides: lsb-cxx
Obsoletes: lsb-cxx
Provides: lsb-graphics
Obsoletes: lsb-graphics
Provides: lsb-desktop
Obsoletes: lsb-desktop
Provides: lsb-desktop-qt4
Obsoletes: lsb-desktop-qt4

%description
The skeleton package defining packages needed for LSB compliance.
Note: To successfuly run the runtime test suites, install lsb-test.

%package core
Summary: Core requirements needed for LSB compliance
Group: System/Base

Requires: pax lsb-release make sendmail-command ed glibc_lsb
Requires: binutils bc nail at m4 patch
Requires: vim-enhanced diffutils file gettext chkconfig
Requires: mtools /etc/sgml
Requires(pre):		rpm-helper
Requires(postun):	rpm-helper

Provides: lsb-core-noarch = %{version} 
Provides: lsb-core-%{lsb_arch} = %{version} 
Provides: lsb-core-noarch = %{compat_version}
Provides: lsb-core-%{lsb_arch} = %{compat_version} 
Provides: lsb-core-noarch = %{compat_version1}
Provides: lsb-core-%{lsb_arch} = %{compat_version1} 

%description core
The core requirements for LSB compliance.

%package test
Summary: Requirements needed to successfully run the LSB runtime tests
Group: System/Base

Requires: lsb
Requires: perl-DBI perl-devel perl-XML-Parser glibc-i18ndata
Requires: locales-de locales-en locales-es locales-fr locales-is
Requires: locales-it locales-ja locales-se locales-ta locales-zh 
Requires: xlsfonts gcc rgb java-1.6.0-openjdk mkfontdir wget
Requires: perl-doc hplip-hpijs qt4-database-plugin-sqlite
Requires: libx11-common qt3-Sqlite iceauth slocate

%description test
This packages pulls in additional packages not specified by LSB, but
required to successfully run the LSB runtime tests.

%prep
#%setup -q

%install
cat << EOF > README.urpmi
To run the LSB binary test suite, download the latest version from
ftp://ftp.freestandards.org/pub/lsb/test_suites/released/binary/runtime/
and install the rpms.
 
For lsb-runtime-test, log in as user vsx0 and use the command 'run_tests'.
The other tests give instructions in the %%post output at package install.

Note1: When prompted for the 'Block special filename' in the test
       interview, use /home/tet/test_sets/nonexistb, rather than
       /dev/sda. 
Note2: Additionally, if you have partitions containing /tmp or /home
       that are mounted with 'noatime', this option should be changed
       to 'atime' or you will see additional test failures.
Note3: You should also note that using the fstab option 'acl' for
       Posix ACLs will generate 1 test failure.  This is not enabled
       by default.
EOF

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT/%{_datadir}/nls
install -d $RPM_BUILD_ROOT/%{_datadir}/tmac
install -d $RPM_BUILD_ROOT/var/cache/fonts
install -d $RPM_BUILD_ROOT/var/games
install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT/lib/%{name}
install -d $RPM_BUILD_ROOT%{_prefix}/lib/%{name}
install -d $RPM_BUILD_ROOT/srv
install -d $RPM_BUILD_ROOT%{_sysconfdir}/opt
install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 755 %SOURCE0 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 755 %SOURCE1 $RPM_BUILD_ROOT%{_prefix}/lib/%{name}
install -m 755 %SOURCE2 $RPM_BUILD_ROOT%{_prefix}/lib/%{name}

# lsb-3.1-foo is in lsb-release
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{compat_version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{compat_version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{compat_version1}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/lsb-%{compat_version1}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{compat_version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{compat_version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{compat_version1}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/core-%{compat_version1}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/cxx-%{compat_version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/cxx-%{compat_version}-noarch
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/graphics-%{compat_version}-%{lsb_arch}
touch $RPM_BUILD_ROOT%{_sysconfdir}/lsb-release.d/graphics-%{compat_version}-noarch

cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/root-ulimit.sh
#!/bin/sh
# enable a nonzero core file value for root (exec_A test issues)
[ "\$UID" = "0" ] && ulimit -c 1000 > /dev/null 2>&1
EOF

cat << EOF > $RPM_BUILD_ROOT%{_bindir}/lsbinstall
#!/bin/sh
exit 0
EOF

cat << EOF > $RPM_BUILD_ROOT/sbin/fasthalt
#!/bin/sh
#start fasthalt
/sbin/halt -f
#end fasthalt
EOF

cat << EOF > $RPM_BUILD_ROOT/sbin/fastboot
#!/bin/sh
#start fastboot
/sbin/reboot -f
#end fastboot
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/hosts.equiv
# Sample hosts.equiv file for LSB compliance
# see man hosts.equiv for usage.
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/hosts.lpd
#
# hosts.lpd     This file describes the names of the hosts which are
#               allowed to use the remote printer services of this
#               host.  This file is used by the LPD subsystem.
#		Added for LSB compiance.
EOF

cat << EOF > $RPM_BUILD_ROOT/etc/gateways
# sample gateways file for LSB compliance. Database of gateways
# used by routed. Sample format shown below.
# [ net | host ] name1 gateway name2 metric value [ passive | active | external ]
EOF

chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/root-ulimit.sh
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/lsbinstall
chmod 0755 $RPM_BUILD_ROOT/sbin/fastboot
chmod 0755 $RPM_BUILD_ROOT/sbin/fasthalt
chmod 0644 $RPM_BUILD_ROOT/etc/hosts.equiv
chmod 0644 $RPM_BUILD_ROOT/etc/hosts.lpd
chmod 0644 $RPM_BUILD_ROOT/etc/gateways

# (sb) concession for lsb-apache to run
%pre core
%_pre_groupadd nobody

%postun core
%_postun_groupdel nobody

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{version}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{compat_version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{compat_version}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{compat_version1}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{compat_version1}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/cxx-%{compat_version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/cxx-%{compat_version}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/graphics-%{compat_version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/graphics-%{compat_version}-%{lsb_arch}

%files core
%defattr(-, root, root)
%{_datadir}/nls
%{_datadir}/tmac
/var/cache/fonts
/var/games
/sbin/fasthalt
/sbin/fastboot
%{_bindir}/lsbinstall
%dir %{_sysconfdir}/opt
%dir /srv
%dir /lib/%{name}
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/install_initd
%{_prefix}/lib/%{name}/remove_initd
%config(noreplace) %{_sysconfdir}/hosts.equiv
%config(noreplace) %{_sysconfdir}/hosts.lpd
%config(noreplace) %{_sysconfdir}/gateways
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{version}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{compat_version}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{compat_version}-%{lsb_arch}
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{compat_version1}-noarch
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-%{compat_version1}-%{lsb_arch}

%files test
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/profile.d/tmpdirlsb.sh
%config(noreplace) %{_sysconfdir}/profile.d/root-ulimit.sh

