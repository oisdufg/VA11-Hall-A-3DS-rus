"""Package the separate local test launcher; reuse the regular music installation."""
from pathlib import Path
import hashlib,json,zipfile

def package(project):
    sd=project/'sd/3ds/va11-3ds-test';sd.mkdir(parents=True,exist_ok=True)
    icon=bytearray((project/'sd/3ds/va11-3ds/va11-3ds.smdh').read_bytes())
    def title(value,length):return value.encode('utf-16le')[:length-2].ljust(length,b'\0')
    for i in range(16):
        icon[8+i*512:8+(i+1)*512]=title('VA-11 HALL-A TEST',128)+title('Days 1-5 / Shop test / 0.8.0',256)+title('build with neumiraie',128)
    (sd/'va11-3ds-test.smdh').write_bytes(icon)
    files={f'3ds/va11-3ds-test/{name}':sd/name for name in ('va11-3ds-test.3dsx','va11-3ds-test.smdh')}
    files['TEST-BUILD.md']=project/'TEST-BUILD.md'
    manifest={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in files.items()}
    dest=project.parent/'VA11-3DS-0.8.0-test.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as archive:
        for name,path in files.items():archive.write(path,name)
        archive.writestr('test-manifest.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist())==set(files)|{'test-manifest.json'}
        for name,digest in manifest.items():assert hashlib.sha256(archive.read(name)).hexdigest()==digest
    print(dest,dest.stat().st_size)

if __name__=='__main__':package(Path(__file__).resolve().parents[1])
