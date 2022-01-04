%define majorver 1.7
%define minorver 4.2

Name:       socat
Summary:    Multipurpose relay for bidirectional data transfer
# define own version because sometimes OBS fiddles with %%{version}
%define upstream_version %{majorver}.%{minorver}
Version:    %{upstream_version}
Release:    1%{?dist}
Group:      Applications/Communications
License:    GPLv2
URL:        http://www.dest-unreach.org/socat
Source0:    %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: gcc
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: autoconf automake
# for make test
BuildRequires: openssl net-tools 

%description
socat is a relay for bidirectional data transfer between two independent data
channels. Each of these data channels may be a file, pipe, device (serial line
etc. or a pseudo terminal), a socket (UNIX, IP4, IP6 - raw, UDP, TCP), an
SSL socket, proxy CONNECT connection, a file descriptor (stdin etc.), the GNU
line editor (readline), a program, or a combination of two of these. 
These modes include generation of "listening" sockets, named pipes, and pseudo
terminals.

socat can be used, e.g., as TCP port forwarder (one-shot or daemon), as an
external socksifier, for attacking weak firewalls, as a shell interface to UNIX
sockets, IP6 relay, for redirecting TCP oriented programs to a serial line, to
logically connect serial lines on different computers, or to establish a
relatively secure environment (su and  chroot) for running client or server
shell scripts with network connections.

Type: console-application
Custom:
  Repo: https://github.com/sailfishos-chum/socat
Categories:
  - Utility

%define source_date_epoch_from_changelog 1
%define clamp_mtime_to_source_date_epoch 1
%define use_source_date_epoch_as_buildtime 1
%define _buildhost SailfishSDK

%prep
%autosetup -n %{name}-%{version}/socat

%build
export CFLAGS="$CFLAGS -Wall -fPIE -shared-libgcc -fstack-protector-strong -fstack-clash-protection -D_FORTIFY_SOURCE=2 -g -Wl,--as-needed -Wl,-z,defs -Wl,-z,relro,-z,now"
# FIXME currently broken: -Wl,-pie

autoconf
%configure \
  --disable-libwrap

# TODO "yodl" is missing for building docs, so only make "progs"
make %{?_smp_mflags} progs

%check
# Run the testsuite - TODO might not work properly in all environments
#make test

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
# missing docs due to missing yodl
#mkdir -p %{buildroot}%{_mandir}/man1
#make install DESTDIR=%{buildroot}
%__install -m 755 socat %{buildroot}%{_bindir}
%__install -m 755 procan %{buildroot}%{_bindir}
%__install -m 755 filan %{buildroot}%{_bindir}

%files
%defattr(-,root,root,-)
%doc README CHANGES EXAMPLES SECURITY FAQ BUGREPORTS
%doc COPYING COPYING.OpenSSL FILES PORTING DEVELOPMENT
%{_bindir}/%{name}
%{_bindir}/procan
%{_bindir}/filan
#%%{_mandir}/man1/socat.1*
