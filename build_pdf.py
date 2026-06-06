#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Монтре Кэпитал — информационный бюллетень для инвесторов (светлый дизайн)."""
import os
import build_charts  # регенерирует графики в /tmp/deck
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from PIL import Image

A="/home/user/sochi-photographer/assets"; TMP="/tmp/deck"
OUT=f"{A}/montre-investor-deck.pdf"
W,H=A4
LF="/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("Serif",LF+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B",LF+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans",LF+"LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans-B",LF+"LiberationSans-Bold.ttf"))

# ── светлая гамма ──
PAPER=HexColor("#F7F3EC"); CARD=HexColor("#FCFAF5"); TINT=HexColor("#EFE6D5")
INK=HexColor("#24211C"); BODY=HexColor("#423B31"); GOLD=HexColor("#B0863B")
GOLDF=HexColor("#CBA461"); MUTED=HexColor("#8C8475"); LINE=HexColor("#E2D8C6")
M=54
TOTAL=9
c=canvas.Canvas(OUT,pagesize=A4)
def yt(t): return H-t
def bg(): c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
def rule(x,top,w,col=GOLD,lw=1):
    c.setStrokeColor(col); c.setLineWidth(lw); c.line(x,yt(top),x+w,yt(top))
def tracked(x,top,text,font,size,color,tr,center=False,right=False):
    c.setFont(font,size); c.setFillColor(color)
    ws=[pdfmetrics.stringWidth(ch,font,size) for ch in text]
    tot=sum(ws)+tr*max(0,len(text)-1)
    cx=x-tot/2 if center else (x-tot if right else x); yy=yt(top)
    for ch,w in zip(text,ws): c.drawString(cx,yy,ch); cx+=w+tr
def title(x,top,text,size=24,color=INK,font="Serif-B"):
    c.setFont(font,size); c.setFillColor(color); c.drawString(x,yt(top),text)
def para(text,x,top,w,size=10.5,leading=16,color=BODY,font="Sans",align=TA_JUSTIFY,space=0):
    st=ParagraphStyle("s",fontName=font,fontSize=size,leading=leading,textColor=color,
                      alignment=align,spaceAfter=space)
    p=Paragraph(text,st); _,h=p.wrap(w,2000); p.drawOn(c,x,yt(top)-h); return top+h
def eyebrow(x,top,text,color=GOLD): tracked(x,top,text.upper(),"Sans-B",8.5,color,2.4)
def section(kicker,headline,top=66,hsize=25):
    eyebrow(M,top,kicker)
    size=hsize
    while size>16 and pdfmetrics.stringWidth(headline,"Serif-B",size)>(W-2*M):
        size-=1
    title(M,top+30,headline,size=size); rule(M,top+48,44,GOLD,2)
    return top+78
def footer(n):
    rule(M,804,W-2*M,LINE,0.8); c.setFont("Sans",7.5); c.setFillColor(MUTED)
    c.drawString(M,yt(816),"Монтре Кэпитал · Бюллетень для инвесторов")
    c.setFillColor(GOLD); c.drawCentredString(W/2,yt(816),"montrecapital.ru")
    c.setFillColor(MUTED); c.drawRightString(W-M,yt(816),f"{n} / {TOTAL}")
def crop_cover(src,ratio,key):
    im=Image.open(src).convert("RGB"); w,h=im.size
    if w/h>ratio:
        nw=int(h*ratio); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
    else:
        nh=int(w/ratio); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
    out=f"{TMP}/c_{key}.jpg"; im.save(out,quality=88); return out
def img_box(src,x,top,w,h,key):
    p=crop_cover(src,w/h,key); c.drawImage(p,x,yt(top)-h,w,h)

