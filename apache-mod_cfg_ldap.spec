%define 	apxs		/usr/sbin/apxs
Summary:	Module to keep Apache VirtualHost configuration in an LDAP directory
Summary(pl):	Modu³ do przechowywania konfiguracji serwerów wirtualnych Apache'a w katalogu LDAP
%define tarname mod_cfg_ldap
Name:		apache-%{tarname}
Version:	1.1
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modcfgldap/%{tarname}-%{version}.tar.gz
# Source0-md5:	42f4018277a2d3673d765d1bfd884c89
URL:		http://modcfgldap.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	db-devel >= 4.2.52
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mod_cfg_ldap allows you to keep your virtual host configuration in a
LDAP directory and update it in nearly realtime.

%description -l pl
mod_cfg_ldap pozwala na przechowywanie konfiguracji hostów wirtualnych
w katalogu LDAP i uaktualnianie jej prawie w czasie rzeczywistym.

%prep
%setup -q -n %{tarname}-%{version}

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules

install -m755 .libs/%{tarname}.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules

# Install the config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf
install cfg_ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf/85_mod_cfg_ldap.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL README TODO
%attr(755,root,root) %{_libdir}/httpd/modules/*.so
%config(noreplace) %{_sysconfdir}/httpd/httpd.conf/*.conf
