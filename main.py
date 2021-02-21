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
        kp=0.01
        Ti=0.25
        Td=0.05
        N=86400
        if(Tzew > Tzad):
            Tzad = Tzew
        T=Tzew
        e=[Tzad-Tzew]
        temp = Tzad-T
        Qdmax = 24
        umax = 20
        a=Qdmax/umax
        x=[0]
        y=[Tzew]
        n=1
        while n<=N:
            if(n>43200):
                temp = Tnoc - T
            else:
                temp = Tzad - T
            e.append(temp)
            u=kp*(e[-2]+(tp/Ti)*sum(e)+(Td/tp)*(e[-1]-e[-2]))
            #if (u > umax):
            #    u = umax
            Qd=kp*u
            if (Qd > 230):
                Qd = 230
            #print(e[n],u, "\n")
            if (Qd < 0):
                T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(pom)+ T
            else:
                T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(pom)+ T
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
