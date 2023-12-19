%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-rmf-task-sequence
Version:        2.1.7
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rmf_task_sequence package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       json-devel
Requires:       ros-humble-nlohmann-json-schema-validator-vendor
Requires:       ros-humble-rmf-api-msgs
Requires:       ros-humble-rmf-task
Requires:       ros-humble-ros-workspace
BuildRequires:  cmake3
BuildRequires:  json-devel
BuildRequires:  ros-humble-nlohmann-json-schema-validator-vendor
BuildRequires:  ros-humble-rmf-api-msgs
BuildRequires:  ros-humble-rmf-task
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-humble-ament-cmake-catch2
BuildRequires:  ros-humble-ament-cmake-uncrustify
%endif

%description
Implementation of phase-sequence tasks for the Robotics Middleware Framework

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Tue Dec 19 2023 Grey <grey@openrobotics.org> - 2.1.7-1
- Autogenerated by Bloom

* Thu Aug 10 2023 Grey <grey@openrobotics.org> - 2.1.6-1
- Autogenerated by Bloom

* Fri Jun 30 2023 Grey <grey@openrobotics.org> - 2.1.5-1
- Autogenerated by Bloom

* Mon Jun 05 2023 Grey <grey@openrobotics.org> - 2.1.4-1
- Autogenerated by Bloom

* Tue Oct 11 2022 Grey <grey@openrobotics.org> - 2.1.1-1
- Autogenerated by Bloom

* Thu Oct 06 2022 Grey <grey@openrobotics.org> - 2.1.0-1
- Autogenerated by Bloom
