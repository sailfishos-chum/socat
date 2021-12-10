socat packaging for Sailfish OS

# Build

- clone into `socat-packaging`
- `cd socat-packaging/socat`
- in build engine (`sfdk engine exec`):
  `sb2 -t SailfishOS-4.3.0.12-aarch64 rpmbuild --build-in-place -bb ../rpm/socat.spec --nocheck`

  which strips symbols,
  or simply

- `sfdk build -p --no-check`

  sfdk does not strip symbols.


The package should build reproducibly.
