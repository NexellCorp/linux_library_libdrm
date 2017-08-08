%ifarch %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

Name:           libdrm
Summary:        Direct Rendering Manager runtime library
Version:        2.4.76
Release:        20%{?dist}
License:        MIT

URL:            https://dri.freedesktop.org
Source0:        %{url}/libdrm/%{name}-%{version}.tar.bz2

BuildRequires:  pkgconfig automake autoconf libtool
BuildRequires:  kernel-headers
BuildRequires:  libxcb-devel
BuildRequires:  systemd-devel
Requires:       systemd
BuildRequires:  libatomic_ops-devel
BuildRequires:  libpciaccess-devel
BuildRequires:  libxslt docbook-style-xsl
%if %{with valgrind}
BuildRequires:  valgrind-devel
%endif
BuildRequires:  xorg-x11-util-macros

%description
Direct Rendering Manager runtime library

%package devel
Summary:        Direct Rendering Manager development package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kernel-headers

%description devel
Direct Rendering Manager development package.

%package -n drm-utils
Summary:        Direct Rendering Manager utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure \
%if ! %{with valgrind}
    --disable-valgrind \
%endif
    --disable-vc4 \
%ifarch %{arm} aarch64
    --enable-etnaviv-experimental-api \
    --enable-exynos-experimental-api \
    --enable-tegra-experimental-api \
    --enable-vc4 \
    --enable-nexell \
%endif
%ifarch %{arm}
    --enable-omap-experimental-api \
%endif
    --enable-install-test-programs \
    --enable-udev

%make_build V=1
pushd tests
%make_build `make check-programs` V=1
popd

%install
%make_install
pushd tests
mkdir -p %{buildroot}%{_bindir}
for foo in $(make check-programs) ; do
 libtool --mode=install install -m 0755 $foo %{buildroot}%{_bindir}
done
popd
# SUBDIRS=libdrm

# NOTE: We intentionally don't ship *.la files
find %{buildroot} -type f -name "*.la" -delete

rm -f %{buildroot}%{_includedir}/%{name}/{r300_reg.h,via_3d_reg.h}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.MIT
%doc README
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%endif
%ifarch %{arm}
%{_libdir}/libdrm_omap.so.1
%{_libdir}/libdrm_omap.so.1.0.0
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_etnaviv.so.1
%{_libdir}/libdrm_etnaviv.so.1.0.0
%{_libdir}/libdrm_exynos.so.1
%{_libdir}/libdrm_exynos.so.1.0.0
%{_libdir}/libdrm_freedreno.so.1
%{_libdir}/libdrm_freedreno.so.1.0.0
%{_libdir}/libdrm_tegra.so.0
%{_libdir}/libdrm_tegra.so.0.0.0
%{_libdir}/libdrm_nexell.so
%{_libdir}/libdrm_nexell.so.1
%{_libdir}/libdrm_nexell.so.1.0.0
%endif
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%{_libdir}/libdrm_amdgpu.so.1
%{_libdir}/libdrm_amdgpu.so.1.0.0
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%{_libdir}/libkms.so.1
%{_libdir}/libkms.so.1.0.0

%files -n drm-utils
%license LICENSE.MIT
%{_bindir}/drmdevice
%{_bindir}/modetest
%{_bindir}/modeprint
%{_bindir}/vbltest
%{_bindir}/kmstest
%{_bindir}/kms-steal-crtc
%{_bindir}/kms-universal-planes
%exclude %{_bindir}/drmsl
%ifarch %{arm} aarch64
%exclude %{_bindir}/etnaviv*
%exclude %{_bindir}/exynos*
%endif
%exclude %{_bindir}/hash
%exclude %{_bindir}/proptest
%exclude %{_bindir}/random

