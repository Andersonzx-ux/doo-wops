# Bruno Mars — Doo-Wops & Hooligans (player)

Player estático (HTML/CSS/JS, sem build) para GitHub Pages. Dados em `data/album.js`.

## Paleta (medida nos pixels da capa)
| Papel | Cor | Origem |
|---|---|---|
| black | `#14130F` | foguete e homem |
| yellow | `#F8BE25` | amarelo de gráfica do fundo |
| cream | `#FBF0C3` | caminho e margem |
| butter | `#F8E7AB` | letras "BRUNO MARS" |
| sand | `#D6CBA7` | sombra do homem |
| amber | `#E8A317` | o amarelo da capa um tom mais fundo (tinta do trecho já percorrido) |

## Identidade
- **Progresso = o caminho sinuoso**: do homem (início) ao foguete (fim), o caminho creme da capa vai ganhando o amarelo mais fundo conforme a faixa toca; um ponto preto marca onde ela está. Toque ou arraste no caminho para buscar na faixa (cliques fora do caminho não fazem nada). A barra comum continua funcionando.
- O nome "BRUNO MARS" aparece sob a capa como recorte real das letras (`assets/nome-mask.webp`).
- **Dia / Noite**: Dia = papel creme, texto no preto do foguete, amarelo como cor viva; Noite = preto do foguete com o amarelo como luz. A escolha fica salva.
- Fonte: Jost (OFL, em `assets/fonts/`). Central de mídia (Media Session) com capa, anterior/próxima e seek.

## Antes de publicar
`data/album.js` traz as 11 faixas da edição padrão com áudios `audio/01.flac` … `audio/11.flac`, sem letras, compositores nem durações (a duração aparece sozinha ao tocar). Confira a ordem, os títulos e a data, e cole as letras `.lrc` em `lyrics` (e a tradução, se quiser, em `translation`).

## Arquivos
`index.html`, `css/style.css`, `js/{app,player,ui,road}.js`, `data/album.js`, `assets/{cover.jpg, cover-256.jpg, cover-512.jpg, nome-mask.webp, fonts/}`, `tools/` (gera o mapa do caminho `js/road.js` e os recortes a partir da capa).
