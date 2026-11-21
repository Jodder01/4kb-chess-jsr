import time
from itertools import count
p={'P':100,'N':280,'B':320,'R':480,'Q':929,'K':60000}
pst={'P':(0,0,0,0,0,0,0,0,78,83,86,73,102,82,85,90,7,29,21,44,40,31,44,7,-17,16,-2,15,14,0,15,-13,-26,3,10,9,6,1,0,-23,-22,9,5,-11,-10,-2,3,-19,-31,8,-7,-37,-36,-14,3,-31,0,0,0,0,0,0,0,0),'N':(-66,-53,-75,-75,-10,-55,-58,-70,-3,-6,100,-36,4,62,-4,-14,10,67,1,74,73,27,62,-2,24,24,45,37,33,41,25,17,-1,5,31,21,22,35,2,0,-18,10,13,22,18,15,11,-14,-23,-15,2,0,2,0,-23,-20,-74,-23,-26,-24,-19,-35,-22,-69),'B':(-59,-78,-82,-76,-23,-107,-37,-50,-11,20,35,-42,-39,31,2,-22,-9,39,-32,41,52,-10,28,-14,25,17,20,34,26,25,15,10,13,10,17,23,17,16,0,7,14,25,24,15,8,25,20,15,19,20,11,6,7,6,20,16,-7,2,-15,-12,-14,-15,-10,-10),'R':(35,29,33,4,37,33,56,50,55,29,56,67,55,62,34,60,19,35,28,33,45,27,25,15,0,5,16,13,18,-4,-9,-6,-28,-35,-16,-21,-13,-29,-46,-30,-42,-28,-42,-25,-25,-35,-26,-46,-53,-38,-31,-26,-29,-43,-44,-53,-30,-24,-18,5,-2,-18,-31,-32),'Q':(6,1,-8,-104,69,24,88,26,14,32,60,-10,20,76,57,24,-2,43,32,60,72,63,43,2,1,-16,22,17,25,20,-13,-6,-14,-15,-2,-5,-1,-10,-20,-22,-30,-6,-13,-11,-16,-11,-16,-27,-36,-18,0,-19,-15,-15,-21,-38,-39,-30,-31,-13,-31,-36,-34,-42),'K':(4,54,47,-99,-99,60,83,-62,-32,10,55,56,56,55,10,3,-62,12,-57,44,-67,28,37,-31,-55,50,11,-4,-19,13,0,-49,-47,-42,-43,-79,-64,-32,-29,-32,-4,3,-14,-50,-57,-18,13,4,17,30,-3,-14,6,-1,40,18)}
def pv(c,i):return pst[c][i%64]+p[c]
N,E,S,W=-10,1,10,-1
ML,MU=1000,10000
D={'P':(N,N+N,N+W,N+E),'N':(N+N+E,E+N+E,E+S+E,S+S+E,S+S+W,W+S+W,W+N+W,N+N+W),'B':(N+E,S+E,S+W,N+W),'R':(N,E,S,W),'Q':(N,E,S,W,N+E,S+E,S+W,N+W),'K':(N,E,S,W,N+E,S+E,S+W,N+W)}
I="         \n         \n rnbqkbnr\n pppppppp\n ........\n ........\n ........\n ........\n PPPPPPPP\n RNBQKBNR\n         \n         \n"
class P:
 def __init__(self,b,s,w):self.b,self.s,self.w=b,s,w
 def g(self):
  for i,c in enumerate(self.b):
   if c not in'PNBRQK':continue
   for d in D[c]:
    for j in count(i+d,d):
     q=self.b[j]
     if q in' \nPNBRQK':break
     if c=='P':
      if d in(N,N+N)and q!='.':break
      if d==N+N and(i<21+N or self.b[i+N]!='.'):break
      if d in(N+W,N+E)and q=='.':break
      if 21<=j<=28:
       for m in'NBRQ':yield(i,j,m)
       break
     yield(i,j,'')
     if c in'PNK'or q in'pnbrqk':break
 def r(self):return P(self.b[::-1].swapcase(),-self.s,self.w[::-1])
 def m(self,mv):
  i,j,pm=mv
  c,q=self.b[i],self.b[j]
  b=self.b[0:i]+'.'+self.b[i+1:j]+self.b[i]+self.b[j+1:]
  s=self.s+pv(q.upper(),119-j)if q in'pnbrqk'else self.s
  if c=='P' and 21<=j<=28:b=b[0:j]+pm+b[j+1:]
  if c=='K' and abs(j-i)==2:b=b[0:21 if j<i else 28]+'.'+b[(21 if j<i else 28)+1:(i+j)//2]+'R'+b[(i+j)//2+1:]
  return P(b,s,self.w).r()
 def a(self):
  for m in self.g():
   if self.b[m[1]]=='k':return 1
  return 0
def q(o,a,b):
 if o.s<=-ML:return -MU
 for m in sorted([x for x in o.g() if o.b[x[1]]in'pnbrqk'],key=lambda x:pv(o.b[x[1]].upper(),119-x[1]),reverse=1):
  v=-q(o.m(m),-b,-a)
  b=max(b,v)
  if b>=a:break
 return o.s if b<o.s else b
class S:
 def __init__(self):self.t={}
 def ab(self,o,a,b,d):
  if d<=0:return q(o,a,b)if o.s<-900 else o.s
  h=hash(o.b)
  if h in self.t:return self.t[h]
  for m in o.g():
   v=-self.ab(o.m(m),-b,-a,d-1)
   b=max(b,v)
   if b>=a:break
  self.t[h]=b
  return b
o=P(I,0,(1,1))
s=S()
while 1:
 try:L=input().strip()
 except EOFError:break
 if L.startswith('uci'):print('id name TinyChess\nuciok')
 elif L=='isready':print('readyok')
 elif L.startswith('position'):
  if'startpos'in L:o=P(I,0,(1,1));s.t={}
  elif'moves'in L:
   for um in L.split('moves')[1].strip().split():
    fi=(ord(um[0])-97)+((8-int(um[1]))*10)+20
    ti=(ord(um[2])-97)+((8-int(um[3]))*10)+20
    for m in o.g():
     if m[0]==fi and m[1]==ti:o=o.m(m);break
 elif L.startswith('go'):
  bm=None
  for d in range(1,6):
   for m in o.g():
    if-s.ab(o.m(m),-MU,MU,d-1)<10000:bm=m;break
  if bm:print('bestmove '+chr(97+bm[0]%10)+str(9-bm[0]//10)+chr(97+bm[1]%10)+str(9-bm[1]//10))