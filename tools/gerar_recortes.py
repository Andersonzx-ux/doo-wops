# Gera os recortes reais da capa: mapa do caminho (progresso), máscara do nome e miniaturas.
# Uso (na raiz do projeto):  python3 -I tools/gerar_recortes.py
import base64, io, json
from collections import deque
import numpy as np
from scipy import ndimage as ndi
from PIL import Image

im = Image.open('assets/cover.jpg').convert('RGB')
W, H = im.size
im.resize((256, 256), Image.LANCZOS).save('assets/cover-256.jpg', quality=88)
im.resize((512, 512), Image.LANCZOS).save('assets/cover-512.jpg', quality=90)
a = np.asarray(im).astype(float)
B = a[..., 2]; lum = a @ [.2126, .7152, .0722]

# --- 1) o caminho creme (azul alto = creme; amarelo tem azul baixo), só dentro da área amarela da capa
X0, Y0, X1, Y1 = 21, 20, 619, 613
box = np.zeros((H, W), bool); box[Y0:Y1 + 1, X0:X1 + 1] = True
cream = (B > 110) & box
lab, n = ndi.label(cream)
sizes = ndi.sum(cream, lab, range(1, n + 1))
road = lab == (1 + int(np.argmax(sizes)))                 # maior componente = o caminho (letras ficam de fora)
road_f = ndi.binary_fill_holes(ndi.binary_closing(road, iterations=3))   # fecha os buracos (homem, foguete)
road_d = ndi.binary_dilation(road_f, iterations=2)

# --- 2) ordem ao longo do caminho: distância pelo próprio caminho a partir da borda de baixo (o homem) até o foguete
INF = 10 ** 9
dist = np.full((H, W), INF, np.int32)
dq = deque()
for x in range(W):
    if road_d[Y1 - 1, x]: dist[Y1 - 1, x] = 0; dq.append((Y1 - 1, x))
while dq:
    y, x = dq.popleft(); d = dist[y, x] + 1
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < H and 0 <= xx < W and road_d[yy, xx] and dist[yy, xx] == INF:
            dist[yy, xx] = d; dq.append((yy, xx))
ok = (dist < INF)
dmax = dist[ok].max()
order = np.zeros((H, W), np.uint8)
order[ok] = 1 + (dist[ok] * 254 // dmax)                  # 1..255 (0 = fora do caminho)

# --- 3) cobertura suavizada (borda do caminho sem serrilhado): 0..255
cov = np.clip((B - 60) / 110.0, 0, 1) * ok
cov = np.maximum(cov, ndi.binary_erosion(road_f, iterations=2) * ok * 0)   # buracos (homem) continuam sem cobertura
out = np.zeros((H, W, 3), np.uint8); out[..., 0] = order; out[..., 1] = (cov * 255).astype(np.uint8)
buf = io.BytesIO(); Image.fromarray(out, 'RGB').save(buf, 'PNG', optimize=True)
# centroides por valor de ordem (posição do "caminhante" na capa, em fração)
cent = []
last = (0.5, 0.95)
for v in range(256):
    m = (order >= max(1, v - 1)) & (order <= v + 1) & (order > 0)
    ys, xs = np.nonzero(m)
    if len(xs): last = (float(xs.mean() / W), float(ys.mean() / H))
    cent.append([round(last[0], 4), round(last[1], 4)])
with open('js/road.js', 'w') as f:
    f.write('/* Mapa do caminho da capa (gerado por tools/gerar_recortes.py): R = ordem ao longo do caminho (1..255), G = cobertura. */\n')
    f.write('window.ROAD = {w: %d, h: %d, png: "data:image/png;base64,%s", pos: %s};\n' % (W, H, base64.b64encode(buf.getvalue()).decode(), json.dumps(cent, separators=(',', ':'))))

# --- 4) máscara do nome "BRUNO MARS" (letras creme sobre amarelo): x 452–598, y 326–416
nx0, ny0, nx1, ny1 = 452, 326, 598, 416
bb = a[ny0:ny1, nx0:nx1, 2]
al = np.clip((bb - 60) / 110.0, 0, 1); al[al < 0.08] = 0
o = np.zeros(al.shape + (4,), np.uint8); o[..., 3] = (al * 255).astype(np.uint8)
Image.fromarray(o, 'RGBA').resize(((nx1 - nx0) * 3, (ny1 - ny0) * 3), Image.LANCZOS).save('assets/nome-mask.webp', quality=92)
print('ok', n, int(dmax), buf.tell())
