M='_categorized_words.csv'
H=','
G=float
E=print
C=len
A=None
from multiprocessing import Pool
from os import error as F
import sys,os,time as I,json as J
import numpy as B
class K:
	def __init__(A):A.initial=1
	def getMovieListFromReview(C,filepath):
		A=[]
		for B in os.listdir(filepath):A.append(B.split(M)[0])
		return A
	def readCSVTables(C,filepath):
		A=[]
		with open(filepath,'r',encoding='utf-8')as B:A=B.read().split('\n\n')
		return A
class N:
	def __init__(A):A.initial=1
	def getListFromParameter(D):
		A=[]
		try:
			for B in sys.argv[1][1:C(sys.argv[1])-1].split(H):A.append(B.replace("'",'').replace('*',' '))
		except:E(F)
		finally:return A
	def getListFromInput(G,input_string):
		A=input_string;B=[]
		try:
			for D in A[1:C(A)-1].split(H):B.append(D.replace("'",'').replace('*',' '))
		except:E(F)
		finally:return B
class O:
	def __init__(A):A.initial=1
	def getWeightFromGapBetweenWeight(A,x):return-2/B.pi*B.arctan(2*x-2)+1
	def getWeightFromGapBetweenDistance(A,x,maxdistance,max,min):
		if x>10:x=10
		return(max-min)/2*B.cos(x*(B.pi/maxdistance))+(max+min)/2
class P:
	filepath=A;filereader=K();movie_weight_map={};formulacalculator=O()
	def __init__(A):A.initial=1
	def readAllMovieWeightList(A,reviewpath,movielist):
		B={};A.filepath=reviewpath
		with Pool(os.cpu_count())as C:D=C.map(A.getWeightFromMovieElement,movielist)
		for E in D:
			for(F,G)in E.items():B[F]=G
		A.movie_weight_map=B;return B
	def getWeightBetweenMovies(B):A={};return A
	def compareAllMovieWeightList(E,weightlist,mvlist_param,mvlist_review):
		F=weightlist;I={}
		for G in mvlist_review:
			if G not in mvlist_param:
				H=0;D=E.movie_weight_map[G]
				for C in D.keys():
					J=0;K=0
					if F.get(C)==A or D.get(C)==A:continue
					M=F[C][0][0];L=F[C][0][1];N=D[C][0][0];O=D[C][0][1];J=E.formulacalculator.getWeightFromGapBetweenDistance(B.abs(M-N),10,2,.2);K=E.formulacalculator.getWeightFromGapBetweenWeight(B.abs(L-O));H=H+L*J*K
				I[H]=G
		return I
	def getWeightFromMovieList(E,mvlist_param):
		C={}
		for F in mvlist_param:
			D=E.movie_weight_map[F]
			for B in D:
				G=D[B][0][0];H=D[B][0][1]
				if C.get(B)==A:C[B]=[]
				C[B].append((G,H))
		I=C;return I
	def getWeightFromMovieElement(J,args):
		N=J.filereader.readCSVTables(J.filepath+args+M);O=N[1];K=O.split('\n');D={};E={};L=0
		for P in range(1,C(K)-1):
			F=K[P].split(H);L+=G(F[1])
			try:D[F[0]]=[(G(F[1]),G(F[2]))]
			except:continue
		Q=L;I=D.keys();R=C(I);S=list(I)
		for B in I:
			T=D[B][0][1];U=D[B][0][0];V=U/Q;W=V*R;X=T*W;Y=S.index(B)
			if E.get(B)==A:E[B]=[]
			E[B].append((Y,X))
		return{args:E}
	def getWeightFromMovieWithDistance(L,weightlist):
		H=weightlist;B={}
		for D in H.keys():
			E=H.get(D,[(0,0)]);F=0;G=0;I=0;J=0
			for K in E:F=F+K[1];G=G+K[0]
			I=F/C(E);J=G/C(E)
			if B.get(D)==A:B[D]=[]
			B[D].append((J,I))
		return B
class Q:
	reviewFolderpath=A;weightcalculator=P();parameterhandler=N()
	def __init__(A):A.initial=1
	def getMovieListFromParameter(A):return A.parameterhandler.getListFromParameter()
	def getMovieListFromInput(A,input_string):return A.parameterhandler.getListFromInput(input_string)
	def getMovieListFromReviews(A):return K().getMovieListFromReview(A.reviewFolderpath)
	def readAllMovieWeightList(A,mvlist):return A.weightcalculator.readAllMovieWeightList(A.reviewFolderpath,mvlist)
	def getWeightListFromMovieList(A,mvlist_param):return A.weightcalculator.getWeightFromMovieList(mvlist_param)
	def getWeightListBetweenMovies(A,mvlist_param,mvlist_review,avg_weightlist):return A.weightcalculator.compareAllMovieWeightList(avg_weightlist,mvlist_param,mvlist_review)
	def makeResult(A):
		B=input()
		if B=='end':return
		D=I.time();C=A.getMovieListFromInput(B);F=A.getWeightListBetweenMovies(C,L,A.getWeightListFromMovieList(C));G=dict(sorted(F.items(),key=lambda item:item[0],reverse=True));H={A:B for(A,B)in list(G.items())[:10]};E(J.loads(J.dumps(H)));E(f"elapse time : {I.time()-D}");A.makeResult()
	def setReviewFolderpath(A,filepath):A.reviewFolderpath=filepath
	def getReviewFolderpath(A):return A.reviewFolderpath
if __name__=='__main__':D=Q();D.setReviewFolderpath('../../csvfile/');L=D.getMovieListFromReviews();R=D.readAllMovieWeightList(L);D.makeResult()