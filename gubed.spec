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
Release:	0.3
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://dl.sourceforge.net/sourceforge/gubed/Gubed%{version}.tar.gz
# Source0-md5:	16c5b36c24f701aaf5d5e8a553b7341e
Source1:	%{name}-gtk.desktop
Source2:	%{name}-x11.desktop
Source3:	%{name}.png
URL:		http://gubed.mccabe.nu/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	wxGTK2-devel
BuildRequires:	wxX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q -n Gubed

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
