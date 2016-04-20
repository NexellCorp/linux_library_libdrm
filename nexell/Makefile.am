AM_CFLAGS = \
	$(WARN_CFLAGS) \
	-I$(top_srcdir) \
	$(PTHREADSTUBS_CFLAGS) \
	-I$(top_srcdir)/include/drm

libdrm_nexell_la_LTLIBRARIES = libdrm_nexell.la
libdrm_nexell_ladir = $(libdir)
libdrm_nexell_la_LDFLAGS = -version-number 1:0:0 -no-undefined
libdrm_nexell_la_LIBADD = ../libdrm.la @PTHREADSTUBS_LIBS@

libdrm_nexell_la_SOURCES = \
	nexell_drm.c 

libdrm_nexellincludedir = ${includedir}/nexell
libdrm_nexellinclude_HEADERS = nexell_drmif.h nexell_drm.h

pkgconfigdir = @pkgconfigdir@
pkgconfig_DATA = libdrm_nexell.pc

TESTS = nexell-symbol-check
EXTRA_DIST = $(TESTS)
