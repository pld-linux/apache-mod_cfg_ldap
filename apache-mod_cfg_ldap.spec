%define		mod_name	cfg_ldap
%define 	apxs		/usr/sbin/apxs
Summary:	Module to keep Apache VirtualHost configuration in an LDAP directory
Summary(pl):	Modu³ do przechowywania konfiguracji serwerów wirtualnych Apache'a w katalogu LDAP
Name:		apache-mod_%{mod_name}
Version:	1.2
Release:	4
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modcfgldap/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	055924d6488608f684b22e7b04cea2ea
Patch0:		%{name}-openldap-2.3.patch
URL:		http://modcfgldap.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	db-devel >= 4.2.52
BuildRequires:	openldap-devel >= 2.3.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
mod_cfg_ldap allows you to keep your virtual host configuration in a
LDAP directory and update it in nearly realtime.

%description -l pl
mod_cfg_ldap pozwala na przechowywanie konfiguracji hostów wirtualnych
w katalogu LDAP i uaktualnianie jej prawie w czasie rzeczywistym.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make} all \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install cfg_ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/85_mod_cfg_ldap.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README TODO *.schema
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
