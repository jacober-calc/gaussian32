import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.stats import norm
from scipy.special import erf, erfc
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/g_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)

# 1 P(z) and Q(z)
z=np.linspace(-4,4,600); y=norm.pdf(z); z0=1.0
fig,ax=plt.subplots(figsize=(8.5,4.3))
ax.fill_between(z,y,where=z<=z0,color=BLUE,alpha=.25); ax.fill_between(z,y,where=z>=z0,color=ORANGE,alpha=.35)
ax.plot(z,y,color=INK,lw=2); ax.axvline(z0,color=INK,lw=1,ls="--")
ax.text(-0.25,.15,f"LBL A\nP(1) = {norm.cdf(z0):.6f}",ha="center",fontsize=11,color=BLUE,fontweight="bold")
ax.annotate(f"LBL B\nQ(1) = {norm.sf(z0):.6f}",xy=(1.6,.05),xytext=(1.75,.22),fontsize=11,color=ORANGE,fontweight="bold",arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.text(z0+.05,.405,"z = 1",fontsize=10)
ax.set_xlim(-4,4); ax.set_ylim(0,.44); ax.set_xlabel("Standardized value z"); ax.set_ylabel("Density")
ax.set_title("Lower Tail P(z) and Upper Tail Q(z)",loc="left"); save(fig,"normal_tails")

# 2 erf and erfc with method split
x=np.linspace(-3,3,600)
fig,ax=plt.subplots(figsize=(8.5,4.3))
ax.axvspan(-1.6,1.6,color=BLUE,alpha=.07,lw=0)
ax.plot(x,erf(x),color=BLUE,lw=2.4,label="erf(x)  LBL D"); ax.plot(x,erfc(x),color=ORANGE,lw=2.4,label="erfc(x)  LBL C")
for xv in (-1.6,1.6): ax.axvline(xv,color=GREY,ls=":",lw=1.2)
ax.text(0,1.72,"|x| ≤ 1.6: integrate e^(−v²) directly (LBL Z)",ha="center",fontsize=9.5,color=BLUE)
ax.text(2.3,.45,"|x| > 1.6:\nsubstitution\nintegral (LBL W)",ha="center",fontsize=9.5,color=GREY,va="center")
ax.text(-2.3,.45,"|x| > 1.6:\nsubstitution\nintegral (LBL W)",ha="center",fontsize=9.5,color=GREY,va="center")
for xv in (0.5,2.0):
    ax.plot(xv,erf(xv),"o",color=BLUE,ms=7,zorder=5); ax.plot(xv,erfc(xv),"o",color=ORANGE,ms=7,zorder=5)
ax.annotate(f"erf(0.5) = {erf(.5):.6f}",xy=(.5,erf(.5)),xytext=(-1.45,1.2),fontsize=9.5,color=BLUE,arrowprops=dict(arrowstyle="->",color=BLUE))
ax.annotate(f"erfc(2) = {erfc(2):.6f}",xy=(2,erfc(2)),xytext=(1.0,-.55),fontsize=9.5,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.axhline(0,color=INK,lw=.8); ax.set_xlim(-3,3); ax.set_ylim(-1.15,2.05)
ax.set_xlabel("x"); ax.legend(frameon=False,loc="lower right")
ax.set_title("Error Function and Complementary Error Function",loc="left"); save(fig,"erf_erfc")

# 3 Golf range (LBL E)
mu,sd=231,23; xs=np.linspace(mu-4*sd,mu+4*sd,600); ys=norm.pdf(xs,mu,sd); lo,hi=200,260
pr=norm.cdf(hi,mu,sd)-norm.cdf(lo,mu,sd)
fig,ax=plt.subplots(figsize=(8.5,4.3))
ax.fill_between(xs,ys,where=(xs>=lo)&(xs<=hi),color=GREEN,alpha=.3); ax.plot(xs,ys,color=INK,lw=2)
for v in (lo,hi): ax.axvline(v,color=GREEN,lw=1.2,ls="--")
ax.text(mu,norm.pdf(mu,mu,sd)*.45,f"LBL E\n{pr:.6f}",ha="center",fontsize=12,color=GREEN,fontweight="bold")
ax.text(lo-2,norm.pdf(mu,mu,sd)*1.03,"200",ha="right",fontsize=10,color=GREEN); ax.text(hi+2,norm.pdf(mu,mu,sd)*1.03,"260",fontsize=10,color=GREEN)
ax.set_xlim(mu-4*sd,mu+4*sd); ax.set_ylim(0,norm.pdf(mu,mu,sd)*1.12); ax.set_yticks([])
ax.set_xlabel("Driving distance (yards)"); ax.set_title("Range with LBL E: drives between 200 and 260 yards (LBL G: mean 231, SD 23)",loc="left",fontsize=11.5)
save(fig,"golf_range")

# 4 x <-> z scales (LBL M / LBL N)
fig,ax=plt.subplots(figsize=(8.5,2.6)); ax.axis("off"); ax.set_xlim(-3.6,3.6); ax.set_ylim(-1.3,1.5)
ax.plot([-3.3,3.3],[.6,.6],color=INK,lw=1.5); ax.plot([-3.3,3.3],[-.4,-.4],color=INK,lw=1.5)
for k in range(-3,4):
    ax.plot([k,k],[.52,.68],color=INK,lw=1.2); ax.plot([k,k],[-.48,-.32],color=INK,lw=1.2)
    ax.text(k,.85,f"{mu+k*sd:g}",ha="center",fontsize=11); ax.text(k,-.72,(f"{k:+d}" if k else "0").replace("-","−"),ha="center",fontsize=11,color=BLUE)
    ax.annotate("",xy=(k,-.28),xytext=(k,.46),arrowprops=dict(arrowstyle="<->",color=GREY,lw=.8))
ax.text(-3.55,.6,"x (yards)",ha="right",va="center",fontsize=10.5); ax.text(-3.55,-.4,"z",ha="right",va="center",fontsize=10.5,color=BLUE)
ax.text(3.45,.1,"LBL M: z = (x − R) ÷ S\nLBL N: x = z × S + R",fontsize=10,va="center",color=INK)
ax.set_xlim(-4.3,5.6)
ax.text(-4.3,1.38,"Converting Between x and z (R = 231, S = 23)",fontsize=13,fontweight="bold",va="center")
save(fig,"xz_scale")

# 5 At least one (LBL F)
bm,bs=.245,.035; p=norm.sf(.300,bm,bs); n=np.arange(1,41); q=1-(1-p)**n
fig,ax=plt.subplots(figsize=(8.5,4.3))
ax.plot(n,q*100,color=BLUE,lw=2.4,marker="o",ms=3.5)
ax.axhline(50,color=GREY,ls=":",lw=1)
for k,lab in [(9,"9 hitters"),(26,"26-man roster")]:
    v=1-(1-p)**k; ax.plot(k,v*100,"o",color=ORANGE,ms=9,zorder=5)
    ax.annotate(f"{lab}: {v:.4f}",xy=(k,v*100),xytext=(10,-18),textcoords="offset points",fontsize=10,color=ORANGE)
ax.set_xlim(0,41); ax.set_ylim(0,100); ax.set_xlabel("Number of players n"); ax.set_ylabel("P(at least one) (%)")
ax.text(1,92,f"p = Q((0.300 − 0.245) ÷ 0.035) = {p:.6f}",fontsize=10,color=INK)
ax.set_title("LBL F: chance at least one player bats .300 or better (LBL J)",loc="left",fontsize=12); save(fig,"at_least_one")

# 6 Keyboard map
fig,ax=plt.subplots(figsize=(9,2.9)); ax.axis("off"); ax.set_xlim(0,6.2); ax.set_ylim(0,2.5)
top=[("A","P(z)"),("B","Q(z)"),("C","erfc(x)"),("D","erf(x)"),("E","Range"),("F","At least one")]
second=[("G","Golf"),("H","Golf"),("I","Golf"),("J","Batting"),("K","Batting"),("L","Batting")]
for row,(items,y,col) in enumerate([(top,1.32,BLUE),(second,.12,GREEN)]):
    for i,(k,t) in enumerate(items):
        ax.add_patch(FancyBboxPatch((i*1.02+.12,y),.9,.92,boxstyle="round,pad=0,rounding_size=.08",fc="white",ec=col,lw=1.8))
        ax.text(i*1.02+.57,y+.62,f"LBL {k}",ha="center",va="center",fontsize=12,fontweight="bold",color=col)
        ax.text(i*1.02+.57,y+.28,t,ha="center",va="center",fontsize=10)
ax.text(.12,2.43,"Program Map: top row computes, second row loads mean and SD into R and S",fontsize=12,fontweight="bold",va="center")
save(fig,"program_map")
