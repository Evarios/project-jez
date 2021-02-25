from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from random import uniform


app = Flask(__name__)

@app.route("/home", methods=["POST","GET"])
def home():
    if request.method=="POST":
        eta=0.95   #sprawnosc
        R=1     #opor lampy
        cv=1005 #powietrza
        a=float(request.form["glebokosc"])/100
        b=float(request.form["szerokosc"])/100
        h=float(request.form["wysokosc"])/100
        V=a*b*h
        ro=1.21 #gestosc
        Tzad=float(request.form["temperatura_dzien"]) #zadana
        Tzew=float(request.form["temperatura_otoczenia"]) #otoczenia/początkowa
        Tnoc=float(request.form["temperatura_noc"]) #temp w nocy
        #1 - boki, 2- front
        lambda1=float(request.form["material_scianek"])  #przenikalność cieplna materiału 
        lambda2=float(request.form["material_frontu"])
        d1=float(request.form["grubosc_scianek"])/100 #grubość ścianki
        d2=float(request.form["grubosc_frontu"])/100
        S1=a*h+2*b*h+a*b
        S2=a*h
        strata=S1*lambda1/d1+S2*lambda2/d2
        pom=cv*V*ro
        tp=1
        kp=0.008
        Ti=0.25
        Td=0.05
        N=172200
        if(Tzew >= Tzad):
            Tzad = Tzew
        if(Tzew >= Tnoc):
            Tnoc = Tzew
        T = Tzew
        e = [Tzad-Tzew]
        temp = Tzad-T
        Qdmax = 24
        umax = 20
        akier = (Qdmax/umax)/100
        x = [0]
        y = [Tzew]
        k = [1/3600,43200/3600,43201/3600,86399/3600,86400/3600,129600/3600,129601/3600,172200/3600]
        l = [Tzad]
        n = 1
        esum = e[0]
        while (n<=N):
            if (n%36 == 0):
                Tzew += round(uniform(-0.02,0.02),4)
            if (n%86400>43200):
                temp = Tnoc - T
            else:
                temp = Tzad - T
            e.append(temp)
            esum += e[n]
            u=kp*(e[-2]+(tp/Ti)*esum+(Td/tp)*(e[-1]-e[-2]))
            #if (u > umax):
            #    u = umax
            Qd=akier*u
            if (Qd > 230):
                Qd = 230
            #print(e[n],u, "\n")
            T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(pom)+ T
            #print(n,T)
            if (T>30): #T>tmax
                T=30
                #e[-1]=Tzad-T
            if (Tzew>30):
                T=Tzew
            x.append((n*tp)/3600)
            y.append(T)
            if(n==43200 or n==86400 or n == 129600):
                l.append(Tzad)
            elif(n == 43201 or n == 86399 or n == 129601 or n == 172200):
                l.append(Tnoc)
            n+=1
        p=figure(plot_width=723,plot_height=400,tools="pan,wheel_zoom,reset",x_axis_label="Czas [h]",y_axis_label="Temperatura [st. C]", toolbar_location="right")
        p.border_fill_color='#fac096'
        p.line(x,y, legend_label = "Obecna temperatura")
        p.line(k, l, line_color='#FF0000', legend_label = "Temperatura zadana")
        p.legend.location = "bottom_right"
        script,div=components(p,CDN)
        cdn_js=CDN.js_files
        cdn_css=CDN.css_files
        a *= 100
        b *= 100
        h *= 100
        d1 *= 100
        d2 *= 100
        if (a.is_integer()):
            a = int(a)
        if (b.is_integer()):
            b = int(b)
        if (h.is_integer()):
            h = int(h)
        if (d1.is_integer()):
            d1 = int(d1)
        if (d2.is_integer()):
            d2 = int(d2)
        if (Tzew.is_integer()):
            Tzew = int(Tzew)
        if (Tzad.is_integer()):
            Tzad = int(Tzad)
        if (Tnoc.is_integer()):
            Tnoc = int(Tnoc)
        return render_template("bokeh.html",script1=script, div1=div, cdn_css=cdn_css, cdn_js=cdn_js[0], glebokosc=a, szerokosc=b, 
        wysokosc=h, grubosc_scianek=d1, grubosc_frontu=d2, temperatura_dzien=Tzad, temperatura_otoczenia=format(Tzew,'.1f'), temperatura_noc=Tnoc)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
