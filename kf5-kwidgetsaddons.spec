#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.93
%define		qtver		5.15.2
%define		kfname		kwidgetsaddons

Summary:	Large set of desktop widgets
Name:		kf5-%{kfname}
Version:	5.93.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	87f96658d4cd23966064cd8555ac377e
Patch0:		failed-tests.patch
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5UiTools-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Widgets >= %{qtver}
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
This repository contains add-on widgets and classes for applications
that use the Qt Widgets module. If you are porting applications from
KDE Platform 4 "kdeui" library, you will find many of its classes
here.

Provided are action classes that can be added to toolbars or menus, a
wide range of widgets for selecting characters, fonts, colors,
actions, dates and times, or MIME types, as well as platform-aware
dialogs for configuration pages, message boxes, and password requests.

Further widgets and classes can be found in other KDE frameworks. For
a full list, please see
<https://projects.kde.org/projects/frameworks/>


%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}
#%%patch0 -p1

%build
install -d build
cd build
%cmake -G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	../
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5WidgetsAddons.so.5
%attr(755,root,root) %{_libdir}/libKF5WidgetsAddons.so.*.*
%attr(755,root,root) %{_libdir}/qt5/plugins/designer/kwidgetsaddons5widgets.so
%dir %{_datadir}/kf5/kcharselect
%{_datadir}/kf5/kcharselect/kcharselect-data
%{_datadir}/qlogging-categories5/kwidgetsaddons.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KWidgetsAddons
%{_libdir}/cmake/KF5WidgetsAddons
%{_libdir}/libKF5WidgetsAddons.so
%{qt5dir}/mkspecs/modules/qt_KWidgetsAddons.pri
