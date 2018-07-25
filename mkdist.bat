@echo off
pyinstaller timtools/scripts/openmail.py -y
pyinstaller timtools/scripts/prn2pdf.py -y
pyinstaller timtools/scripts/prnprint.py -y
pyinstaller timtools/scripts/sync.py -y
pyinstaller timtools/scripts/sendmail.py -y
cd dist
mkdir timtools
xcopy openmail\* timtools /s/y
xcopy prn2pdf\* timtools /s/y
xcopy prnprint\* timtools /s/y
xcopy sync\* timtools /s/y
xcopy sendmail\* timtools /s/y
python -m zipfile -c ..\docs\dl\timtools.zip timtools
cd ..
dir docs\dl\timtools.zip
