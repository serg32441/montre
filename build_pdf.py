#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""АО «Монтре» — презентация для инвесторов (PDF)."""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from PIL import Image

A = "/home/user/sochi-photographer/assets"
TMP = "/tmp/deck"
OUT = f"{A}/montre-investor-deck.pdf"
W, H = A4  # 595.27 x 841.89

# ── шрифты ──
LF = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif", LF+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", LF+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", LF+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B", LF+"LiberationSans-Bold.ttf"))

# ── гамма ──
CREAM=HexColor("#F5F0E8"); WW=HexColor("#FAF8F4"); GOLD=HexColor("#B8965A")
GOLDL=HexColor("#D4B07A"); DARK=HexColor("#1A1714"); DARKMID=HexColor("#2E2A26")
MUTED=HexColor("#7A746C"); BORDER=HexColor("#E4DAC8"); INK=HexColor("#2B2820")

M = 52  # поля
c = canvas.Canvas(OUT, pagesize=A4)

def yt(top): return H-top

def tracked(x, top, text, font, size, color, tr, center=False, right=False):
    # посимвольный вывод с трекингом — без утечки состояния char-space
    c.setFont(font, size); c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tr*max(0, len(text)-1)
    cx = x - total/2 if center else (x - total if right else x)
    yy = yt(top)
    for ch, w in zip(text, widths):
        c.drawString(cx, yy, ch); cx += w + tr

def bg(dark=False):
    c.setFillColor(DARK if dark else WW)
    c.rect(0,0,W,H,fill=1,stroke=0)

def eyebrow(x, top, text, color=GOLD):
    tracked(x, top, text.upper(), "Sans-B", 8.5, color, 2.6)

def title(x, top, text, size=25, color=INK, font="Serif-B"):
    c.setFont(font, size); c.setFillColor(color)
    c.drawString(x, yt(top), text)

def rule(x, top, w, color=GOLD, lw=1):
    c.setStrokeColor(color); c.setLineWidth(lw)
    c.line(x, yt(top), x+w, yt(top))

def para(text, x, top, w, size=10.5, leading=16, color=INK, font="Sans",
         align=4, space=0):
    st = ParagraphStyle("s", fontName=font, fontSize=size, leading=leading,
                        textColor=color, alignment=align, spaceAfter=space)
    p = Paragraph(text, st); _, h = p.wrap(w, 1000); p.drawOn(c, x, yt(top)-h)
    return top + h

def footer(n):
    rule(M, 800, W-2*M, BORDER, 0.8)
    c.setFont("Sans", 7.5); c.setFillColor(MUTED)
    c.drawString(M, yt(812), "АО «Монтре» · Презентация для инвесторов")
    c.drawRightString(W-M, yt(812), f"{n:02d}")
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, yt(812), "montrecapital.ru")

def crop_cover(src, ratio, key):
    im = Image.open(src).convert("RGB"); w,h = im.size
    tr = ratio
    if w/h > tr:
        nw = int(h*tr); im = im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else:
        nh = int(w/tr); im = im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    out = f"{TMP}/c_{key}.jpg"; im.save(out, quality=88); return out

def img_box(src, x, top, w, h, ratio=None, radius=0):
    if ratio is None: ratio = w/h
    p = crop_cover(src, ratio, f"{int(x)}_{int(top)}_{int(w)}")
    c.drawImage(p, x, yt(top)-h, w, h, mask='auto')

