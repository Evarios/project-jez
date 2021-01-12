import pylab

eta=0.95   #sprawnosc
R=1     #opor lampy
cv=1005 #powietrza
a=5
b=1.5
h=0.4
V=a*b*h
ro = 1.21 #gestosc
Tzad = 20 #zadana
Tzew = 0 #otoczenia/początkowa
#1 - boki, 2- front
lambda1 = 0.16  #przenikalność cieplna materiału 
lambda2 = 0.8
d1=0.05 #grubość ścianki
d2=0.01
S1=a*h+2*b*h+a*b
S2=a*h
strata=S1*lambda1/d1+S2*lambda2/d2
pom=cv*V*ro

tp=0.01
kp=0.1
Ti=0.25
Td=0.05
N=100000
T=Tzew
e = [Tzad-Tzew]

n=1
x=[0]
y=[Tzew]

while n<=N:
  e.append(Tzad-T)
  u=kp*(e[-2]+(tp/Ti)*sum(e)+(Td/tp)*(e[-1]-e[-2]))
  Qd=kp*u
  #print(e[n],u, "\n")

  T=(eta*(Qd**2)*tp/R-tp*(T-Tzew)*strata)/(tp*strata)+T
  #print(n,T)
  #if T>300: #T>tmax
   # T=300
    #e[-1]=Tzad-T

  x.append(n*tp)
  y.append(T)
  n+=1

pylab.plot(x,y)

pylab.show()
#test githuba
