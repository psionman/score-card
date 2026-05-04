[app]
title = Score Card
package.name = scorecard
package.domain = org.jeff
version = 0.1
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = src/score_card/fonts/*.ttf
icon.filename = src/score_card/images/score_card_icon.png
presplash.filename = src/score_card/images/score_card_splash.png


requirements = python3,kivy==2.2.1,pillow,kivymd==1.2.0,android,androidstorage4kivy

orientation = portrait
fullscreen = 0

[python]
adb logcat python:D *:S

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE
android.add_cmake_options = -DCMAKE_POLICY_VERSION_MINIMUM=3.5