# ═══════════════════════ 1 · ОБЛОЖКА / МАСТХЕД ═══════════════════════
bg()
rule(M,46,W-2*M,INK,1.4)
ink=ImageReader(f"{A}/logo-ink.png"); lw=120; lh=lw*(1324/996)
# в мастхеде — компактная надпись справа, лого-марка слева не нужна: используем текст-марку
c.drawImage(ink,M,yt(96)-0,86,86*(1324/996)*0.0+86,mask='auto') if False else None
tracked(M,70,"МОНТРЕ КЭПИТАЛ","Serif-B",15,INK,1.2)
tracked(W-M,66,"БЮЛЛЕТЕНЬ ДЛЯ ИНВЕСТОРОВ","Sans-B",8,GOLD,1.6,right=True)
tracked(W-M,78,"ВЫПУСК № 1 · 2026","Sans",8,MUTED,1.4,right=True)
rule(M,86,W-2*M,INK,2); rule(M,90,W-2*M,GOLD,0.8)
# лид
eyebrow(M,128,"Доходная недвижимость")
c.setFont("Serif-B",30); c.setFillColor(INK)
c.drawString(M,yt(166),"Как старые здания становятся")
c.drawString(M,yt(200),"источником стабильного дохода")
para("Модель доходных домов известна больше века: здание приобретают, "
     "приводят в порядок и сдают в аренду. Разбираемся, почему сегодня это снова "
     "один из самых понятных способов вложить средства в реальный актив — и как "
     "компания «Монтре Кэпитал» сделала эту модель повторяемой в разных городах России.",
     M,224,W-2*M,size=11.5,leading=18,color=BODY)
# изображение-баннер
img_box(f"{A}/tambov-aseev.jpg",M,300,W-2*M,250,"hero")
c.setFont("Sans",8); c.setFillColor(MUTED)
c.drawString(M,yt(566),"Комплекс доходных домов М. В. Асеева, Тамбов — один из объектов компании.")
# содержание выпуска
ry=600
rule(M,ry,W-2*M,LINE,0.8)
tracked(M,ry+20,"В ЭТОМ ВЫПУСКЕ","Sans-B",8.5,GOLD,2)
items=["История модели","Экономика и доходность","Объекты в разных городах","Как стать участником"]
cw=(W-2*M)/4
for i,t in enumerate(items):
    x=M+i*cw
    c.setFont("Serif-B",11); c.setFillColor(INK); c.drawString(x,yt(ry+44),f"0{i+1}")
    st=ParagraphStyle("t",fontName="Sans",fontSize=9,leading=12,textColor=BODY)
    p=Paragraph(t,st); _,hh=p.wrap(cw-16,40); p.drawOn(c,x+22,yt(ry+48)-hh+6)
footer(1); c.showPage()

# ═══════════════════════ 2 · ИСТОРИЯ ═══════════════════════
bg()
y=section("История компании","Путь к проверенной модели")
y=para("Компания, которая сегодня работает под брендом «Монтре Кэпитал», "
 "была основана ещё в 2006 году, но долгое время оставалась без активной "
 "деятельности. Поворот произошёл в 2023 году: команда поставила задачу — "
 "построить бизнес на реальных активах, а не на обещаниях.",
 M,y+8,W-2*M,leading=17)
y=para("Выбор пал на доходные дома. Но компания подошла к модели системно. Были "
 "сформулированы строгие критерии отбора городов: население от 350 тысяч человек, "
 "устойчивая демография, развитая промышленность и удобная логистика — не более "
 "двух часов перелёта до Москвы без пересадок.",
 M,y+10,W-2*M,leading=17)
y=para("С этими критериями компания вышла на муниципальные аукционы. За короткое "
 "время — участие более чем в 20 аукционах в 13 городах: от Калининграда и "
 "Санкт-Петербурга до Тамбова, Тулы, Екатеринбурга и Барнаула. Результат — шесть "
 "приобретённых объектов, пять из которых имеют статус объектов культурного наследия.",
 M,y+10,W-2*M,leading=17)
