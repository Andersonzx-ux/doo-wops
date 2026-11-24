# Mede as cores da capa. Uso: python3 -I tools/medir_paleta.py assets/cover.jpg
import sys, numpy as np
from PIL import Image
a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
hx = lambda c: '#%02x%02x%02x' % tuple(int(round(v)) for v in c)
def reg(n, x0, y0, x1, y1):
    r = a[y0:y1, x0:x1].reshape(-1, 3); print(f'{n:12s} {hx(np.median(r, 0))}')
reg('caminho', 250, 300, 330, 380); reg('amarelo', 20, 300, 70, 420); reg('letras', 470, 340, 560, 370)
reg('homem', 415, 500, 440, 530); reg('sombra', 470, 570, 540, 590)
