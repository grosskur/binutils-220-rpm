# rpmbuild parameters:
# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with debug: Build without optimizations and without splitting the debuginfo.
# --without testsuite: Do not run the testsuite.  Default is to run it.
# --with testsuite: Run the testsuite.  Default --with debug is not to run it.

%define binutils_target %{_target_platform}

Summary: Binary utilities for the preview of GCC version 4.4
Name: binutils220%{?_with_debug:-debug}
Version: 2.20.51.0.2
Release: 5.29%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils
Source: http://s3.amazonaws.com/cb-mirror/binutils-%{version}.tar.bz2
Source2: binutils-2.19.50.0.1-output-format.sed
Patch01: binutils-2.20.51.0.2-libtool-lib64.patch
Patch02: binutils-2.20.51.0.2-ppc64-pie.patch
Patch03: binutils-2.20.51.0.2-ia64-lib64.patch
Patch04: binutils-2.20.51.0.2-envvar-revert.patch
Patch05: binutils-2.20.51.0.2-version.patch
Patch06: binutils-2.20.51.0.2-set-long-long.patch
Patch07: binutils-2.20.51.0.2-build-id.patch
Patch08: binutils-2.20.51.0.2-add-needed.patch
Patch09: binutils-2.20.51.0.2-ifunc-ld-s.patch
Patch10: binutils-2.20.51.0.2-lwp.patch
Patch11: binutils-2.20.51.0.2-gas-expr.patch
Patch12: binutils-2.20.51.0.2-pie-perm.patch
Patch13: binutils-2.20.51.0.2-ppc64-ifunc-nocombreloc.patch
Patch14: binutils-2.20.51.0.2-ppc64-tls-transitions.patch
Patch15: binutils-2.20.51.0.2-readelf-dynamic.patch
Patch16: binutils-2.20.51.0.2-xop.patch
Patch17: binutils-2.20.51.0.2-xop2.patch
Patch18: binutils-2.20.51.0.2-xop3.patch
Patch19: binutils-2.20.51.0.2-rh545384.patch
Patch20: testsuite.patch
Patch21: binutils-rh576129.patch
Patch22: binutils-amd-bni.patch
Patch23: binutils-lwp-16bit.patch
Patch24: binutils-2.20.51.0.2-ld-r.patch
Patch25: binutils-rh578576.patch
Patch26: binutils-rh587788.patch
Patch27: binutils-rh588825.patch
Patch28: binutils-rh578661.patch
Patch29: binutils-rh633448.patch
Patch30: binutils-rh464723.patch
Patch31: binutils-rh631540.patch
Patch32: binutils-rh614443.patch
Patch33: binutils-rh663587.patch
Patch34: binutils-rh679435.patch
Patch35: binutils-rh680143.patch
Patch36: binutils-rh697703.patch
Patch37: binutils-rh698005.patch
Patch38: binutils-rh689829.patch
Patch39: binutils-rh664640.patch
Patch40: binutils-rh701586.patch
Patch41: binutils-rh707387.patch
Patch42: binutils-rh696494.patch
Patch43: binutils-rh714824.patch
Patch44: binutils-rh721079.patch
Patch45: binutils-rh696368.patch
Patch46: binutils-rh733122.patch

%define run_testsuite 0%{!?_without_testsuite:1}

Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel
# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{run_testsuite}
BuildRequires: dejagnu, sharutils
%endif

%description
The binutils220 package contains the assembler and objdump utility
for the preview of GCC version 4.4.

%prep
%setup -q -n binutils-%{version}
%patch01 -p0 -b .libtool-lib64~
%patch02 -p0 -b .ppc64-pie~
%ifarch ia64
%if "%{_lib}" == "lib64"
%patch03 -p0 -b .ia64-lib64~
%endif
%endif
%patch04 -p0 -b .envvar-revert~
%patch05 -p0 -b .version~
%patch06 -p0 -b .set-long-long~
%patch07 -p0 -b .build-id~
%patch08 -p0 -b .add-needed~
%patch09 -p0 -b .ifunc-ld-s~
%patch10 -p0 -b .lwp~
%patch11 -p0 -b .gas-expr~
%patch12 -p0 -b .pie-perm~
%patch13 -p0 -b .ppc64-ifunc-nocombreloc~
%patch14 -p0 -b .ppc64-tls-transitions~
%patch15 -p0 -b .readelf-dynamic~
%patch16 -p0 -b .xop~
%patch17 -p0 -b .xop2~
%patch18 -p0 -b .xop3~
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1

# We cannot run autotools as there is an exact requirement of autoconf-2.59.

# On ppc64 we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%%{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}
# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi
touch */configure

%build
echo target is %{binutils_target}
export CFLAGS="$RPM_OPT_FLAGS"
CARGS=

case %{binutils_target} in i?86*|sparc*|ppc*|s390*|sh*)
  CARGS="$CARGS --enable-64-bit-bfd"
  ;;
esac

case %{binutils_target} in ia64*)
  CARGS="$CARGS --enable-targets=i386-linux"
  ;;
esac

%configure \
  --build=%{_target_platform} --host=%{_target_platform} \
  --target=%{binutils_target} \
  --disable-shared \
  $CARGS \
  --disable-werror \
  --with-bugurl=http://bugzilla.redhat.com/bugzilla/
make %{_smp_mflags} tooldir=%{_prefix} all

# Do not use %%check as it is run after %%install where libbfd.so is rebuild
# with -fvisibility=hidden no longer being usable in its shared form.
%if !%{run_testsuite}
echo ====================TESTSUITE DISABLED=========================
%else
status=0
make -k check-{gas,binutils} < /dev/null || status=$?
echo ====================TESTING=========================
cat {gas/testsuite/gas,binutils/binutils}.sum
echo ====================TESTING END=====================
for file in {gas/testsuite/gas,binutils/binutils}.{sum,log}
do
  ln $file binutils-%{_target_platform}-$(basename $file) || :
done
tar cjf binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
uuencode binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}.tar.bz2
rm -f binutils-%{_target_platform}.tar.bz2 binutils-%{_target_platform}-*.{sum,log}
test $status -eq 0
%endif

%install
rm -rf %{buildroot}
make install-{gas,binutils} DESTDIR=%{buildroot}

# No -devel
rm -rf %{buildroot}%{_includedir}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}

mkdir -p %{buildroot}%{_libexecdir}/binutils220
mv %{buildroot}%{_prefix}/bin/{as,objdump} %{buildroot}%{_libexecdir}/binutils220
rm -f %{buildroot}%{_prefix}/bin/*
rm -rf %{buildroot}%{_mandir}/man1

# This one comes from gcc
rm -rf %{buildroot}%{_prefix}/%{binutils_target}

rm -rf %{buildroot}%{_prefix}/share

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/binutils220

%changelog
* Tue Nov 01 2011 Frank Ch. Eigler <fche@redhat.com> - 2.20.51.0.2-5.29.el5
- Added patches 33..46

* Thu Jan 13 2011 Andreas Schwab <schwab@redhat.com> - 2.20.51.0.2-5.28.el5
- New package