# цитата
qy=y+28
c.setFillColor(TINT); c.rect(M,yt(qy+70),W-2*M,70,fill=1,stroke=0)
c.setFillColor(GOLD); c.rect(M,yt(qy+70),4,70,fill=1,stroke=0)
st=ParagraphStyle("q",fontName="Serif-B",fontSize=15,leading=21,textColor=INK)
p=Paragraph("«Мы искали не быструю прибыль, а модель, которая одинаково надёжно "
            "работает в любом городе».",st)
_,hh=p.wrap(W-2*M-50,80); p.drawOn(c,M+26,yt(qy+70)+(70-hh)/2)
# таймлайн
ty=qy+120
tracked(M,ty,"ХРОНОЛОГИЯ","Sans-B",8.5,GOLD,2)
tl=[("2006","Основание компании"),("2023","Старт программы доходных домов"),
    ("2024","Формирование группы"),("Сегодня","6 объектов · 7 700 м² в работе")]
cwn=(W-2*M)/4; node_y=ty+44
cxs=[M+cwn*(i+0.5) for i in range(4)]
rule(cxs[0],node_y,cxs[3]-cxs[0],LINE,1.2)
for i,(yr,desc) in enumerate(tl):
    x=cxs[i]
    c.setFillColor(GOLD); c.circle(x,yt(node_y),5,fill=1,stroke=0)
    c.setFont("Serif-B",15); c.setFillColor(INK); c.drawCentredString(x,yt(node_y-16),yr)
    st=ParagraphStyle("d",fontName="Sans",fontSize=8.6,leading=11.5,textColor=BODY,alignment=TA_CENTER)
    tw=cwn-16; p=Paragraph(desc,st); _,hh=p.wrap(tw,50); p.drawOn(c,x-tw/2,yt(node_y+18)-hh)
# итог
para("Так выкристаллизовалась модель, которую можно повторять: одни и те же "
 "принципы работают в разных городах и на разных типах зданий. Сегодня проекты "
 "объединены в группу, а накопленный опыт позволяет приглашать в них частных инвесторов.",
 M,ty+120,W-2*M,leading=17,color=BODY)
footer(2); c.showPage()

# ═══════════════════════ 3 · МОДЕЛЬ ═══════════════════════
bg()
y=section("Бизнес-модель","Идея проста")
y=para("В основе — проверенная веками идея: превратить недооценённое здание в "
 "источник арендного дохода. Мы разложили её на четыре повторяемых шага.",
 M,y+8,W-2*M,leading=17)
steps=[("01","Находим объект","Здание в сильной локации, которое можно купить ниже его потенциальной стоимости — часто это памятник архитектуры."),
       ("02","Приводим в порядок","Реставрация и качественный ремонт. Объект культурного наследия приспосабливается к современному использованию."),
       ("03","Сдаём в аренду","Готовые квартиры заселяются арендаторами. Здание начинает приносить регулярный доход."),
       ("04","Получаем доход","Арендный поток плюс постепенный рост стоимости самого актива — два источника дохода одновременно.")]
