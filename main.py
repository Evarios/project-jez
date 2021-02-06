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
        #cv=1005 #powietrza
        a=float(request.form["glebokosc"])
        b=float(request.form["szerokosc"])
        h=float(request.form["wysokosc"])
        #V=a*b*h
        #ro=1.21 #gestosc
        Tzad=float(request.form["temperatura_dzien"]) #zadana
        Tzew=float(request.form["temperatura_otoczenia"]) #otoczenia/początkowa
        #1 - boki, 2- front
        lambda1=float(request.form["material_scianek"])  #przenikalność cieplna materiału 
        lambda2=float(request.form["material_frontu"])
        d1=float(request.form["grubosc_scianek"]) #grubość ścianki
        d2=float(request.form["grubosc_frontu"])
        S1=a*h+2*b*h+a*b
        S2=a*h
        strata=S1*lambda1/d1+S2*lambda2/d2
        #pom=cv*V*ro
        tp=0.01
        kp=0.1
        Ti=0.25
        Td=0.05
        N=100000
        T=Tzew
        e=[Tzad-Tzew]
        Qdmax = 64
        umax = 10
        a=Qdmax/umax
        x=[0]
        y=[Tzew]
        n=1
        while n<=N:
            e.append(Tzad-T)
            u=kp*(e[-2]+(tp/Ti)*sum(e)+(Td/tp)*(e[-1]-e[-2]))
            #if (u > umax):
            #    u = umax
            Qd=kp*u
            if (Qd > 230):
                Qd = 230
            #print(e[n],u, "\n")
            T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(tp*strata)+T
            #print(n,T)
            if T>45: #T>tmax
                T=45
                #e[-1]=Tzad-T
            x.append(n*tp)
            y.append(T)
            n+=1
        p=figure(plot_width=475,plot_height=400,tools='')
        p.line(x,y)
        script,div=components(p,CDN)
        cdn_js=CDN.js_files
        cdn_css=CDN.css_files
        return render_template("bokeh.html", script1=script, div1=div, cdn_css=cdn_css, cdn_js=cdn_js[0])
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)