%define compat_versions 2.0 3.0 3.1 3.2 4.0
%define modular_versions 3.1 3.2

# populate the Provides for the compat versions and the old 3.x modular setup
# this way we only have to change the lists above when we bump up 
# (at least until LSB drops something, or we choose to)
%define compat_provides_noarch %(for ver in %{compat_versions};do echo -n "lsb-noarch = $ver ";done)
%define core_compat_provides_noarch %(for ver in %{compat_versions};do echo -n "lsb-core-noarch = $ver ";done)
%define compat_provides_arch %(for ver in %{compat_versions};do echo -n "lsb-%{lsb_arch} = $ver ";done)
%define core_compat_provides_arch %(for ver in %{compat_versions};do echo -n "lsb-core-%{lsb_arch} = $ver ";done)
%define modular_provides_noarch %(for ver in %{modular_versions};do echo -n "lsbcxx-noarch = $ver lsb-graphics-noarch = $ver ";done)
%define modular_provides_arch %(for ver in %{modular_versions};do echo -n "lsbcxx-%{lsb_arch} = $ver lsb-graphics-%{lsb_arch} = $ver ";done)

Summary:	The skeleton package defining packages needed for LSB compliance
Name:		lsb
Version:	4.1
Release:	13
License:	GPL
Group:		System/Base
URL:		http://www.linuxbase.org
Source0:	tmpdirlsb.sh
Source1:	install_initd
Source2:	remove_initd

Exclusivearch:	%{ix86} x86_64 %arm

%define lsb_arch ia32
%ifarch x86_64
%define lsb_arch amd64
%endif
%ifarch armv7l
%define lsb_arch armv7l
%endif
%ifarch armv7hl
%define lsb_arch armv7hl
%endif

%description
The skeleton package defining packages needed for LSB compliance.
Note: To successfuly run the runtime test suites, install lsb-test.

%package	%{_lib}
Summary:	The skeleton package defining packages needed for LSB compliance
Group:		System/Base

Requires:	lsb-noarch
Requires:	lsb-core-%{_lib}
# former lsb-cxx - both arches called libfoo
Requires:	libstdc++.so.6%{_arch_tag_suffix}
# former lsb-graphics
Requires:	libX11.so.6%{_arch_tag_suffix}
Requires:	libXext.so.6%{_arch_tag_suffix}
Requires:	libXi.so.6%{_arch_tag_suffix}
Requires:	libXt.so.6%{_arch_tag_suffix}
Requires:	libXtst.so.6%{_arch_tag_suffix}
Requires:	libXft.so.2%{_arch_tag_suffix}
Requires:	libXrender.so.1%{_arch_tag_suffix}
Requires:	libfreetype.so.6%{_arch_tag_suffix}
Requires:	libGL.so.1%{_arch_tag_suffix}
Requires:	libGLU.so.1%{_arch_tag_suffix}

# former lsb-desktop
Requires:	libxml2.so.2%{_arch_tag_suffix}
Requires:	libgtk-x11-2.0.so.0%{_arch_tag_suffix}
Requires:	libpng12.so.0%{_arch_tag_suffix}
Requires:	libcairo.so.2%{_arch_tag_suffix}
Requires:	libpango-1.0.so.0%{_arch_tag_suffix}
Requires:	libpangoxft-1.0.so.0%{_arch_tag_suffix}
Requires:	libpangocairo-1.0.so.0%{_arch_tag_suffix}
Requires:	libfontconfig.so.1%{_arch_tag_suffix}
Requires:	libqt-mt.so.3%{_arch_tag_suffix}
Requires:	libjpeg.so.62%{_arch_tag_suffix}

# former lsb-qt4
Requires:	qt4-common >= 4.2.3
# %%mklibname doesn't work here
Requires:	libQtOpenGL.so.4%{_arch_tag_suffix}
Requires:	libQtSvg.so.4%{_arch_tag_suffix}
Requires:	libQtNetwork.so.4%{_arch_tag_suffix}
Requires:	libQtSql.so.4%{_arch_tag_suffix}
Requires:	libQtXml.so.4%{_arch_tag_suffix}

# printing
Requires:	libcups.so.2%{_arch_tag_suffix}

# multimedia
Requires:	libasound.so.2%{_arch_tag_suffix}

# security
Requires:	libnss3.so%{_arch_tag_suffix}
Requires:	libnspr4.so%{_arch_tag_suffix}