%files devel
%license LICENSE.MIT
# FIXME should be in drm/ too
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%ifarch %{ix86} x86_64 ia64
%{_includedir}/libdrm/intel_aub.h
%{_includedir}/libdrm/intel_bufmgr.h
%{_includedir}/libdrm/intel_debug.h
%endif
%ifarch %{arm}
%{_includedir}/libdrm/omap_drmif.h
%{_includedir}/omap/
%endif
%ifarch %{arm} aarch64
%{_includedir}/exynos/
%{_includedir}/freedreno/
%{_includedir}/libdrm/etnaviv_drmif.h
%{_includedir}/nexell/
%{_includedir}/libdrm/exynos_drmif.h
%{_includedir}/libdrm/tegra.h
%{_includedir}/libdrm/vc4_packet.h
%{_includedir}/libdrm/vc4_qpu_defines.h
%endif
%{_includedir}/libdrm/amdgpu.h
%{_includedir}/libdrm/radeon_bo.h
%{_includedir}/libdrm/radeon_bo_gem.h
%{_includedir}/libdrm/radeon_bo_int.h
%{_includedir}/libdrm/radeon_cs.h
%{_includedir}/libdrm/radeon_cs_gem.h
%{_includedir}/libdrm/radeon_cs_int.h
%{_includedir}/libdrm/radeon_surface.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_includedir}/libdrm/nouveau/
%{_includedir}/libdrm/*_drm.h
%{_includedir}/libkms
%{_includedir}/libsync.h
%{_libdir}/libdrm.so
%ifarch %{ix86} x86_64 ia64
%{_libdir}/libdrm_intel.so
%endif
%ifarch %{arm}
%{_libdir}/libdrm_omap.so
%endif
%ifarch %{arm} aarch64
%{_libdir}/libdrm_etnaviv.so
%{_libdir}/libdrm_exynos.so
%{_libdir}/libdrm_freedreno.so
%{_libdir}/libdrm_tegra.so
%endif
%{_libdir}/libdrm_radeon.so
%{_libdir}/libdrm_amdgpu.so
%{_libdir}/libdrm_nouveau.so
%{_libdir}/libkms.so
%{_libdir}/pkgconfig/libdrm.pc
%ifarch %{ix86} x86_64 ia64
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%ifarch %{arm}
%{_libdir}/pkgconfig/libdrm_omap.pc
%endif
%ifarch %{arm} aarch64
%{_libdir}/pkgconfig/libdrm_etnaviv.pc
%{_libdir}/pkgconfig/libdrm_exynos.pc
%{_libdir}/pkgconfig/libdrm_freedreno.pc
%{_libdir}/pkgconfig/libdrm_tegra.pc
%{_libdir}/pkgconfig/libdrm_vc4.pc
%{_libdir}/pkgconfig/libdrm_nexell.pc
%endif
%{_libdir}/pkgconfig/libdrm_radeon.pc
%{_libdir}/pkgconfig/libdrm_amdgpu.pc
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%{_libdir}/pkgconfig/libkms.pc
%{_mandir}/man3/drm*.3*
%{_mandir}/man7/drm*.7*

%changelog
* Thu Mar 30 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.76-1
- Update to 2.4.76

* Thu Mar 23 2017 Adam Jackson <ajax@redhat.com> - 2.4.75-3
- Fix pkg-config detection on non-Intel

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Dave Airlie <airlied@redhat.com> - 2.4.75-1
- Update to 2.4.75

* Sat Jan 21 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.74-2
- Enable etnaviv support on aarch64 too

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.74-1
- Update to 2.4.74 (RHBZ #1400154)

* Tue Nov 15 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.73-1
- Update to 2.4.73 (RHBZ #1394986)

* Wed Oct 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.71-2
- Enable etnaviv on ARM (RHBZ #1381898, billiboy@mt2015.com)

* Tue Oct 04 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.71-1
- Update to 2.4.71 (RHBZ #1381543)

* Thu Aug 11 2016 Michal Toman <mtoman@fedoraproject.org> - 2.4.70-2
- No valgrind on MIPS

* Sun Jul 24 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.70-1
- Update to 2.4.70 (RHBZ #1359449)

* Thu Jul 21 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.69-1
- Update to 2.4.69 (RHBZ #1358549)

* Thu Apr 28 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.68-1
- Update to 2.4.68

* Sat Apr  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-3
- Build some extra bits for aarch64

* Sun Feb 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-2
- Fix build on aarch64

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 2.4.67-2
- fix installing drm-utils properly - we were install libtool scripts

* Tue Feb 16 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-1
- Update to 2.4.67
- Enable VC4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.66-1
- Update to 2.4.66 (RHBZ #1294382)

* Thu Sep 17 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.65-1
- Update to 2.4.65 (RHBZ #1263878)

* Tue Aug 25 2015 Dave Airlie <airlied@redhat.com> 2.4.64-1
- libdrm 2.4.64

* Mon Jul 13 2015 Dan Horák <dan[at]danny.cz> 2.4.62-2
- valgrind needs explicit disable if not available

* Sun Jul 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.62-1
- libdrm 2.4.62
- Minor spec cleanups

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-3
- build needs xorg-x11-util-macros now...

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-2
- fixup patch, don't ship extra tests

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-1
- libdrm 2.4.61

* Mon Mar 23 2015 Dave Airlie <airlied@redhat.com> 2.4.60-1
- libdrm 2.4.60

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-4
- No we don't actually want to install the exynos tests

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-3
- Add test apps to drm-utils package

* Thu Jan 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.59-2
- Enable tegra

* Thu Jan 22 2015 Dave Airlie <airlied@redhat.com> 2.4.59-1
- libdrm 2.4.59

* Wed Nov 19 2014 Dan Horák <dan[at]danny.cz> 2.4.58-3
- valgrind available only on selected arches

* Tue Nov 18 2014 Adam Jackson <ajax@redhat.com> 2.4.58-2
- BR: valgrind-devel so we get ioctl annotations

* Thu Oct 02 2014 Adam Jackson <ajax@redhat.com> 2.4.58-1
- libdrm 2.4.58

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Dave Airlie <airlied@redhat.com> 2.4.56-1
- libdrm 2.4.56

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.54-3
- Build freedreno support on aarch64 too

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Dennis Gilmore <dennis@ausil.us> 2.4.54-1
- libdrm 2.4.54

* Sun Apr 13 2014 Dave Airlie <airlied@redhat.com> 2.4.53-1
- libdrm 2.4.53

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> 2.4.52-1
- libdrm 2.4.52

* Thu Dec 05 2013 Dave Airlie <airlied@redhat.com> 2.4.50-1
- libdrm 2.4.50

* Mon Dec 02 2013 Dave Airlie <airlied@redhat.com> 2.4.49-2
- backport two fixes from master

* Sun Nov 24 2013 Dave Airlie <airlied@redhat.com> 2.4.49-1
- libdrm 2.4.49

* Fri Nov 08 2013 Dave Airlie <airlied@redhat.com> 2.4.47-1
- libdrm 2.4.47

- add fix for nouveau with gcc 4.8
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Dave Airlie <airlied@redhat.com> 2.4.46-1
- libdrm 2.4.46

* Tue Jun 18 2013 Adam Jackson <ajax@redhat.com> 2.4.45-2
- Sync some Haswell updates from git

* Thu May 16 2013 Dave Airlie <airlied@redhat.com> 2.4.45-1
- libdrm 2.4.45

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.44-2
- enable freedreno support on ARM

* Fri Apr 19 2013 Jerome Glisse <jglisse@redhat.com> 2.4.44-1
- libdrm 2.4.44

* Fri Apr 12 2013 Adam Jackson <ajax@redhat.com> 2.4.43-1
- libdrm 2.4.43

* Tue Mar 12 2013 Dave Airlie <airlied@redhat.com> 2.4.42-2
- add qxl header file

* Tue Feb 05 2013 Adam Jackson <ajax@redhat.com> 2.4.42-1
- libdrm 2.4.42

* Tue Jan 22 2013 Adam Jackson <ajax@redhat.com> 2.4.41-2
- Fix directory ownership in -devel (#894468)

* Thu Jan 17 2013 Adam Jackson <ajax@redhat.com> 2.4.41-1
- libdrm 2.4.41 plus git.  Done as a git snapshot instead of the released
  2.4.41 since the release tarball is missing man/ entirely. 
- Pre-F16 changelog trim

* Wed Jan 09 2013 Ben Skeggs <bskeggs@redhat.com> 2.4.40-2
- nouveau: fix bug causing kernel to reject certain command streams

* Tue Nov 06 2012 Dave Airlie <airlied@redhat.com> 2.4.40-1
- libdrm 2.4.40

* Thu Oct 25 2012 Adam Jackson <ajax@redhat.com> 2.4.39-4
- Rebuild to appease koji and get libkms on F18 again

* Mon Oct 08 2012 Adam Jackson <ajax@redhat.com> 2.4.39-3
- Add exynos to arm

* Mon Aug 27 2012 Dave Airlie <airlied@redhat.com> 2.4.39-1
- upstream 2.4.39 release

* Tue Aug 14 2012 Dave Airlie <airlied@redhat.com> 2.4.38-2
- add radeon prime support

* Sun Aug 12 2012 Dave Airlie <airlied@redhat.com> 2.4.38-1
- upstream 2.4.38 release

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Dave Airlie <airlied@redhat.com> 2.4.37-3
- add libdrm prime support for core, intel, nouveau

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 2.4.37-2
- libdrm-2.4.37-i915-hush.patch: Silence an excessive error message

* Fri Jul 13 2012 Dave Airlie <airlied@redhat.com> 2.4.37-1
- bump to libdrm 2.4.37

* Thu Jun 28 2012 Dave Airlie <airlied@redhat.com> 2.4.36-1
- bump to libdrm 2.4.36

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> 2.4.35-2
- Drop libkms. Only used by plymouth, and even that's a mistake.

* Fri Jun 15 2012 Dave Airlie <airlied@redhat.com> 2.4.35-1
- bump to libdrm 2.4.35

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 2.4.34-2
- Rebuild for new libudev
- Conditional BuildReqs for {libudev,systemd}-devel

* Sat May 12 2012 Dave Airlie <airlied@redhat.com> 2.4.34-1
- libdrm 2.4.34

* Fri May 11 2012 Dennis Gilmore <dennis@ausil.us> 2.4.34-0.3
- enable libdrm_omap on arm arches

* Thu May 10 2012 Adam Jackson <ajax@redhat.com> 2.4.34-0.2
- Drop ancient kernel Requires.

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 2.4.34-0.1.20120424
- Update to a newer git snapshot

* Sat Mar 31 2012 Dave Airlie <airlied@redhat.com> 2.4.33-1
- libdrm 2.4.33
- drop libdrm-2.4.32-tn-surface.patch

* Wed Mar 21 2012 Adam Jackson <ajax@redhat.com> 2.4.32-1
- libdrm 2.4.32
- libdrm-2.4.32-tn-surface.patch: Sync with git.

* Sat Feb 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.31-4
- Add gem_ binaries to x86 only exclusion too

* Wed Feb 22 2012 Adam Jackson <ajax@redhat.com> 2.4.31-3
- Fix build on non-Intel arches

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-2
- Fix missing header file

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-1
- upstream 2.4.31 release

* Fri Jan 20 2012 Dave Airlie <airlied@redhat.com> 2.4.30-1
- upstream 2.4.30 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Adam Jackson <ajax@redhat.com> 2.4.27-2
- Fix typo in udev rule

* Tue Nov 01 2011 Adam Jackson <ajax@redhat.com> 2.4.27-1
- libdrm 2.4.27

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.26-4
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Adam Jackson <ajax@redhat.com> 2.4.26-3
- Fix udev rule matching and install location (#748205)

* Fri Oct 21 2011 Dave Airlie <airlied@redhat.com> 2.4.26-2
- fix perms on control node in udev rule

* Mon Jun 06 2011 Adam Jackson <ajax@redhat.com> 2.4.26-1
- libdrm 2.4.26 (#711038)
