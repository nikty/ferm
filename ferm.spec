Summary: ferm - For Easy Rule Making
Name: ferm
Version: 2.6
Release: 1
Group: system/firewalls
License: GPL
Source: http://ferm.foo-projects.org/download/%{version}/%{name}-%{version}.tar.xz
URL: http://ferm.foo-projects.org/
BuildArchitectures: noarch

Requires: perl


%description
Ferm is a tool to maintain complex firewalls, without having the
trouble to rewrite the complex rules over and over again. Ferm
allows the entire firewall rule set to be stored in a separate
file, and to be loaded with one command. The firewall configuration
resembles structured programming-like language, which can contain
levels and lists.

%prep
%setup -q

%build
make
cat > ferm.service <<"END"
[Unit]
Description=for Easy Rule Making

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=%{_prefix}/sbin/ferm %{_sysconfdir}/%{name}/%{name}.conf
ExecStop=%{_prefix}/sbin/ferm --flush %{_sysconfdir}/%{name}/%{name}.conf

[Install]
WantedBy=multi-user.target
END


%install
make install PREFIX=%{buildroot}%{_prefix} DOCDIR=%{buildroot}%{_pkgdocdir} MANDIR=%{buildroot}%{_mandir}/man1

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%files
# %doc AUTHORS README TODO NEWS examples/
%{_pkgdocdir}
%exclude %{_pkgdocdir}/COPYING
%license COPYING
%{_mandir}/man1/*
%{_unitdir}/%{name}.service
%{_sbindir}/import-ferm
%{_sbindir}/ferm

%changelog
* Thu Apr 7 2022
- Bumped version to 2.6