Provides:	lsb-%{lsb_arch} = %{version} 
Provides:	%{compat_provides_arch}
Provides:	%{modular_provides_arch}

Conflicts:	lsb-release < 2.0

%rename		lsb-cxx
%rename		lsb-graphics
%rename		lsb-desktop
%rename		lsb-desktop-qt4
%rename		lsb

%description	%{_lib}
The skeleton package defining packages needed for LSB compliance.
Note: To successfuly run the runtime test suites, install lsb-test.

%package	noarch
Summary:	Architecture neutral components of LSB
Group:		System/Base

# former lsb-desktop
Requires:	xdg-utils

# interpreted languages
Requires:	perl perl(CGI) perl(Safe) perl(Pod::Perldoc) 
Requires:	perl(Class::ISA) perl(Pod::Plainer)
Requires:	python

# printing
Requires:	ghostscript foomatic-filters cups-common

Provides:	%{compat_provides_noarch}
Provides:	%{modular_provides_noarch}

%description	noarch
The architecture-neutral requirements for LSB compliance.

%package	core-%{_lib}
Summary:	Core requirements needed for LSB compliance
Group:		System/Base

Requires:	lsb-core-noarch
Requires:	%{_lib}glibc_lsb
Requires:	libpam.so.0%{_arch_tag_suffix}
Requires:	libncurses.so.5%{_arch_tag_suffix}

Provides:	lsb-core-%{lsb_arch} = %{version} 
Provides:	%{core_compat_provides_arch}
%rename		lsb-core

%description	core-%{_lib}
The core requirements for LSB compliance.

%package	core-noarch
Summary:	Architecture neutral components of lsb-core
Group:		System/Base

Requires:	pax lsb-release make sendmail-command ed 
Requires:	binutils bc nail at m4 patch
Requires:	diffutils file gettext chkconfig

Provides:	%{core_compat_provides_noarch}

%description	core-noarch
The architecture-neutral core requirements for LSB compliance.

%package	test
Summary:	Requirements needed to successfully run the LSB runtime tests
Group:		System/Base

Requires:	lsb
Requires:	perl-DBI perl-devel perl-XML-Parser perl-URI glibc-i18ndata
Requires:	locales-de locales-en locales-es locales-fr locales-is
Requires:	locales-it locales-ja locales-se locales-ta locales-zh 
Requires:	wget qt4-database-plugin-sqlite qt3-Sqlite libx11-common
Requires(pre):	rpm-helper
Requires(postun):rpm-helper

%description	test
This packages pulls in additional packages not specified by LSB, but
required to successfully run the LSB runtime tests.

%prep
#%setup -q

%install
cat << EOF > README.urpmi
To run the LSB binary test suite, download the latest version from
ftp://ftp.linuxfoundation.org/pub/lsb/test_suites/released/binary/runtime/
and install lsb-dist-checker or lsb-task-dist-testkit.
 
There is a GUI test manager now, lsb-dist-checker that can guide you 
through the test/certification process.

There are also yum repos at:
 http://ftp.linuxfoundation.org/pub/lsb/repositories/yum/
EOF

install -d %{buildroot}/%{_datadir}/%{name}
install -d %{buildroot}/%{_datadir}/nls
install -d %{buildroot}/%{_datadir}/tmac
install -d %{buildroot}/var/cache/fonts
install -d %{buildroot}/var/games
install -d %{buildroot}/sbin
install -d %{buildroot}%{_sysconfdir}/lsb-release.d
install -d %{buildroot}%{_bindir}
install -d %{buildroot}/lib/%{name}
install -d %{buildroot}%{_prefix}/lib/%{name}
install -d %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %SOURCE0 %{buildroot}%{_sysconfdir}/profile.d
install -m 755 %SOURCE1 %{buildroot}%{_prefix}/lib/%{name}
install -m 755 %SOURCE2 %{buildroot}%{_prefix}/lib/%{name}

