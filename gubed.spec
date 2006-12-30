#
# Conditional build:
%bcond_without	gtk2	# don't build gbdclient with GTK2 interface
%bcond_without	x11univ	# don't build gbdclient with x11univ interface
%bcond_without	proxy	# don't build proxy
%bcond_without	server	# don't build server
#
Summary:	Gubed - a PHP debuger
Name:		gubed
Version:	0.2.2
Release:	0.5
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://dl.sourceforge.net/sourceforge/gubed/Gubed%{version}.tar.gz
# Source0-md5:	16c5b36c24f701aaf5d5e8a553b7341e
Source1:	%{name}-gtk.desktop
Source2:	%{name}-x11.desktop
Source3:	%{name}.png
Patch0:		%{name}-paths.patch
URL:		http://gubed.mccabe.nu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_gtk2:BuildRequires:	wxGTK2-devel}
%{?with_x11univ:BuildRequires:	wxX11-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires(triggerpostun):	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Gubed PHP debuger.

%package client-gtk2
Summary:	Gubed debugger - client with GTK2 interface
Group:		Development/Languages/PHP

%description client-gtk2
Gubed PHP debugger - client with GTK2 interface.

%package client-x11
Summary:	Gubed PHP debugger - client with x11univ interface
Group:		Development/Languages/PHP

%description client-x11
Gubed PHP debugger - client with x11univ interface.

%package proxy
Summary:	Gubed debugger - proxy server
Group:		Development/Languages/PHP

%description proxy
Gubed PHP debugger - proxy server.

%package server
Summary:	Gubed server part
Group:		Development/Languages/PHP

%description server
Gubed PHP debugger - server part.

%prep
%setup -q -n Gubed
%patch0 -p1

%build
%if %{with gtk2}
cp -af Client{,-gtk2}
cd Client-gtk2
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-wx-config=/usr/bin/wx-gtk2-ansi-config

%{__make}
cd ..
%endif

%if %{with x11univ}
mv -f Client{,-x11}
cd Client-x11
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-wx-config=/usr/bin/wx-x11univ-ansi-config

%{__make}
cd ..
%endif

%if %{with proxy}
cd Proxy
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure 
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{Client-{gtk2,x11},Proxy}
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_pixmapsdir}/%{name}.png

%if %{with gtk2}
cd Client-gtk2
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/gbdclient{,-gtk}
cd ..
install -D %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-gtk.desktop
%endif

%if %{with x11univ}
cd Client-x11
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_bindir}/gbdclient{,-x11}
cd ..
install -D %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}-x11.desktop
%endif

%if %{with proxy}
cd Proxy
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
cd ..
%endif

%if %{with server}
cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}/ServerScripts
<Directory %{_appdir}>
	Order Allow,Deny
	Allow from all
</Directory>
EOF

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

cp -a ServerScripts $RPM_BUILD_ROOT%{_appdir}
mv -f $RPM_BUILD_ROOT%{_appdir}/ServerScripts/localsettings_dist.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.php

%triggerin server -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun server -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin server -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun server -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_datadir}/gbdclient
%{_pixmapsdir}/*.png

%files client-gtk2
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gbdclient-gtk
%{_desktopdir}/%{name}-gtk.desktop

%files client-x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gbdclient-x11
%{_desktopdir}/%{name}-x11.desktop

%files proxy
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gbdproxy

%files server
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
