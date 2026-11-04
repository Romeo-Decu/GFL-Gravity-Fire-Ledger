"""Per-frame flame geometry survey for a directory of BASS NEF stills (bbox of relative radiance > 5e5 counts/s)."""
import rawpy,exifread,glob,json,sys,numpy as np
from datetime import datetime
from multiprocessing import Pool
D=sys.argv[1]
def one(f):
    t=exifread.process_file(open(f,'rb'),details=False)
    dt=datetime.strptime(str(t['EXIF DateTimeOriginal']),'%Y:%m:%d %H:%M:%S'); sub=str(t.get('EXIF SubSecTimeOriginal','0')).strip() or '0'
    n,d=(str(t['EXIF ExposureTime'])+'/1').split('/')[:2]; exp=float(n)/float(d)
    with rawpy.imread(f) as r: lin=r.postprocess(gamma=(1,1),no_auto_bright=True,output_bps=16,half_size=True,use_camera_wb=True,user_flip=0)
    Y=(0.2126*lin[...,0]+0.7152*lin[...,1]+0.0722*lin[...,2])/exp; bg=float(np.median(Y)); S=Y-bg
    m=S>5e5; rec=dict(f=f.rsplit('/',1)[-1],ts=dt.timestamp()+int(sub)/10**len(sub),exp=exp,bg=bg,npx=int(m.sum()))
    if m.sum()>200:
        ys,xs=np.where(m); rec.update(x0=int(np.percentile(xs,1)),x1=int(np.percentile(xs,99)),y0=int(np.percentile(ys,1)),y1=int(np.percentile(ys,99)))
    return rec
if __name__=='__main__':
    fs=sorted(glob.glob(D+'/*.NEF'))
    with Pool(8) as p: R=p.map(one,fs)
    json.dump(R,open(sys.argv[2],'w'))