top=y+34
for i,(n,t,d) in enumerate(steps):
    row=i//2; col=i%2
    x=M+col*((W-2*M)/2+14); yy=top+row*120
    c.setFont("Serif-B",30); c.setFillColor(GOLDF); c.drawString(x,yt(yy+8),n)
    c.setFont("Serif-B",14); c.setFillColor(INK); c.drawString(x+54,yt(yy),t)
    st=ParagraphStyle("s",fontName="Sans",fontSize=9.6,leading=14.5,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap((W-2*M)/2-70,90); p.drawOn(c,x+54,yt(yy+16)-hh)
# вывод
by=top+250
c.setFillColor(TINT); c.rect(M,yt(by+58),W-2*M,58,fill=1,stroke=0)
c.setFillColor(GOLD); c.rect(M,yt(by+58),4,58,fill=1,stroke=0)
st=ParagraphStyle("x",fontName="Serif-B",fontSize=13,leading=18,textColor=INK)
p=Paragraph("Одни и те же шаги — в Калининграде, Тамбове или Санкт-Петербурге. "
            "Именно повторяемость делает модель надёжной и предсказуемой.",st)
_,hh=p.wrap(W-2*M-50,80); p.drawOn(c,M+26,yt(by+58)+(58-hh)/2)
footer(3); c.showPage()

# ═══════════════════════ 4 · ПОЧЕМУ РАБОТАЕТ ═══════════════════════
bg()
y=section("Анализ рынка","Почему аренда — устойчивый класс активов")
y=para("Спрос на качественную долгосрочную аренду в России растёт не из-за моды, "
 "а под действием структурных причин. Они работают вдолгую — и именно это важно для инвестора.",
 M,y+8,W-2*M,leading=17)
factors=[("Покупка стала дороже","Высокие ставки и ужесточение ипотеки сдвигают спрос от покупки к аренде качественного жилья."),
         ("Люди стали мобильнее","Гибкость аренды всё чаще предпочитают долгосрочным обязательствам при покупке недвижимости."),
         ("Качества не хватает","Рынок профессиональной долгосрочной аренды в российских городах только формируется — спрос опережает предложение.")]
fy=y+34
for i,(t,d) in enumerate(factors):
    yy=fy+i*80
    c.setFont("Serif-B",20); c.setFillColor(GOLDF); c.drawString(M,yt(yy),f"0{i+1}")
    c.setFont("Serif-B",14); c.setFillColor(INK); c.drawString(M+44,yt(yy),t)
    st=ParagraphStyle("f",fontName="Sans",fontSize=10,leading=15,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap(W-2*M-44,80); p.drawOn(c,M+44,yt(yy+18)-hh)
# акцент
ay=fy+255
c.setFillColor(INK); c.rect(M,yt(ay+86),W-2*M,86,fill=1,stroke=0)
c.setFillColor(GOLDF); c.rect(M,yt(ay+86),4,86,fill=1,stroke=0)
st=ParagraphStyle("a",fontName="Serif-B",fontSize=16,leading=22,textColor=PAPER)
p=Paragraph("Доходный дом — это доход от реального актива, защищённого от инфляции "
            "самими стенами и землёй. Не котировки на экране, а здание, которое можно увидеть.",st)
_,hh=p.wrap(W-2*M-50,100); p.drawOn(c,M+26,yt(ay+86)+(86-hh)/2)
footer(4); c.showPage()

# ═══════════════════════ 5 · ЭКОНОМИКА ═══════════════════════
bg()
y=section("Экономика","Что формирует доход инвестора")
para("Доход складывается из двух источников: арендных платежей и постепенного роста "
     "стоимости отреставрированного здания. Ниже — ориентировочная модель окупаемости.",
     M,y+8,W-2*M,leading=17)
c.drawImage(ImageReader(f"{TMP}/payback.png"),M,yt(y+44+255),300,255,mask='auto')
rx=M+320; rw=W-M-rx; my=y+42
for num,lab in [("10–14%","доходность от аренды в год (прогноз)"),
                ("8–9 лет","ориентировочная окупаемость"),
                ("2 источника","аренда + рост стоимости актива")]:
    c.setFillColor(CARD); c.setStrokeColor(LINE); c.setLineWidth(1)
    c.rect(rx,yt(my+74),rw,74,fill=1,stroke=1)
    c.setStrokeColor(GOLD); c.setLineWidth(3); c.line(rx,yt(my),rx,yt(my+74))
    c.setFont("Serif-B",21); c.setFillColor(INK); c.drawString(rx+16,yt(my+34),num)
    st=ParagraphStyle("m",fontName="Sans",fontSize=8.8,leading=11.5,textColor=MUTED)
    p=Paragraph(lab,st);_,hh=p.wrap(rw-28,40);p.drawOn(c,rx+16,yt(my+74)+10); my+=86
ty=y+330
tracked(M,ty,"ПРИМЕР СТРУКТУРЫ ПРОЕКТА","Sans-B",8.5,GOLD,2)
rows=[("Площадь объекта","≈ 650 м²"),("Назначение","24 квартиры под аренду"),
      ("Стадия","выкуп → реставрация → аренда"),
      ("Доход инвестора","арендный поток + рост стоимости актива"),
      ("Форма участия","фиксируется договором по объекту")]
ry=ty+22
for k,v in rows:
    c.setFont("Sans",10); c.setFillColor(MUTED); c.drawString(M,yt(ry+12),k)
    c.setFont("Sans-B",10.5); c.setFillColor(INK); c.drawRightString(W-M,yt(ry+12),v)
    rule(M,ry+22,W-2*M,LINE,0.7); ry+=33
c.setFillColor(TINT); c.rect(M,yt(ry+50),W-2*M,42,fill=1,stroke=0)
st=ParagraphStyle("d",fontName="Sans",fontSize=8.3,leading=12,textColor=HexColor("#6E5C36"))
p=Paragraph("Цифры — ориентир и прогноз, а не публичная оферта или гарантия доходности. "
            "Параметры зависят от объекта и фиксируются договором. Инвестиции связаны с риском.",st)
_,hh=p.wrap(W-2*M-28,60); p.drawOn(c,M+14,yt(ry+50)+(42-hh)/2)
footer(5); c.showPage()

# ═══════════════════════ 6 · ОБЪЕКТЫ ═══════════════════════
cases=[("mr-justs.jpg","Зеленоградск","Mr. Just’s Hotel","ул. Пограничная, 1",
        "Памятник «Здание отеля Восточная Пруссия» 1906 года приспособлен под современный отель. Завершённый проект полного цикла.",
        [("1906","год постройки"),("Отель","назначение"),("Реализован","статус")]),
 ("tambov-aseev.jpg","Тамбов","Комплекс домов Асеева","ул. М. Горького, 49",
        "Объект культурного наследия — ансамбль из трёх исторических зданий. Создаются квартиры для долгосрочной аренды.",
        [("1 311 м²","площадь"),("38","квартир"),("ОКН","статус")]),
 ("tula.jpg","Тула","Дом Богородицкой","ул. Пирогова, 24",
        "Памятник XIX века с торговым залом. Приспособление под современное использование, долгосрочная аренда на 49 лет.",
        [("343 м²","площадь"),("9","квартир"),("ОКН","статус")])]
def cases_page(items,pageno,kicker,headline):
    bg(); section(kicker,headline)
    top=150; ch=185; gap=24
    for i,(img,city,name,addr,desc,mets) in enumerate(items):
        t=top+i*(ch+gap); iw=232
        img_box(f"{A}/{img}",M,t,iw,ch,f"case{pageno}_{i}")
        tx=M+iw+26; tw=W-M-tx
        eyebrow(tx,t+6,city); c.setFont("Serif-B",17); c.setFillColor(INK)
        c.drawString(tx,t and yt(t+32),name)
        c.setFont("Sans",9.5); c.setFillColor(MUTED); c.drawString(tx,yt(t+49),addr)
        st=ParagraphStyle("c",fontName="Sans",fontSize=9.8,leading=14.5,textColor=BODY)
        p=Paragraph(desc,st); _,hh=p.wrap(tw,120); p.drawOn(c,tx,yt(t+66)-hh)
        myy=t+ch-30; mw=tw/3
        for j,(num,lab) in enumerate(mets):
            mx=tx+j*mw
            c.setFont("Serif-B",15); c.setFillColor(GOLD); c.drawString(mx,yt(myy),num)
            c.setFont("Sans",8); c.setFillColor(MUTED); c.drawString(mx,yt(myy+13),lab)
        if i<len(items)-1: rule(M,t+ch+gap/2,W-2*M,LINE,0.6)
    footer(pageno); c.showPage()
cases_page(cases,6,"Портфель","Проверено в разных городах")

# ═══════════════════════ 7 · ГЕОГРАФИЯ ═══════════════════════
bg()
y=section("География","От Калининграда до Тамбова")
para("Компания выбирает города с устойчивым спросом и развитым потенциалом. "
     "Реализованные и текущие проекты охватывают всю европейскую часть России.",
     M,y+8,W-2*M,leading=17)
c.drawImage(ImageReader(f"{TMP}/areas.png"),M,yt(y+44+250),300,250,mask='auto')
rx=M+330
eyebrow(rx,y+40,"Реализованные проекты")
regions=[("Москва","Кузнецкий мост · Бауманская · Трифоновская · Волгоградский пр-т"),
         ("Московская обл.","Коломна · Долгопрудный · Реутов · Видное · Мытищи · Домодедово"),
         ("Калининградская обл.","Зеленоградск · Светлогорск"),
         ("Другие города","Сочи · Тамбов · Тула · Санкт-Петербург · Петергоф")]
yy=y+62
for t,d in regions:
    c.setFont("Serif-B",12); c.setFillColor(INK); c.drawString(rx,yt(yy),t)
    st=ParagraphStyle("r",fontName="Sans",fontSize=9,leading=13,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap(W-M-rx,90); p.drawOn(c,rx,yt(yy+15)-hh); yy+=15+hh+12
para("За время работы приобретены пять объектов культурного наследия и жилой дом. "
     "Текущие проекты — в Зеленоградске, Светлогорске, Санкт-Петербурге, Петергофе, "
     "Тамбове и Туле: новое строительство и реставрация под долгосрочную аренду.",
     M,y+330,W-2*M,leading=17,color=BODY)
footer(7); c.showPage()

# ═══════════════════════ 8 · ПРОЗРАЧНОСТЬ И УЧАСТИЕ ═══════════════════════
bg()
y=section("Прозрачность и участие","Как защищены ваши вложения")
trust=[("Реальные активы","Конкретные здания в собственности или аренде — с адресом и документами."),
       ("Объекты культурного наследия","Дефицитный, устойчивый в цене и востребованный продукт."),
       ("Юридическая чистота","Проверка истории объекта; отношения закреплены договором."),
       ("Регулярная отчётность","Понятные отчёты по стадиям проекта и арендным поступлениям.")]
cw=(W-2*M-24)/2; ty=y+10
for i,(t,d) in enumerate(trust):
    col=i%2; rw=i//2; x=M+col*(cw+24); top=ty+rw*84
    c.setFillColor(CARD); c.setStrokeColor(LINE); c.setLineWidth(1)
    c.rect(x,yt(top+70),cw,70,fill=1,stroke=0)
    c.setStrokeColor(GOLD); c.setLineWidth(2.5); c.line(x,yt(top),x,yt(top+70))
    c.setFont("Serif-B",12.5); c.setFillColor(INK); c.drawString(x+18,yt(top+22),t)
    st=ParagraphStyle("g",fontName="Sans",fontSize=9,leading=13,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap(cw-34,70); p.drawOn(c,x+18,yt(top+34)-hh+2)
# шаги участия
sy=ty+200
tracked(M,sy,"КАК СТАТЬ УЧАСТНИКОМ","Sans-B",8.5,GOLD,2)
steps=[("Знакомство","Высылаем материалы и отвечаем на вопросы — без обязательств."),
       ("Выбор объекта","Изучаете конкретные здания, документы и экономику."),
       ("Договор","Условия и распределение дохода фиксируются до вложения средств."),
       ("Доход","Получаете арендный доход и регулярную отчётность.")]
swy=sy+22; scw=(W-2*M-3*16)/4
for i,(t,d) in enumerate(steps):
    x=M+i*(scw+16)
    c.setFillColor(GOLD); c.circle(x+12,yt(swy+8),12,fill=1,stroke=0)
    c.setFont("Serif-B",11); c.setFillColor(PAPER); c.drawCentredString(x+12,yt(swy+12),str(i+1))
    c.setFont("Serif-B",11.5); c.setFillColor(INK); c.drawString(x+30,yt(swy+12),t)
    st=ParagraphStyle("s",fontName="Sans",fontSize=8.8,leading=12.5,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap(scw-4,80); p.drawOn(c,x,yt(swy+34)-hh)
footer(8); c.showPage()

# ═══════════════════════ 9 · ПРЕДЛОЖЕНИЕ + КОНТАКТЫ ═══════════════════════
bg()
eyebrow(M,70,"Предложение")
title(M,102,"Познакомьтесь с объектами первыми",size=24); rule(M,120,44,GOLD,2)
para("Этот бюллетень — приглашение к разговору. Читателям выпуска мы предлагаем "
     "условия, которые обычно доступны только по личному запросу:",
     M,148,W-2*M,leading=17)
# панель предложения
oy=190
offers=[("Бесплатный расчёт доходности","по конкретному объекту, который вам интересен"),
        ("Приоритетный доступ","к новым объектам — до публичного предложения"),
        ("Личный осмотр и встреча","с командой — увидите объект и документы своими глазами"),
        ("Сопровождение сделки","и прозрачная отчётность на всём сроке участия")]
ph=2*86+16
c.setFillColor(TINT); c.rect(M,yt(oy+ph),W-2*M,ph,fill=1,stroke=0)
c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(M,yt(oy+ph),W-2*M,ph,fill=0,stroke=1)
icw=(W-2*M-40)/2
for i,(t,d) in enumerate(offers):
    col=i%2; rw=i//2; x=M+24+col*icw; top=oy+18+rw*86
    c.setFillColor(GOLD); c.saveState(); c.translate(x+5,yt(top+4)); c.rotate(45)
    c.rect(-4,-4,8,8,fill=1,stroke=0); c.restoreState()
    c.setFont("Serif-B",13); c.setFillColor(INK); c.drawString(x+20,yt(top),t)
    st=ParagraphStyle("o",fontName="Sans",fontSize=9.5,leading=13.5,textColor=BODY)
    p=Paragraph(d,st); _,hh=p.wrap(icw-44,60); p.drawOn(c,x+20,yt(top+16)-hh)
# призыв
cy=oy+ph+40
st=ParagraphStyle("c",fontName="Serif-B",fontSize=17,leading=23,textColor=INK,alignment=TA_CENTER)
p=Paragraph("Это ни к чему вас не обязывает. Один разговор — и вы увидите, "
            "как устроен доход на реальных активах.",st)
_,hh=p.wrap(W-2*M-60,80); p.drawOn(c,M+30,yt(cy)-hh)
# контакты
ky=cy+70
rule(W/2-30,ky-14,60,GOLD,1)
tracked(W/2,ky+4,"СВЯЖИТЕСЬ С НАМИ","Sans-B",8.5,GOLD,2,center=True)
c.setFont("Serif-B",19); c.setFillColor(INK)
c.drawCentredString(W/2,yt(ky+34),"info@montrecapital.ru")
c.setFont("Serif",17); c.drawCentredString(W/2,yt(ky+58),"+7 (926) 531-55-30")
c.setFont("Sans",10); c.setFillColor(MUTED); c.drawCentredString(W/2,yt(ky+80),"montrecapital.ru")
# логотип-чернила внизу
ink=ImageReader(f"{A}/logo-ink.png"); lw=104; lh=lw*(1324/996)
c.drawImage(ink,(W-lw)/2,98,lw,lh,mask='auto')
st=ParagraphStyle("dd",fontName="Sans",fontSize=7.4,leading=10.5,textColor=MUTED,alignment=TA_CENTER)
p=Paragraph("Материал носит информационный характер и не является публичной офертой "
            "или индивидуальной инвестиционной рекомендацией. Инвестиции связаны с риском. "
            "Условия по каждому объекту определяются договором. © 2026 Монтре Кэпитал.",st)
_,hh=p.wrap(W-150,60); p.drawOn(c,75,52)
c.showPage()

c.save()
print("PDF:",OUT,os.path.getsize(OUT),"bytes")
