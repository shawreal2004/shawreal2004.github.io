"""Generate reproducible teaching figures from procedural arrays, not personal photos.
Requires Python, Pillow and NumPy. All coordinates and parameters are illustrative.
"""
from pathlib import Path
from io import BytesIO
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/images/encyclopedia'
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path('C:/Windows/Fonts/msyh.ttc')
FONT_BOLD = Path('C:/Windows/Fonts/msyhbd.ttc')
if not FONT.exists():
    # Override with an installed CJK font on other platforms.
    import os
    FONT = Path(os.environ['CJK_FONT'])
    FONT_BOLD = Path(os.environ.get('CJK_FONT_BOLD', str(FONT)))
BG = '#f7f4ed'
INK = '#2e4436'
MUTED = '#647165'
SAGE = '#e5eddf'
BLUE = '#dce9ee'
RUST = '#a95f49'
RESAMPLE = Image.Resampling
MANIFEST = {}

def font(size, bold=False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)

def label(im, xy, value, size=23, color=INK, bold=False, anchor=None):
    ImageDraw.Draw(im).text(xy, value, font=font(size, bold), fill=color, anchor=anchor)

def wrap(im, xy, value, width, size=22, color=MUTED, gap=7):
    d = ImageDraw.Draw(im)
    current, lines = '', []
    for ch in value:
        if ch == '\n' or (current and d.textlength(current + ch, font=font(size)) > width):
            lines.append(current)
            current = '' if ch == '\n' else ch
        else:
            current += ch
    if current:
        lines.append(current)
    for i, line in enumerate(lines):
        label(im, (xy[0], xy[1] + i * (size + gap)), line, size, color)
    return len(lines) * (size + gap)

def canvas(h, title, subtitle):
    im = Image.new('RGB', (1200, h), BG)
    label(im, (38, 23), title, 32, bold=True)
    label(im, (40, 69), subtitle, 19, MUTED)
    label(im, (40, h - 34), 'shaw 的手记 · 入门百科 · 程序绘制教学示例', 17, MUTED)
    return im

def save(im, name, parameters):
    path = OUT / name
    im.save(path, optimize=True)
    MANIFEST[name] = {'size': list(im.size), 'parameters': parameters}

def arrow(im, start, end, color=MUTED):
    d = ImageDraw.Draw(im)
    d.line([start, end], fill=color, width=4)
    a = np.arctan2(end[1] - start[1], end[0] - start[0])
    points = [end]
    for sign in [-1, 1]:
        points.append((end[0] - 14*np.cos(a + sign*.5), end[1] - 14*np.sin(a + sign*.5)))
    d.polygon(points, fill=color)

def box(im, rect, title, detail='', fill='white', size=24):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(rect, radius=14, fill=fill, outline='#d1d8cb', width=2)
    label(im, (rect[0]+20, rect[1]+15), title, size, bold=True)
    if detail:
        wrap(im, (rect[0]+20, rect[1]+57), detail, rect[2]-rect[0]-40, 20)

