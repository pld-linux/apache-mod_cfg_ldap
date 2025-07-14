%define		mod_name	cfg_ldap
%define 	apxs		/usr/sbin/apxs
Summary:	Module to keep Apache VirtualHost configuration in an LDAP directory
Summary(pl.UTF-8):	Moduł do przechowywania konfiguracji serwerów wirtualnych Apache'a w katalogu LDAP
Name:		apache-mod_%{mod_name}
Version:	1.2
Release:	4
License:	BSD
Group:		Networking/Daemons/HTTP
Source0:	http://dl.sourceforge.net/modcfgldap/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	055924d6488608f684b22e7b04cea2ea
Patch0:		%{name}-openldap-2.3.patch
URL:		http://sourceforge.net/projects/modcfgldap/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	db-devel >= 4.2.52
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	rpmbuild(macros) >= 1.304
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		schemadir	/usr/share/openldap/schema

%description
mod_cfg_ldap allows you to keep your virtual host configuration in a
LDAP directory and update it in nearly realtime.

%description -l pl.UTF-8
mod_cfg_ldap pozwala na przechowywanie konfiguracji hostów wirtualnych
w katalogu LDAP i uaktualnianie jej prawie w czasie rzeczywistym.

%package -n openldap-schema-mod_cfg_ldap
Summary:	mod_cfg_ldap LDAP schema
Summary(pl.UTF-8):	Schemat LDAP dla mod_cfg_ldap
Group:		Networking/Daemons/HTTP
Requires:	openldap-servers

%description -n openldap-schema-mod_cfg_ldap
This package contains LDAP schema for use with mod_cfg_ldap.

%description -n openldap-schema-mod_cfg_ldap -l pl.UTF-8
Ten pakiet zawiera schemat LDAP do używania z mod_cfg_ldap.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch -P0 -p1

%build
%{__make} all \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir},%{schemadir}}

install -p .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p cfg_ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/85_mod_cfg_ldap.conf
cp -p mod_cfg_ldap.schema $RPM_BUILD_ROOT%{schemadir}/mod_cfg_ldap.schema

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%post -n openldap-schema-mod_cfg_ldap
%openldap_schema_register %{schemadir}/mod_cfg_ldap.schema
%service -q ldap restart

%postun -n openldap-schema-mod_cfg_ldap
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/mod_cfg_ldap.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README TODO
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so

%files -n openldap-schema-mod_cfg_ldap
%defattr(644,root,root,755)
%{schemadir}/*.schema