# ════════════════════════════ СТР. 1 — ОБЛОЖКА ════════════════════════════
bg(dark=True)
# тонкая золотая рамка
c.setStrokeColor(GOLD); c.setLineWidth(1)
c.rect(28,28,W-56,H-56,fill=0,stroke=1)
c.setStrokeColor(HexColor("#3a3026")); c.setLineWidth(0.6)
c.rect(34,34,W-68,H-68,fill=0,stroke=1)
# логотип
logo = ImageReader(f"{A}/logo.png")
lw = 210; lh = lw*(1480/1065)  # пропорции logo.png
c.drawImage(logo, (W-lw)/2, H-150-lh, lw, lh, mask='auto')
# заголовок
c.setFillColor(CREAM); c.setFont("Serif-B", 33)
c.drawCentredString(W/2, 330, "Доходные дома")
c.setFont("Serif", 21); c.setFillColor(GOLDL)
c.drawCentredString(W/2, 298, "инвестиции в реальные активы")
# линия
c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(W/2-40, 270, W/2+40, 270)
tracked(W/2, H-243, "ПРЕЗЕНТАЦИЯ ДЛЯ ИНВЕСТОРОВ", "Sans", 11, HexColor("#C9C2B6"), 3, center=True)
# низ
c.setFont("Sans", 9.5); c.setFillColor(HexColor("#8a8276"))
c.drawCentredString(W/2, 70, "2026 · montrecapital.ru")
c.showPage()

# ════════════════════════════ СТР. 2 — О КОМПАНИИ ═════════════════════════
bg()
eyebrow(M, 70, "О компании")
title(M, 100, "Возвращаем зданиям историю,")
title(M, 130, "создаём арендный доход")
rule(M, 150, 46, GOLD, 2)
y = para(
 "АО «Монтре» развивает сеть доходных домов в России. Мы выкупаем исторические "
 "и недооценённые здания, проводим реставрацию и качественный ремонт и сдаём "
 "готовые помещения в долгосрочную аренду. С 2023 года компания планомерно "
 "формирует портфель: участвует в муниципальных аукционах и приобретает объекты "
 "в собственность или долгосрочную аренду на срок не менее 49 лет.",
 M, 176, W-2*M, leading=17, color=DARKMID)
y = para(
 "Особый фокус — объекты культурного наследия, которые мы приспосабливаем для "
 "современного использования, сохраняя облик памятника. Такой продукт дефицитен, "
 "устойчив в цене и востребован на рынке аренды.",
 M, y+10, W-2*M, leading=17, color=DARKMID)

# карточки-цифры
stats=[("20+","аукционов пройдено с 2023 года"),
       ("6","объектов в собственности и аренде"),
       ("7 700","м² в текущих проектах"),
       ("49","лет — горизонт долгосрочной аренды")]
bx=M; bw=(W-2*M-3*14)/4; bh=92; topcards=y+34
for i,(num,lab) in enumerate(stats):
    x=bx+i*(bw+14)
    c.setFillColor(CREAM); c.setStrokeColor(BORDER); c.setLineWidth(1)
    c.rect(x, yt(topcards+bh), bw, bh, fill=1, stroke=1)
    c.setFillColor(GOLD); c.setStrokeColor(GOLD); c.setLineWidth(2)
    c.line(x, yt(topcards+bh), x+bw, yt(topcards+bh))
    c.setFont("Serif-B", 25); c.setFillColor(INK)
    c.drawString(x+12, yt(topcards+34), num)
    st=ParagraphStyle("c",fontName="Sans",fontSize=8.6,leading=11.5,textColor=MUTED)
    Paragraph(lab,st).wrapOn(c,bw-22,60)
    p=Paragraph(lab,st); _,hh=p.wrap(bw-22,60); p.drawOn(c,x+12,yt(topcards+bh)+12)

# принципы
py=topcards+bh+40
eyebrow(M, py, "Что отличает нашу модель")
prin=[("Реальные активы","За каждым проектом — конкретное здание с адресом и документами."),
      ("Полный цикл","Выкуп, реставрация, ремонт и управление арендой — под единым контролем."),
      ("Прозрачность","Понятная отчётность по стадиям проекта и арендным поступлениям.")]
