[app]
title = Masked Signal App
package.name = maskedsignalApp
package.domain = org.maskedsignal
source.dir =.
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests,certifi
orientation = portrait
android.api = 31
android.minapi = 24
android.permissions = INTERNET
android.archs = arm64-v8a
icon.filename = icon.png
p4a.branch = master

[buildozer]
log_level = 2