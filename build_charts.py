#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Инвесторская презентация АО «Монтре» — премиальный PDF."""
import os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ASSETS = "/home/user/sochi-photographer/assets"
TMP = "/tmp/deck"; os.makedirs(TMP, exist_ok=True)

# ── гамма ──
CREAM="#F5F0E8"; WW="#FAF8F4"; GOLD="#B8965A"; GOLDL="#D4B07A"
DARK="#1A1714"; DARKMID="#2E2A26"; MUTED="#7A746C"; BORDER="#E4DAC8"

plt.rcParams.update({
    "font.family":"DejaVu Sans","text.color":DARKMID,
    "axes.edgecolor":BORDER,"axes.labelcolor":DARKMID,
    "xtick.color":MUTED,"ytick.color":MUTED,"font.size":11,
})

# ─────────── ГРАФИК A: окупаемость ───────────
def chart_payback():
    yrs=np.arange(0,11); annual=11.5; cum=annual*yrs; invest=100
    fig,ax=plt.subplots(figsize=(6.6,3.5),dpi=200)
    ax.fill_between(yrs,0,cum,color=GOLD,alpha=.18,zorder=1)
    ax.plot(yrs,cum,color=GOLD,lw=2.6,zorder=3,label="Накопленный арендный доход")
    ax.axhline(invest,color=DARKMID,lw=1.6,ls=(0,(5,4)),zorder=2,label="Объём вложений")
    x0=invest/annual
    ax.scatter([x0],[invest],color=DARK,zorder=5,s=42)
    ax.annotate("Окупаемость\n≈ 8–9 лет",(x0,invest),(x0-3.1,invest+24),
                color=DARK,fontsize=11,fontweight="bold",ha="center",
                arrowprops=dict(arrowstyle="-",color=DARKMID,lw=1))
    ax.set_xlim(0,10); ax.set_ylim(0,135)
    ax.set_xlabel("Год эксплуатации"); ax.set_ylabel("% от вложенных средств")
    ax.set_xticks(range(0,11,2))
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.grid(axis="y",color=BORDER,lw=.8,alpha=.7)
    ax.legend(frameon=False,fontsize=9.5,loc="lower right")
    fig.tight_layout(); fig.savefig(f"{TMP}/payback.png",transparent=True); plt.close(fig)

# ─────────── ГРАФИК B: источники дохода (донат) ───────────
def chart_sources():
    fig,ax=plt.subplots(figsize=(3.5,3.5),dpi=200)
    sizes=[70,30]; cols=[GOLD,DARKMID]
    w,_=ax.pie(sizes,colors=cols,startangle=90,counterclock=False,
              wedgeprops=dict(width=0.42,edgecolor=WW,linewidth=2))
    ax.text(0,0.12,"Доход",ha="center",fontsize=11,color=MUTED)
    ax.text(0,-0.18,"инвестора",ha="center",fontsize=11,color=MUTED)
    ax.set(aspect="equal")
    fig.tight_layout(); fig.savefig(f"{TMP}/sources.png",transparent=True); plt.close(fig)

# ─────────── ГРАФИК C: площади по городам ───────────
def chart_areas():
    data=[("Петергоф",2728),("Светлогорск",1765),("Тамбов",1311),
          ("Зеленоградск",895),("Санкт-Петербург",654),("Тула",343)]
    data=data[::-1]; labels=[d[0] for d in data]; vals=[d[1] for d in data]
    fig,ax=plt.subplots(figsize=(6.6,3.4),dpi=200)
    bars=ax.barh(labels,vals,color=GOLD,height=.62)
    bars[-1].set_color(DARKMID)
    for b,v in zip(bars,vals):
        ax.text(v+40,b.get_y()+b.get_height()/2,f"{v:,} м²".replace(","," "),
                va="center",fontsize=9.5,color=DARKMID)
    ax.set_xlim(0,3150)
    for s in ("top","right","bottom"): ax.spines[s].set_visible(False)
    ax.set_xticks([])
    ax.tick_params(axis="y",length=0,labelsize=10.5)
    fig.tight_layout(); fig.savefig(f"{TMP}/areas.png",transparent=True); plt.close(fig)

chart_payback(); chart_sources(); chart_areas()
print("charts done")
