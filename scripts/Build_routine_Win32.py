import os, sys

version = sys.version_info[:2]

os.system('C:\Python%d%d\Scripts\pyi-makespec -F -c --icon=Resources\Cecilia5.ico "Cecilia5.py"' % version)
os.system('C:\Python%d%d\Scripts\pyi-build "Cecilia5.spec"' % version)

os.system("git checkout-index -a -f --prefix=Cecilia5_Win/")
os.system("copy dist\Cecilia5.exe Cecilia5_Win /Y")
os.system("rmdir /Q /S Cecilia5_Win\scripts")
os.system("rmdir /Q /S Cecilia5_Win\doc-en")
os.remove("Cecilia5_Win/Cecilia5.py")
os.remove("Cecilia5_Win/Resources/Cecilia5.icns")
os.remove("Cecilia5_Win/Resources/CeciliaFileIcon5.icns")
os.remove("Cecilia5.spec")
os.system("rmdir /Q /S build")
os.system("rmdir /Q /S dist")
for f in os.listdir(os.getcwd()):
    if f.startswith("warn") or f.startswith("logdict"):
        os.remove(f)

