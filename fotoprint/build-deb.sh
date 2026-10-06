#!/bin/bash
# Gera dist/fotoprint_<versão>_all.deb (requer apenas dpkg-deb).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

VERSION="$(sed -n 's/^Version: //p' packaging/DEBIAN/control)"
PKG="fotoprint_${VERSION}_all"
STAGE="$(mktemp -d)/$PKG"
trap 'rm -rf "$(dirname "$STAGE")"' EXIT

mkdir -p "$STAGE/DEBIAN" \
         "$STAGE/usr/lib/python3/dist-packages" \
         "$STAGE/usr/bin" \
         "$STAGE/usr/share/applications" \
         "$STAGE/usr/share/icons/hicolor/scalable/apps" \
         "$STAGE/usr/share/doc/fotoprint"

cp packaging/DEBIAN/control packaging/DEBIAN/postinst packaging/DEBIAN/prerm "$STAGE/DEBIAN/"
chmod 755 "$STAGE/DEBIAN/postinst" "$STAGE/DEBIAN/prerm"

cp -r fotoprint "$STAGE/usr/lib/python3/dist-packages/fotoprint"
find "$STAGE" -name '__pycache__' -type d -prune -exec rm -rf {} +

printf '#!/bin/sh\nexec python3 -m fotoprint "$@"\n' > "$STAGE/usr/bin/fotoprint"
chmod 755 "$STAGE/usr/bin/fotoprint"

install -m 644 packaging/fotoprint.desktop "$STAGE/usr/share/applications/fotoprint.desktop"
install -m 644 packaging/fotoprint.svg "$STAGE/usr/share/icons/hicolor/scalable/apps/fotoprint.svg"
for size in 16 24 32 48 64 128 256 512; do
    mkdir -p "$STAGE/usr/share/icons/hicolor/${size}x${size}/apps"
    install -m 644 "packaging/icons/fotoprint-${size}.png" \
        "$STAGE/usr/share/icons/hicolor/${size}x${size}/apps/fotoprint.png"
done
install -m 644 README.md "$STAGE/usr/share/doc/fotoprint/README.md"

find "$STAGE" -type d -exec chmod 755 {} +
find "$STAGE/usr" -type f ! -path '*/bin/*' -exec chmod 644 {} +

mkdir -p dist
dpkg-deb --root-owner-group --build "$STAGE" "dist/${PKG}.deb"
echo "Pacote criado em: $ROOT/dist/${PKG}.deb"