touch %{buildroot}%{_sysconfdir}/lsb-release.d/lsb-%{version}-%{lsb_arch}
touch %{buildroot}%{_sysconfdir}/lsb-release.d/lsb-%{version}-noarch
touch %{buildroot}%{_sysconfdir}/lsb-release.d/core-%{version}-%{lsb_arch}
touch %{buildroot}%{_sysconfdir}/lsb-release.d/core-%{version}-noarch
rm -f lsb-noarch-files.txt lsb-files.txt
for lsbver in %{compat_versions}; do
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/lsb-$lsbver-noarch
  echo %{_sysconfdir}/lsb-release.d/lsb-$lsbver-noarch >> lsb-noarch-files.txt
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/lsb-$lsbver-%{lsb_arch}
  echo %{_sysconfdir}/lsb-release.d/lsb-$lsbver-%{lsb_arch} >> lsb-files.txt
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/core-$lsbver-noarch
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/core-$lsbver-%{lsb_arch}
done
for lsbver in %{modular_versions}; do
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/cxx-$lsbver-noarch
  echo %{_sysconfdir}/lsb-release.d/cxx-$lsbver-noarch >> lsb-noarch-files.txt
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/cxx-$lsbver-%{lsb_arch}
  echo %{_sysconfdir}/lsb-release.d/cxx-$lsbver-%{lsb_arch} >> lsb-files.txt
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/graphics-$lsbver-noarch
  echo %{_sysconfdir}/lsb-release.d/graphics-$lsbver-noarch >> lsb-noarch-files.txt
  touch %{buildroot}%{_sysconfdir}/lsb-release.d/graphics-$lsbver-%{lsb_arch}
  echo %{_sysconfdir}/lsb-release.d/graphics-$lsbver-%{lsb_arch} >> lsb-files.txt
done

cat << EOF > %{buildroot}%{_sysconfdir}/profile.d/root-ulimit.sh
# enable a nonzero core file value for root (exec_A test issues)
[ "\$UID" = "0" ] && ulimit -c 1000 > /dev/null 2>&1
EOF

cat << EOF > %{buildroot}%{_bindir}/lsbinstall
#!/bin/sh
exit 0
EOF

cat << EOF > %{buildroot}/sbin/fasthalt
#!/bin/sh
#start fasthalt
/sbin/halt -f
#end fasthalt
EOF

cat << EOF > %{buildroot}/sbin/fastboot
#!/bin/sh
#start fastboot
/sbin/reboot -f
#end fastboot
EOF

cat << EOF > %{buildroot}/etc/hosts.equiv
# Sample hosts.equiv file for LSB compliance
# see man hosts.equiv for usage.
EOF

cat << EOF > %{buildroot}/etc/hosts.lpd
#
# hosts.lpd     This file describes the names of the hosts which are
#               allowed to use the remote printer services of this
#               host.  This file is used by the LPD subsystem.
#		Added for LSB compiance.
EOF

cat << EOF > %{buildroot}/etc/gateways
# sample gateways file for LSB compliance. Database of gateways
# used by routed. Sample format shown below.
# [ net | host ] name1 gateway name2 metric value [ passive | active | external ]
EOF

chmod 0644 %{buildroot}%{_sysconfdir}/profile.d/root-ulimit.sh
chmod 0755 %{buildroot}%{_bindir}/lsbinstall
chmod 0755 %{buildroot}/sbin/fastboot
chmod 0755 %{buildroot}/sbin/fasthalt
chmod 0644 %{buildroot}/etc/hosts.equiv
chmod 0644 %{buildroot}/etc/hosts.lpd
chmod 0644 %{buildroot}/etc/gateways

# (sb) concession for lsb-apache to run
%pre test
%_pre_groupadd nobody

%postun test
%_postun_groupdel nobody

%files %{_lib} -f lsb-files.txt
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{version}-%{lsb_arch}

%files noarch -f lsb-noarch-files.txt
%config(noreplace) %{_sysconfdir}/lsb-release.d/lsb-%{version}-noarch

%files core-%{_lib}
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-*-%{lsb_arch}

%files core-noarch
%{_datadir}/nls
%{_datadir}/tmac
/var/cache/fonts
/var/games
/sbin/fasthalt
/sbin/fastboot
%{_bindir}/lsbinstall
%dir /lib/%{name}
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/install_initd
%{_prefix}/lib/%{name}/remove_initd
%config(noreplace) %{_sysconfdir}/hosts.equiv
%config(noreplace) %{_sysconfdir}/hosts.lpd
%config(noreplace) %{_sysconfdir}/gateways
%config(noreplace) %{_sysconfdir}/lsb-release.d/core-*-noarch

%files test
%{_sysconfdir}/profile.d/tmpdirlsb.sh
%{_sysconfdir}/profile.d/root-ulimit.sh
