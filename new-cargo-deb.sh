#!/bin/bash

temp=$(tempfile)d
mkdir -p $temp
cd $temp

echo $temp

triple=x86_64-unknown-linux-gnu
curl -O https://static.rust-lang.org/cargo-dist/cargo-nightly-$triple.tar.gz
tar xf cargo-nightly-$triple.tar.gz

snapshot=$(cat cargo-nightly-$triple/version | awk '{ print $3 }' | tr -d '\-)')

version=0.0.1+1SNAPSHOT$snapshot-0ubuntu0~trusty
mkdir -p cargo_$version/DEBIAN
mkdir -p cargo_$version/usr/local

cat > cargo_$version/DEBIAN/control << EOF
Package: cargo
Version: $version
Section: base
Priority: optional
Architecture: amd64
Depends: rust-nightly
Maintainer: Andrei Vacariu <andrei@avacariu.me>
Description: Rust's Package Manager
 Cargo downloads your Rust project’s dependencies and compiles your project.
EOF

cp -r cargo-nightly-$triple/cargo/bin cargo_$version/usr/local/
cp -r cargo-nightly-$triple/cargo/etc cargo_$version/usr/local/
cp -r cargo-nightly-$triple/cargo/lib cargo_$version/usr/local/
cp -r cargo-nightly-$triple/cargo/share cargo_$version/usr/local/

find cargo_$version/usr/local -type d -exec chmod 755 "{}" \;
find cargo_$version/usr/local -type f -exec chmod 644 "{}" \;

chmod +x cargo_$version/usr/local/bin/cargo

dpkg-deb --build cargo_$version

echo "Install using: sudo dpkg -i $temp/cargo_$version.deb"
