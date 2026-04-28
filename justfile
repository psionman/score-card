list:
    just --list

run arg1="" arg2=""  arg3 = "":
    uv run main.py {{arg1}} {{arg2}} {{arg3}}

build arg1="":
    .venv/bin/buildozer android debug

deploy arg1="":
    .venv/bin/buildozer android debug deploy run

clean:
    buildozer android clean
    rm -rf .buildozer/android/platform/build/build/other_builds/jpeg*
    rm -rf .buildozer/android/platform/build/build/other_builds/libjpeg-turbo*
    rm -rf .buildozer/android/platform/build/packages/jpeg*
    rm -rf .buildozer/android/platform/build/packages/libjpeg-turbo*
    buildozer android debug deploy run


test arg1="":
    uv run -m pytest {{arg1}}