cw=(W-2*M-2*16)/3; cy=py+18
for i,(t,d) in enumerate(prin):
    x=M+i*(cw+16)
    c.setFillColor(GOLD); c.setFont("Serif-B",13); c.drawString(x,yt(cy+4),t)
    st=ParagraphStyle("p",fontName="Sans",fontSize=9.3,leading=14,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(cw,80); p.drawOn(c,x,yt(cy+22)-hh)
footer(2); c.showPage()

# ════════════════════════════ СТР. 3 — БИЗНЕС-МОДЕЛЬ ══════════════════════
bg()
eyebrow(M,70,"Бизнес-модель")
title(M,100,"Полный цикл — от аукциона до аренды")
rule(M,120,46,GOLD,2)
para("Каждый объект проходит один и тот же выверенный путь. Это делает результат "
     "предсказуемым, а для инвестора — понятным на любом этапе.",
     M,146,W-2*M,leading=16,color=DARKMID)

steps=[("01","Выкуп объекта","Покупка зданий в сильных локациях на аукционах — в собственность или аренду на 49 лет."),
       ("02","Реставрация","Восстановление фасада и инженерии, приспособление памятника к новому использованию."),
       ("03","Ремонт и запуск","Создание готового арендного жилья и заселение арендаторов."),
       ("04","Доход и рост","Регулярный арендный поток и рост стоимости самого актива.")]
top=215; cw=(W-2*M-3*14)/4
for i,(n,t,d) in enumerate(steps):
    x=M+i*(cw+14)
    cx=x+26; cyc=yt(top+26)
    c.setStrokeColor(GOLD); c.setLineWidth(1.4); c.circle(cx,cyc,22,fill=0,stroke=1)
    c.setFont("Serif-B",15); c.setFillColor(GOLD); c.drawCentredString(cx,cyc-6,n)
    if i<3:
        c.setStrokeColor(GOLDL); c.setLineWidth(1)
        c.line(x+54,cyc, x+cw+8,cyc)
    c.setFont("Serif-B",13.5); c.setFillColor(INK); c.drawString(x,yt(top+74),t)
    st=ParagraphStyle("s",fontName="Sans",fontSize=9.2,leading=13.5,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(cw,140); p.drawOn(c,x,yt(top+92)-hh)

# нижний акцент-блок
by=406
c.setFillColor(DARK); c.rect(M,yt(by+118),W-2*M,118,fill=1,stroke=0)
c.setFillColor(GOLD); c.setFont("Serif-B",16)
c.drawString(M+30,yt(by+44),"Контроль на всех этапах — внутри компании")
st=ParagraphStyle("x",fontName="Sans",fontSize=10.5,leading=16,textColor=HexColor("#CFC8BC"))
p=Paragraph("Мы не зависим от случайных подрядчиков: отбор объекта, строительство, "
            "реставрация и последующее управление арендой выполняются в рамках единой "
            "группы. Это снижает риски сроков и качества и делает экономику проекта прозрачной.",st)
_,hh=p.wrap(W-2*M-60,120); p.drawOn(c,M+30,yt(by+62)-hh)
footer(3); c.showPage()

# ════════════════════════════ СТР. 4 — ПОЧЕМУ ════════════════════════════
bg()
eyebrow(M,70,"Почему доходные дома")
title(M,100,"Устойчивый спрос и понятный доход")
rule(M,120,46,GOLD,2)
colw=(W-2*M-40)/2
factors=[("Снижение доступности покупки","Высокие ставки и ужесточение ипотеки переориентируют спрос с покупки на аренду качественного жилья."),
         ("Рост мобильности","Всё больше людей выбирают гибкость аренды вместо долгосрочных обязательств при покупке."),
         ("Дефицит качества","Рынок профессиональной долгосрочной аренды в российских городах только формируется.")]
fy=160
for i,(t,d) in enumerate(factors):
    yy=fy+i*78
    c.setFont("Serif-B",13); c.setFillColor(GOLD)
    c.drawString(M,yt(yy),f"0{i+1}")
    c.setFillColor(INK); c.drawString(M+30,yt(yy),t)
    st=ParagraphStyle("f",fontName="Sans",fontSize=9.6,leading=14,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(colw-30,80); p.drawOn(c,M+30,yt(yy+16)-hh)

# правый блок — донат источников дохода
rx=M+colw+40
c.setFillColor(CREAM); c.setStrokeColor(BORDER); c.setLineWidth(1)
c.rect(rx,yt(fy+250),colw,260,fill=1,stroke=1)
tracked(rx+20, fy+24, "ИСТОЧНИКИ ДОХОДА ИНВЕСТОРА", "Sans-B", 8.5, GOLD, 1.6)
c.drawImage(ImageReader(f"{TMP}/sources.png"),rx+colw/2-80,yt(fy+185),160,160,mask='auto')
# легенда
ly=fy+200
c.setFillColor(GOLD); c.rect(rx+24,yt(ly+9),11,11,fill=1,stroke=0)
c.setFillColor(INK); c.setFont("Sans-B",9.5); c.drawString(rx+42,yt(ly),"Арендный поток — 70%")
c.setFillColor(DARKMID); c.rect(rx+24,yt(ly+27),11,11,fill=1,stroke=0)
c.setFillColor(INK); c.drawString(rx+42,yt(ly+18),"Рост стоимости актива — 30%")
st=ParagraphStyle("n",fontName="Sans",fontSize=8,leading=11,textColor=MUTED)
p=Paragraph("Иллюстративное распределение. Соотношение зависит от объекта и стратегии.",st)
_,hh=p.wrap(colw-40,40); p.drawOn(c,rx+24,yt(fy+250)+14)
footer(4); c.showPage()

# ════════════════════════════ СТР. 5 — ЭКОНОМИКА ══════════════════════════
bg()
eyebrow(M,70,"Экономика объекта")
title(M,100,"Как формируется доход инвестора")
rule(M,120,46,GOLD,2)
para("Доход складывается из арендных платежей и постепенного роста стоимости "
     "отреставрированного здания. Ниже — ориентировочная модель окупаемости.",
     M,146,W-2*M,leading=16,color=DARKMID)
# график окупаемости
c.drawImage(ImageReader(f"{TMP}/payback.png"),M,yt(190+255),300,255,mask='auto')
# правый блок — ключевые метрики
rx=M+320; rw=W-M-rx
metrics=[("10–14%","доходность от аренды в год (прогноз)"),
         ("8–9 лет","ориентировочная окупаемость"),
         ("49 лет","горизонт аренды / собственность")]
my=188
for num,lab in metrics:
    c.setFillColor(CREAM); c.setStrokeColor(BORDER); c.setLineWidth(1)
    c.rect(rx,yt(my+72),rw,72,fill=1,stroke=1)
    c.setStrokeColor(GOLD); c.setLineWidth(3); c.line(rx,yt(my),rx,yt(my+72))
    c.setFont("Serif-B",22); c.setFillColor(INK); c.drawString(rx+16,yt(my+34),num)
    c.setFont("Sans",9); c.setFillColor(MUTED)
    st=ParagraphStyle("m",fontName="Sans",fontSize=8.8,leading=11,textColor=MUTED)
    p=Paragraph(lab,st);_,hh=p.wrap(rw-28,40);p.drawOn(c,rx+16,yt(my+72)+10)
    my+=84

# таблица-пример
ty=470
eyebrow(M,ty,"Пример структуры проекта")
rows=[("Площадь объекта","≈ 650 м²"),
      ("Назначение","24 квартиры под долгосрочную аренду"),
      ("Стадия","выкуп → реставрация → аренда"),
      ("Источник дохода инвестора","арендный поток + рост стоимости актива"),
      ("Форма участия","фиксируется договором по выбранному объекту")]
ry=ty+22
for i,(k,v) in enumerate(rows):
    c.setFont("Sans",10); c.setFillColor(MUTED); c.drawString(M,yt(ry+12),k)
    c.setFont("Sans-B",10.5); c.setFillColor(INK); c.drawRightString(W-M,yt(ry+12),v)
    rule(M,ry+22,W-2*M,BORDER,0.7); ry+=34
# дисклеймер
c.setFillColor(HexColor("#F0E7D4")); c.rect(M,yt(ry+58),W-2*M,46,fill=1,stroke=0)
st=ParagraphStyle("d",fontName="Sans",fontSize=8.4,leading=12,textColor=HexColor("#6b5a36"))
p=Paragraph("Цифры приведены как ориентир и являются прогнозом, а не публичной офертой "
            "или гарантией доходности. Точные параметры определяются по каждому объекту "
            "и фиксируются договором. Инвестиции связаны с риском.",st)
_,hh=p.wrap(W-2*M-28,60); p.drawOn(c,M+14,yt(ry+58)+ (46-hh)/2)
footer(5); c.showPage()

# ════════════════════════════ СТР. 6-7 — ОБЪЕКТЫ ═════════════════════════
cases=[
 ("mr-justs.jpg","Калининградская обл. · Зеленоградск","Mr. Just’s Hotel","ул. Пограничная, 1",
  "Приспособление памятника «Здание отеля Восточная Пруссия» (1906 г.) под современный отель. Завершённый проект полного цикла.",
  [("1906","год постройки"),("Отель","назначение"),("Реализован","статус")]),
 ("tambov-aseev.jpg","Тамбов","Комплекс доходных домов Асеева","ул. М. Горького, 49 / 49А / 49В",
  "Объект культурного наследия — ансамбль из трёх исторических зданий. Приспособление под квартиры для долгосрочной аренды.",
  [("1 310,7 м²","площадь"),("38","квартир"),("ОКН","статус")]),
 ("tula.jpg","Тула","Дом Д. Ф. Богородицкой","ул. Пирогова, 24",
  "Объект культурного наследия XIX века с торговым залом. Приспособление под современное использование, аренда 49 лет.",
  [("343,1 м²","площадь"),("9","квартир"),("ОКН","статус")]),
 ("spb.jpg","Санкт-Петербург","Историческое здание","Лесной проспект, 37, лит. Л",
  "Объект культурного наследия регионального значения в долгосрочной аренде на 49 лет. Приспособление под арендные квартиры.",
  [("654,1 м²","площадь"),("24","квартиры"),("Аренда 49 лет","право")]),
 ("svetlogorsk.jpg","Калининградская обл. · Светлогорск","Новый доходный дом","ул. Хуторская, 1",
  "Строительство нового четырёхэтажного дома на собственном участке: квартиры под аренду и подземный паркинг.",
  [("1 765,3 м²","площадь"),("32","квартиры"),("Стройка","статус")]),
 ("petergof.jpg","Санкт-Петербург · Петергоф","Новый доходный дом","ул. Суворовская, 3, корп. 8",
  "Строительство нового четырёхэтажного жилого здания на собственном земельном участке под долгосрочную аренду.",
  [("2 728,4 м²","площадь"),("44","квартиры"),("Стройка","статус")]),
]
def cases_page(items, pageno, first=False):
    bg()
    if first:
        eyebrow(M,70,"Объекты компании")
        title(M,100,"Реализованные и текущие проекты")
        rule(M,120,46,GOLD,2)
        topstart=150
    else:
        eyebrow(M,70,"Объекты компании")
        title(M,98,"Портфель проектов",size=20)
        topstart=128
    ch=200; gap=22
    for i,(img,city,name,addr,desc,mets) in enumerate(items):
        top=topstart+i*(ch+gap)
        iw=240;
        img_box(f"{A}/{img}", M, top, iw, ch-0, ratio=iw/(ch))
        tx=M+iw+26; tw=W-M-tx
        eyebrow(tx,top+4,city)
        c.setFont("Serif-B",17); c.setFillColor(INK); c.drawString(tx,yt(top+30),name)
        c.setFont("Sans",9.5); c.setFillColor(MUTED); c.drawString(tx,yt(top+47),addr)
        st=ParagraphStyle("c",fontName="Sans",fontSize=9.6,leading=14.5,textColor=DARKMID)
        p=Paragraph(desc,st); _,hh=p.wrap(tw,120); p.drawOn(c,tx,yt(top+64)-hh)
        # метрики
        myy=top+ch-34
        mw=tw/3
        for j,(num,lab) in enumerate(mets):
            mx=tx+j*mw
            c.setFont("Serif-B",15); c.setFillColor(GOLD); c.drawString(mx,yt(myy),num)
            c.setFont("Sans",8); c.setFillColor(MUTED); c.drawString(mx,yt(myy+13),lab)
        if j is not None and i<len(items)-1:
            rule(M,top+ch+gap/2, W-2*M, BORDER,0.6)
    footer(pageno); c.showPage()

cases_page(cases[:3], 6, first=True)
cases_page(cases[3:], 7)

# ════════════════════════════ СТР. 8 — ГЕОГРАФИЯ ═════════════════════════
bg()
eyebrow(M,70,"География портфеля")
title(M,100,"Проекты в городах с устойчивым спросом")
rule(M,120,46,GOLD,2)
para("Мы выбираем города с населением от 350 тысяч человек, развитым потенциалом и "
     "удобной логистикой. С 2023 года компания участвовала более чем в 20 аукционах.",
     M,146,W-2*M,leading=16,color=DARKMID)
c.drawImage(ImageReader(f"{TMP}/areas.png"),M,yt(200+250),300,250,mask='auto')
# список регионов
rx=M+330;
eyebrow(rx,196,"Реализованные проекты")
regions=[("Москва","Кузнецкий мост · Бауманская · Трифоновская · Волгоградский пр-т"),
         ("Московская обл.","Коломна · Долгопрудный · Реутов · Видное · Мытищи · Домодедово"),
         ("Калининградская обл.","Зеленоградск · Светлогорск"),
         ("Другие","Сочи · Тамбов · Тула · Санкт-Петербург · Петергоф")]
yy=216
for t,d in regions:
    c.setFont("Serif-B",11.5); c.setFillColor(GOLD); c.drawString(rx,yt(yy),t)
    st=ParagraphStyle("r",fontName="Sans",fontSize=9,leading=13,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(W-M-rx,90); p.drawOn(c,rx,yt(yy+15)-hh)
    yy+=15+hh+12
para("За время работы приобретены 5 объектов культурного наследия и жилой дом; "
     "последний реализованный проект — отель Mr. Just’s Hotel в Зеленоградске.",
     M,480,W-2*M,leading=16,color=MUTED,size=9.5)
footer(8); c.showPage()

# ════════════════════════════ СТР. 9 — УСЛОВИЯ ═══════════════════════════
bg()
eyebrow(M,70,"Условия участия")
title(M,100,"Как инвестор входит в проект")
rule(M,120,46,GOLD,2)
steps=[("Знакомство","Высылаем презентацию и материалы, обсуждаем модель и отвечаем на вопросы. Без обязательств."),
       ("Выбор объекта","Вы знакомитесь с конкретными зданиями, их документами и экономикой и выбираете понятный вам проект."),
       ("Договор","Условия участия и распределения дохода фиксируются документально до вложения средств."),
       ("Доход и отчётность","После запуска объекта вы получаете доход от аренды и регулярную отчётность по проекту.")]
sy=165
for i,(t,d) in enumerate(steps):
    yy=sy+i*92
    c.setFillColor(DARK); c.circle(M+22,yt(yy+10),22,fill=1,stroke=0)
    c.setFont("Serif-B",16); c.setFillColor(GOLD); c.drawCentredString(M+22,yt(yy+16),str(i+1))
    c.setFont("Serif-B",15); c.setFillColor(INK); c.drawString(M+62,yt(yy+6),t)
    st=ParagraphStyle("s",fontName="Sans",fontSize=10,leading=15,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(W-2*M-62,90); p.drawOn(c,M+62,yt(yy+24)-hh)
    if i<3: rule(M+62,yy+70,W-M-(M+62),BORDER,0.6)
footer(9); c.showPage()

# ════════════════════════════ СТР. 10 — ГАРАНТИИ ═════════════════════════
bg()
eyebrow(M,70,"Почему нам доверяют")
title(M,100,"Прозрачность на каждом этапе")
rule(M,120,46,GOLD,2)
items=[("Реальные активы","Конкретные здания в собственности или долгосрочной аренде — с адресом и документами."),
       ("Юридическая чистота","Проверка истории объекта и документов; отношения закреплены договором."),
       ("Объекты культурного наследия","Дефицитный и устойчивый в цене продукт, востребованный на рынке."),
       ("Регулярная отчётность","Понятные отчёты по стадиям проекта и арендным поступлениям."),
       ("Полный цикл","Все этапы под единым контролем группы — без зависимости от подрядчиков."),
       ("Долгосрочные отношения","Репутация важнее одной сделки: мы заинтересованы в возврате инвесторов.")]
cw=(W-2*M-30)/2; cardh=98; gy=160
for i,(t,d) in enumerate(items):
    col=i%2; row=i//2
    x=M+col*(cw+30); top=gy+row*(cardh+16)
    c.setFillColor(CREAM); c.setStrokeColor(BORDER); c.setLineWidth(1)
    c.rect(x,yt(top+cardh),cw,cardh,fill=1,stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2.5); c.line(x,yt(top),x,yt(top+cardh))
    c.setFont("Serif-B",13.5); c.setFillColor(INK); c.drawString(x+20,yt(top+26),t)
for i,(t,d) in enumerate(items):
    col=i%2; row=i//2
    x=M+col*(cw+30); top=gy+row*(cardh+16)
    st=ParagraphStyle("g",fontName="Sans",fontSize=9.4,leading=14,textColor=DARKMID)
    p=Paragraph(d,st); _,hh=p.wrap(cw-36,90); p.drawOn(c,x+20,yt(top+40)-hh)
footer(10); c.showPage()

# ════════════════════════════ СТР. 11 — КОНТАКТЫ ═════════════════════════
bg(dark=True)
c.setStrokeColor(GOLD); c.setLineWidth(1); c.rect(28,28,W-56,H-56,fill=0,stroke=1)
logo=ImageReader(f"{A}/logo.png"); lw=150; lh=lw*(1480/1065)
c.drawImage(logo,(W-lw)/2,H-120-lh,lw,lh,mask='auto')
c.setFillColor(CREAM); c.setFont("Serif-B",28)
c.drawCentredString(W/2,400,"Познакомьтесь с объектами лично")
st=ParagraphStyle("c",fontName="Sans",fontSize=11,leading=17,textColor=HexColor("#CFC8BC"),alignment=1)
p=Paragraph("Расскажем о текущих проектах, покажем документы и экономику и ответим "
            "на ваши вопросы. Первый шаг — без обязательств.",st)
_,hh=p.wrap(360,120); p.drawOn(c,(W-360)/2,374-hh)
# контакты
c.setStrokeColor(GOLD); c.setLineWidth(1); c.line(W/2-30,322,W/2+30,322)
tracked(W/2, H-300, "КОНТАКТЫ", "Sans-B", 9, GOLD, 2, center=True)
c.setFont("Serif",18); c.setFillColor(CREAM)
c.drawCentredString(W/2,268,"info@montrecapital.ru")
c.drawCentredString(W/2,240,"+7 (926) 531-55-30")
c.setFont("Sans",10); c.setFillColor(HexColor("#9a9286"))
c.drawCentredString(W/2,214,"montrecapital.ru")
# дисклеймер
st=ParagraphStyle("d",fontName="Sans",fontSize=7.6,leading=11,textColor=HexColor("#6f685c"),alignment=1)
p=Paragraph("Материал носит ознакомительный характер и не является публичной офертой "
            "или индивидуальной инвестиционной рекомендацией. Инвестиции связаны с риском. "
            "Условия участия по каждому объекту определяются договором. © 2026 АО «Монтре».",st)
_,hh=p.wrap(W-140,80); p.drawOn(c,70,70)
c.showPage()

c.save()
print("PDF:", OUT, os.path.getsize(OUT),"bytes")