def scene():
    w, h = 600, 360
    x = np.linspace(0, 1, w)[None, :, None]
    y = np.linspace(0, 1, h)[:, None, None]
    base = np.broadcast_to(np.array([220., 224., 213.])[None, None, :] + 24*x - 35*y, (h,w,3)).copy()
    im = Image.fromarray(np.uint8(np.clip(base, 0, 255)))
    d = ImageDraw.Draw(im)
    d.rectangle((25,30,235,205), fill='#9fc6cf', outline='#334c49', width=5)
    d.polygon([(30,190),(85,130),(145,175),(200,95),(231,153),(231,201),(30,201)], fill='#779a78')
    d.ellipse((52,50,84,82), fill='#efdf9d')
    d.line((130,32,130,203), fill='#f9f6e8', width=6)
    d.line((26,111,234,111), fill='#f9f6e8', width=6)
    d.rectangle((0,252,599,359), fill='#b49e83')
    for yy in range(260,360,12):
        d.line((0,yy,599,yy), fill='#8d7d6c', width=1)
    d.rectangle((276,36,555,214), fill='#fbf8ee', outline='#3f5350', width=4)
    for yy in range(51,146,7):
        for xx in range(293,390,7):
            d.rectangle((xx,yy,xx+5,yy+5), fill='#1b3430' if ((xx-293)//7+(yy-51)//7)%2 else '#fdfbec')
    d.text((404,63), 'IQA', font=font(29, True), fill='#364e41')
    d.text((404,108), '012345', font=font(17), fill='#555b52')
    for j in range(8):
        d.line((298,168+j*3,540,168+j*3), fill='#344c44', width=1)
    d.polygon([(182,251),(490,251),(536,278),(133,278)], fill='#6d5040')
    d.rectangle((164,279,175,340), fill='#513e34')
    d.rectangle((486,279,497,340), fill='#513e34')
    d.ellipse((333,191,371,238), fill='#d08362', outline='#7b5045', width=3)
    for j in range(7):
        xx = 323 + j*9
        d.line((353,205,xx,155+abs(j-3)*9), fill='#5e7e4d', width=3)
        d.ellipse((xx-8,147+abs(j-3)*9,xx+9,167+abs(j-3)*9), fill='#688950')
    return im

REF = scene()
A = np.asarray(REF, dtype=np.float64)

def gaussian(a, sigma):
    r = int(np.ceil(3*sigma))
    xx = np.arange(-r,r+1)
    k = np.exp(-xx**2/(2*sigma**2)); k /= k.sum()
    result = a.copy()
    for axis in [0,1]:
        pads = [(0,0)] * a.ndim; pads[axis] = (r,r)
        padded = np.pad(result, pads, mode='reflect')
        out = np.zeros_like(result)
        for j, value in enumerate(k):
            sl = [slice(None)] * a.ndim; sl[axis] = slice(j,j+a.shape[axis])
            out += value * padded[tuple(sl)]
        result = out
    return result

def as_image(a):
    return Image.fromarray(np.uint8(np.clip(a,0,255)))

def compare_four(filename, title, subtitle, items, params):
    im = canvas(900, title, subtitle)
    d = ImageDraw.Draw(im)
    for index, (name, picture) in enumerate(items):
        x, y = 38+(index%2)*584, 110+(index//2)*365
        d.rounded_rectangle((x,y,x+546,y+343), radius=12, fill='white', outline='#d9dace', width=2)
        label(im,(x+15,y+9),name,24,bold=True)
        im.paste(picture.resize((516,231),RESAMPLE.LANCZOS),(x+15,y+48))
        # The identical crop reveals differences without comparing different content.
        crop = picture.crop((272,40,442,72)).resize((340,64),RESAMPLE.NEAREST)
        im.paste(crop,(x+191,y+279))
        label(im,(x+15,y+294),'同位置局部放大',17,MUTED)
    save(im,filename,params)

# Figure 1: numeric RGB values from actual sampled positions.
im=canvas(930,'01  从网格位置到 RGB 数值','像素是位置及其数值；方块是放大显示的方式。')
low=REF.resize((60,36),RESAMPLE.LANCZOS)
im.paste(low.resize((500,300),RESAMPLE.NEAREST),(40,140))
label(im,(40,110),'测试图采样为 60 × 36 后显示',21,bold=True)
ImageDraw.Draw(im).rectangle((40+28*500/60,140+4*300/36,40+32*500/60,140+8*300/36),outline=RUST,width=4)
label(im,(650,110),'标记区域的 4 × 4 个像素',21,bold=True)
vals=np.asarray(low)[4:8,28:32]
for yy in range(4):
    for xx in range(4):
        x,y=650+xx*125,147+yy*72
        c=tuple(int(v) for v in vals[yy,xx]); ImageDraw.Draw(im).rectangle((x,y,x+122,y+69),fill=c,outline='white',width=2)
        color='white' if np.mean(c)<130 else '#18241e'
        label(im,(x+61,y+35),str(c),15,color,anchor='mm')
label(im,(40,474),'三个通道各保存一张数值网格',24,bold=True)
for ch,(name,color) in enumerate([('R 红','#a25245'),('G 绿','#4f7750'),('B 蓝','#4b789b')]):
    x=40+ch*385
    channel=np.zeros_like(np.asarray(REF)); channel[:,:,ch]=np.asarray(REF)[:,:,ch]
    im.paste(Image.fromarray(channel).resize((350,210),RESAMPLE.LANCZOS),(x,538))
    label(im,(x,505),name,23,color,bold=True)
wrap(im,(40,792),'例如常见 8 bit RGB：红色 (255, 0, 0)，白色 (255, 255, 255)。通道顺序、颜色空间和数值范围都需要核对。',1110,22)
save(im,'pixels-rgb.png',{'sample_grid':[60,36],'crop_xy':[28,4,32,8],'display':'nearest-neighbor'})

# Figure 2: operational source labels rather than quality claims.
im=canvas(760,'02  来源记录与质量分数是两件事','用户上传可以包含 AI 内容；实际数据库需要明确来源分类规则。')
for i,(name,steps,fill) in enumerate([
    ('采集／用户内容',['拍摄或拼接','编辑与平台压缩','保留采集与处理链'],SAGE),
    ('AI 生成内容',['提示词／条件','生成模型与参数','保留生成来源'],BLUE),
    ('AI 编辑内容',['母图与编辑区域','扩图／修复／转换','保留母图与来源链'],'#f0e2d8'),
]):
    y=128+i*160
    label(im,(40,y+12),name,23,bold=True)
    for j,v in enumerate(steps):
        x=240+j*305
        box(im,(x,y,x+275,y+104),v,fill=fill,size=21)
        if j<2: arrow(im,(x+277,y+52),(x+298,y+52))
wrap(im,(40,628),'数据库需要分别记录：来源标签、内容家族、处理链、评分维度和真实主观标签。来源本身不表示好或坏。',1100,23)
save(im,'content-origins.png',{'type':'source-chain schematic'})

# Figures 3 and 4: controlled, reproducible image-processing simulations.
motion=np.pad(A,[(0,0),(10,10),(0,0)],mode='reflect')
motion=sum(motion[:,j:j+600,:] for j in range(21))/21
compare_four('blur-comparison.png','03  模糊怎样减弱边缘与细节','相同输入、相同显示尺寸；局部放大对应相同坐标。',[
    ('原图：未添加模糊',REF),('高斯模糊：σ = 1.5 px',as_image(gaussian(A,1.5))),
    ('高斯模糊：σ = 4 px',as_image(gaussian(A,4))),('水平运动核：长度 21 px',as_image(motion))],
    {'gaussian_sigma':[1.5,4],'motion_length':21,'motion_direction':'horizontal','boundary':'reflect'})
rng=np.random.default_rng(20261008)
gauss=as_image(A+rng.normal(0,20,A.shape))
poisson=as_image(rng.poisson(A/255*35)/35*255)
salt=A.copy(); mask=rng.random(A.shape[:2]); salt[mask<.02]=0; salt[(mask>=.02)&(mask<.04)]=255
compare_four('noise-comparison.png','04  噪声怎样增加颗粒与突变','统计模型用于教学，不是实际传感器噪声标定。',[
    ('原图：未添加噪声',REF),('加性高斯噪声：σ = 20',gauss),
    ('泊松模拟：峰值 35',poisson),('椒盐噪声：替换比例 4%',as_image(salt))],
    {'seed':20261008,'gaussian_sigma_8bit':20,'poisson_peak':35,'salt_pepper_fraction':.04})

# Figure 5: JPEG is actually encoded and decoded; ringing is explicit schematic.
buffer=BytesIO(); REF.save(buffer,format='JPEG',quality=5,subsampling=2); buffer.seek(0)
jpeg=Image.open(buffer).convert('RGB')
step=np.where(np.arange(280)<140,60.,190.)
dist=np.arange(280)-140
ring=step+45*np.sin(dist*.8)*np.exp(-np.abs(dist)/15)
edge0=as_image(np.repeat(np.tile(step,(130,1))[:,:,None],3,axis=2))
edge1=as_image(np.repeat(np.tile(ring,(130,1))[:,:,None],3,axis=2))
grad=np.linspace(40,210,280)[None,:,None]
grad=np.repeat(np.repeat(grad,130,axis=0),3,axis=2)
band=np.round(grad/32)*32
line=Image.new('RGB',(280,130),'#f3eee2'); ImageDraw.Draw(line).line((12,112,265,18),fill='#324f45',width=3)
alias=line.resize((40,19),RESAMPLE.NEAREST).resize((280,130),RESAMPLE.NEAREST)
yy,xx=np.indices((130,280)); stripes=127+110*np.sin(2*np.pi*(xx*.43+yy*.13))
stripe0=as_image(np.repeat(stripes[:,:,None],3,axis=2))
stripe1=stripe0.resize((72,34),RESAMPLE.NEAREST).resize((280,130),RESAMPLE.NEAREST)
sharp=as_image(A+2*(A-gaussian(A,2)))
im=canvas(1020,'05  常见伪影图谱','每个面板左侧为对照，右侧为失真／现象模拟；观察的是形态。')
pairs=[('压缩块：JPEG quality = 5',REF.crop((270,35,550,165)),jpeg.crop((270,35,550,165))),
       ('振铃：强边缘旁的明暗波纹',edge0,edge1),('色带：连续渐变变成阶梯',as_image(grad),as_image(band)),
       ('锯齿：斜线采样不足',line,alias),('混叠：重复细节变成假纹路',stripe0,stripe1),
       ('过度锐化：边缘光晕与过冲',REF.crop((265,32,545,162)),sharp.crop((265,32,545,162)))]
for i,(name,left,right) in enumerate(pairs):
    x,y=38+(i%2)*585,115+(i//2)*280
    label(im,(x,y),name,21,bold=True)
    im.paste(left.resize((255,160),RESAMPLE.NEAREST),(x,y+49))
    im.paste(right.resize((255,160),RESAMPLE.NEAREST),(x+275,y+49))
    label(im,(x,y+216),'对照',17,MUTED); label(im,(x+275,y+216),'变化后',17,RUST)
save(im,'artifact-atlas.png',{'jpeg_quality':5,'jpeg_subsampling':2,'band_step':32,'unsharp_amount':2,'ringing':'analytic edge schematic','aliasing':'nearest downsample without antialiasing'})

# Figure 6: semantic errors are drawn deliberately, not attributed to a model.
im=canvas(900,'06  画面清晰 结构也可能错误','人为绘制的示意；不代表真实生成器的输出分布。')
for row,name in enumerate(['椅腿连接关系','文字可读性','透视与线条连续性']):
    y=130+row*230
    label(im,(40,y-22),name,22,bold=True)
    for col in [0,1]:
        x=290+col*440
        d=ImageDraw.Draw(im); d.rounded_rectangle((x,y,x+390,y+175),radius=10,fill='white',outline='#d7d8cd',width=2)
        if row==0:
            d.rectangle((x+110,y+25,x+237,y+88),fill='#b78e67',outline='#5e4b3d',width=4)
            d.polygon([(x+87,y+94),(x+248,y+94),(x+271,y+114),(x+70,y+114)],fill='#826653')
            d.line((x+89,y+116,x+78,y+157),fill='#55473a',width=10)
            if col==0: d.line((x+246,y+115,x+256,y+158),fill='#55473a',width=10)
            else:
                d.line((x+263,y+137,x+270,y+160),fill='#55473a',width=10)
                d.ellipse((x+235,y+113,x+296,y+172),outline=RUST,width=4)
        elif row==1:
            if col==0: label(im,(x+195,y+85),'OPEN',62,bold=True,anchor='mm')
            else:
                rr=np.random.default_rng(9)
                for pos in range(4):
                    for j in range(8):
                        pts=rr.integers([x+68+pos*62,y+45],[x+109+pos*62,y+126],size=(2,2))
                        d.line([tuple(pts[0]),tuple(pts[1])],fill=INK,width=4)
        else:
            van=(x+195,y+47)
            d.rectangle((x+157,y+23,x+234,y+97),outline=INK,width=4)
            for pos in [20,110,280,375]:
                if col==0: d.line((pos+x,y+158,van[0],van[1]),fill='#8a795f',width=4)
                else: d.line([(pos+x,y+158),(x+140,y+105),(x+252,y+77),van],fill='#8a795f',width=4)
        label(im,(x,y+183),'连接／结构连贯' if col==0 else '结构／文字错误示意',18,MUTED if col==0 else RUST)
save(im,'semantic-errors.png',{'type':'hand-drawn geometry schematic; not an AI-generated sample'})

# Figure 7: periodic spherical direction field and actual perspective ray mapping.
pw,ph=1100,550
u=(np.arange(pw)+.5)/pw; v=(np.arange(ph)+.5)/ph
lon=2*np.pi*(u-.5)[None,:]; lat=np.pi*(.5-v)[:,None]
r=125+65*np.cos(lon)*np.cos(lat)
g=140+55*np.sin(lon)*np.cos(lat)
b=135+70*np.sin(lat)+np.zeros_like(lon)
pano=np.stack(np.broadcast_arrays(r,g,b),axis=2)
for center,lc in [(0,0), (np.pi/2,0), (0,np.pi/3)]:
    dot=np.sin(lat)*np.sin(lc)+np.cos(lat)*np.cos(lc)*np.cos(lon-center)
    ringmask=np.abs(np.arccos(np.clip(dot,-1,1))-.22)<.012
    pano[ringmask]=[245,235,209]
grid_lon=np.abs(np.mod(lon+np.pi/12,np.pi/6)-np.pi/12)<.009
grid_lat=np.abs(np.mod(lat+np.pi/12,np.pi/6)-np.pi/12)<.009
pano[np.broadcast_to(grid_lon,(ph,pw))|np.broadcast_to(grid_lat,(ph,pw))]=[55,72,64]
pano=as_image(pano)
base=np.asarray(pano,dtype=float)

def viewport(yaw,pitch,w=330,h=174,fov=90):
    hf=np.tan(np.deg2rad(fov)/2)
    x=((np.arange(w)+.5)/w*2-1)*hf
    y=(1-(np.arange(h)+.5)/h*2)*hf*h/w
    xx,yy=np.meshgrid(x,y)
    local=np.stack([xx,yy,np.ones_like(xx)],axis=2)
    local/=np.linalg.norm(local,axis=2,keepdims=True)
    ya,pi=np.deg2rad([yaw,pitch])
    forward=np.array([np.cos(pi)*np.sin(ya),np.sin(pi),np.cos(pi)*np.cos(ya)])
    right=np.array([np.cos(ya),0,-np.sin(ya)])
    up=np.cross(forward,right)
    ray=local[:,:,0,None]*right+local[:,:,1,None]*up+local[:,:,2,None]*forward
    lam=np.arctan2(ray[:,:,0],ray[:,:,2]); phi=np.arcsin(np.clip(ray[:,:,1],-1,1))
    sx=(lam/(2*np.pi)+.5)*pw-.5; sy=(.5-phi/np.pi)*ph-.5
    x0=np.floor(sx).astype(int); y0=np.floor(sy).astype(int)
    ax=sx-x0; ay=sy-y0
    y0c=np.clip(y0,0,ph-1); y1c=np.clip(y0+1,0,ph-1)
    result=(base[y0c,x0%pw]*(1-ax)[:,:,None]*(1-ay)[:,:,None]+base[y0c,(x0+1)%pw]*ax[:,:,None]*(1-ay)[:,:,None]
        +base[y1c,x0%pw]*(1-ax)[:,:,None]*ay[:,:,None]+base[y1c,(x0+1)%pw]*ax[:,:,None]*ay[:,:,None])
    return as_image(result)

im=canvas(960,'07  从 ERP 展开图到透视视口','方向场与经纬网仅用于几何演示；左右边界对应相邻方向。')
im.paste(pano,(50,132))
d=ImageDraw.Draw(im)
for number,yaw,pitch in [(1,0,0),(2,90,0),(3,0,60)]:
    x=50+(yaw/360+.5)*pw; y=132+(.5-pitch/180)*ph
    d.ellipse((x-17,y-17,x+17,y+17),fill='#fff7e7',outline=RUST,width=3)
    label(im,(x,y),str(number),20,RUST,bold=True,anchor='mm')
label(im,(50,102),'−180° 经度',19,MUTED); label(im,(1060,102),'180°',19,MUTED)
for i,(yaw,pitch,name) in enumerate([(0,0,'① 前方  yaw 0° / pitch 0°'),(90,0,'② 右方  yaw 90° / pitch 0°'),(0,60,'③ 上方  yaw 0° / pitch 60°')]):
    x=50+i*375
    label(im,(x,706),name,18,bold=True)
    im.paste(viewport(yaw,pitch),(x,740))
save(im,'erp-viewports.png',{'ERP':[pw,ph],'ray_convention':'x right, y up, z forward; longitude atan2(x,z)','viewport':[330,174],'horizontal_fov_deg':90,'views':[[0,0],[90,0],[0,60]],'interpolation':'bilinear; horizontal wrap; vertical clamp'})

# Figure 8: four fabricated scores, identical mean, different variability.
im=canvas(720,'08  平均分相同 意见分歧可以不同','四人评分只用于数学演示，不是主观实验数据。')
d=ImageDraw.Draw(im)
for row,(name,scores) in enumerate([('示例 A',[3,3,3,3]),('示例 B',[1,1,5,5])]):
    y=135+row*190
    label(im,(40,y+18),name,25,bold=True)
    for i,score in enumerate(scores):
        x=235+i*130
        d.rounded_rectangle((x,y,x+91,y+105),radius=10,fill=SAGE if row==0 else '#eddaca')
        label(im,(x+45,y+46),str(score),38,bold=True,anchor='mm')
        label(im,(x+45,y+88),f'观察者 {i+1}',16,MUTED,anchor='mm')
    label(im,(820,y+18),'MOS = 3',31,bold=True)
    label(im,(820,y+68),'评分一致' if row==0 else '评分分歧大',24,MUTED)
wrap(im,(40,552),'评分协议还需明确：评价维度、设备与显示、观看时间、起始朝向、顺序随机化、有效观察者与评分处理。',1100,24)
save(im,'mos-and-uncertainty.png',{'scores':[[3,3,3,3],[1,1,5,5]],'means':[3,3],'provenance':'fabricated teaching values'})

# Figure 9: split at family level before derived views.
im=canvas(760,'09  内容家族先划分 再派生视口','同一全景的视口共享内容，不能靠换文件名获得独立样本。')
label(im,(40,125),'风险示意：先提视口，再随机拆分',25,RUST,bold=True)
box(im,(40,180,245,294),'全景 A','同一内容家族',fill='#f0e2d8')
for i,name in enumerate(['A 的前方视口 → 训练','A 的右方视口 → 测试']):
    yy=168+i*90
    box(im,(345,yy,1100,yy+73),name,fill='#f0e2d8',size=24)
    arrow(im,(247,236),(332,yy+37),RUST)
label(im,(40,365),'划分原则：先隔离内容家族，再生成视口',25,bold=True)
for i,(family,split) in enumerate([('内容家族 A','训练集'),('内容家族 B','验证集'),('内容家族 C','测试集')]):
    x=40+i*385
    box(im,(x,425,x+345,573),family,f'{split}\n全部派生版本与视口保持在组内',fill=SAGE,size=24)
wrap(im,(40,641),'分组还需要检查：同场景、失真版本、AI 编辑母图、条件图、近重复图片与数据来源重叠。',1100,22)
save(im,'content-split.png',{'type':'family-level split schematic; no actual dataset split'})

(OUT/'figure-manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Generated {len(MANIFEST)} figures in {OUT}')
