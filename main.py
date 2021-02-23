from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

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
        d1=float(request.form["grubosc_scianek"])/1000 #grubość ścianki
        d2=float(request.form["grubosc_frontu"])/1000
        S1=a*h+2*b*h+a*b
        S2=a*h
        strata=S1*lambda1/d1+S2*lambda2/d2
        pom=cv*V*ro
        tp=1
        kp=0.008
        Ti=0.25
        Td=0.05
        N=172200
        if(Tzew > Tzad):
            Tzad = Tzew
        if(Tzew > Tnoc):
            Tnoc = Tzew
        T=Tzew
        e=[Tzad-Tzew]
        temp = Tzad-T
        Qdmax = 24
        umax = 20
        a=(Qdmax/umax)/100
        x=[0]
        y=[Tzew]
        n=1
        esum = e[0]
        while n<=N:
            if (n%86400>43200):
                temp = Tnoc - T
            else:
                temp = Tzad - T
            e.append(temp)
            esum += e[n]
            u=kp*(e[-2]+(tp/Ti)*esum+(Td/tp)*(e[-1]-e[-2]))
            #if (u > umax):
            #    u = umax
            Qd=a*u
            if (Qd > 230):
                Qd = 230
            #print(e[n],u, "\n")
            T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(pom)+ T
            #print(n,T)
            if (T>30): #T>tmax
                T=30
                #e[-1]=Tzad-T
            x.append(n*tp)
            y.append(T)
            n+=1
        p=figure(plot_width=723,plot_height=400,tools='',x_axis_label="Czas [s]",y_axis_label="Temperatura [st. C]")
        p.border_fill_color='#fac096'
        p.line(x,y)
        script,div=components(p,CDN)
        cdn_js=CDN.js_files
        cdn_css=CDN.css_files
        return render_template("bokeh.html",script1=script, div1=div, cdn_css=cdn_css, cdn_js=cdn_js[0])
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
