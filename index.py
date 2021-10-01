from flask import Flask, render_template, request
from werkzeug.exceptions import MethodNotAllowed 
import networkx as nx #grafo
import matplotlib.pyplot as plt #vizualisar
from pyvis.network import Network #""
import webbrowser #desplegar web
import numpy as np 
import itertools

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/opciongrafo', methods=['POST'])

def tipodegrafo():

    tipodegrafo = request.form["tipodegrafo"]
    global G, D
    global tipo, tipo2
    

    if(tipodegrafo == "normal"):
        G = nx.Graph ()
        D = nx.Graph ()
        tipo="normal"
        tipo2="normal"

    if(tipodegrafo == "dirigido"):
        G = nx.DiGraph() 
        D = nx.DiGraph()
        tipo = "dirigido" 
        tipo2="dirigido"  

    if(tipodegrafo == "Multigrafo"):
        G = nx.MultiGraph() 
        D = nx.MultiGraph()
        tipo = "Multigrafo" 
        tipo2="Multigrafo"

    if(tipodegrafo == "Multidigrafo"):
        G = nx.MultiDiGraph()
        D = nx.MultiDiGraph()
        tipo = "Multidigrafo"  
        tipo2="Multidigrafo"
        
    return render_template("home.html")



@app.route('/formulario', methods=['POST'])

def definir():

    
    numnodo=1
    vertini=""
    vertfin=""
    nomnodo = request.form["nomnodo"]
    vertini = request.form["vertini"]
    vertfin = request.form["vertfin"]
    
    if(nomnodo != ""):
        G.add_node (nomnodo)

    if(vertfin != " " and vertfin !=""):
        G.add_edge(vertini, vertfin)

    nx.draw (G, with_labels=True)
    plt.show()
    
    
    return render_template("home.html", nombrenodo = nomnodo)

@app.route('/isomorfo', methods=['POST'])

def isomorfo():
    cantidad=nx.number_of_nodes(D)
    if(cantidad>=1):
        D.remove_node("nulo")

    avisoisomorfo="--";
    vertini=""
    vertfin=""
    nomnodo = request.form["nomnodo"]
    vertini = request.form["vertini"]
    vertfin = request.form["vertfin"]
    
    if(nomnodo != ""):
        D.add_node (nomnodo)

    if(vertfin != " " and vertfin !=""):
        D.add_edge(vertini, vertfin)
    plt.title("Grafo 1")
    nx.draw (G, with_labels=True)
    plt.show()
    plt.title("Grafo 2")
    nx.draw (D, with_labels=True)
    plt.show()

    if(nx.is_isomorphic(G, D)):
        avisoisomorfo="Si son isomorfo"
    else:
        avisoisomorfo="No es isomorfo"


    return render_template("home.html", avisoisomorfo=avisoisomorfo)    

@app.route('/eliminarnodo', methods=['POST'])

def eliminar():

    nomnodoelim = request.form["nomnodoelim"]
    
    if(nomnodoelim != ""):
        G.remove_node(nomnodoelim) 
    nx.draw (G, with_labels=True)
    plt.show ()
    
    return render_template("home.html")

@app.route('/ponderacion', methods=['POST'])

def ponderar():

    vertini = request.form["vertini"]
    vertfin = request.form["vertfin"]
    peso = request.form["peso"]
    if(vertfin != " " and vertfin !="" and peso!=""):
        
        #G.add_weighted_edges_from([(vertini, vertfin,peso)])
        G.add_edges_from([(vertini,vertfin)],  weight=peso, label=peso)
        
    edge_labels=dict([((u,v,),d['weight'])
                 for u,v,d in G.edges(data=True)])
                 
    pos=nx.spring_layout(G)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    nx.draw(G,pos, with_labels=True)     
    plt.draw ()
    plt.show ()
    
    return render_template("home.html")    


@app.route('/grafointeractivo', methods=['POST'])

def vergrafo():
    
    if(tipo == "dirigido"):
        net = Network(notebook= True, directed = True)
        net.show_buttons(filter_=True)
        net.from_nx(G)
        net.show("about.html")
    if(tipo=="normal"):   
        net = Network(notebook= True)
        net.show_buttons(filter_=True)
        net.from_nx(G)
        net.show("about.html")
    if(tipo=="Multigrafo"):   
        net = Network(notebook= True)
        net.show_buttons(filter_=True)
        net.from_nx(G)
        net.show("about.html")
    if(tipo=="Multidigrafo"):   
        net = Network(notebook= True, directed = True)
        net.show_buttons(filter_=True)
        net.from_nx(G)
        net.show("about.html")
    

        
    if(G!=""):
        webbrowser.open_new('about.html')

    return render_template("home.html")


@app.route('/eliminargrafo', methods=['POST'])

def eliminargrafo():

    if(G!=""):
        G.clear()
    
    return render_template("home.html")  


@app.route('/eliminararista', methods=['POST'])

def eliminararista():

    vertini = request.form["vertini"]
    vertfin = request.form["vertfin"]

    G.remove_edge(vertini, vertfin)
    nx.draw (G, with_labels=True)
    plt.show()

    return render_template("home.html")    

def coloreado_voraz(grafo):

    colores = {}
    nodos = grafo.nodes()
    for u in nodos:
        colores_vecinos = {colores[v] for v in grafo[u] if v in colores}
        for color in itertools.count():
            if color not in colores_vecinos:
                break
        colores[u] = color
    return colores



@app.route('/colorear', methods=['POST'])

def colorear():

    colores_dict = {0:'pink', 1: 'blue', 2: 'green', 3:'red', 4:'orange', 5:'yellow'}
    colores = []
    coloreado = coloreado_voraz(G)

    for i,j in coloreado.items():
        colores.append(colores_dict[coloreado[i]])
    nx.draw(G,node_color = colores,with_labels = True)

    plt.show()
    return render_template("home.html")   

@app.route('/dijkstra', methods=['POST'])

def dijkstra():

    vertfin2=""
    vertini2=""
    vertini = request.form["vertini"]
    vertfin = request.form["vertfin"]
    vertini2 = request.form["vertini2"]
    vertfin2 = request.form["vertfin2"]
    D.add_node ("nulo")
    numerodenodos2= nx.number_of_nodes(D)


    if(numerodenodos2>=2):
        if(vertini2!= " " and vertfin2!=" "):
            D.remove_node("nulo")
            rutacorta2 = nx.dijkstra_path(D, vertini2, vertfin2)
    else:
        rutacorta2="--"    


    rutacorta = nx.dijkstra_path(G, vertini, vertfin)
    
    
    return render_template("home.html", rutacorta=rutacorta, rutacorta2=rutacorta2)     
  
 

@app.route('/verinformacion', methods=['POST'])


def verinformacion():
    
    
    D.add_node ("nulo")
    tipo2 =tipo
    numerodenodos= nx.number_of_nodes(G)
    numeroaristas = nx.number_of_edges(G)
    numerodenodos2antes= nx.number_of_nodes(D)
    numeroaristas2 = nx.number_of_edges(D)
    matrizcopia = nx.to_numpy_array(G)
    
    avisoconexo="--"
    avisoconexo2="--"
    textoponderado2=""
    plano2="--"
    regular2="--"
    
    esciclo="--"
    esrueda="--"
    
    
    cont2=1
    

    if(numerodenodos2antes>1):
        
        D.remove_node("nulo")
        matrizcopia3 = nx.adjacency_matrix(D,weight=1).todense() 
        numerodenodos2= nx.number_of_nodes(D)
        matrizidentidad2 = np.identity(numerodenodos2)
        matrizcopia4 = nx.to_numpy_array(D)
        matrizcamino2 = matrizcopia4
        
        if(tipo2 != "dirigido" and tipo2 != "Multidigrafo"):
            if(nx.is_connected ( D)):
                avisoconexo2="SI"
            else:
                avisoconexo2="NO" 

        if(tipo=="dirigido" ):
            if(nx.is_semiconnected(D)):
                avisoconexo2="SI"
            else:
                avisoconexo2="NO"

        if(nx.is_weighted(D)):
            textoponderado2="SI"
        else:
            textoponderado2="NO" 

        for cont2 in range(numerodenodos2-1):

            for i in range(numerodenodos2):
                for j in range(numerodenodos2):
                    if(cont2==numerodenodos2-1):
                        matrizcopia4[i][j]=matrizcopia4[i][j]+matrizidentidad2[i][j]
                    matrizelevada2=np.linalg.matrix_power(matrizcamino2, cont2)
                    matrizcopia4[i][j] = matrizcopia4[i][j] + matrizelevada2[i][j]

        if(nx.check_planarity(D, False)):
            plano2="SI"
        else:
            plano2="NO"  
    
        if(nx.is_regular(D)):
            regular2="SI"
        else:
            regular2="NO"
    else:
        numerodenodos2= "--"
        numeroaristas2 = "--"
        tipo2="--"
        matrizcopia3="--"
        matrizcopia4="--"
        textoponderado2="--"
        





    if(tipo!="dirigido" and tipo!= "Multidigrafo"):
        if(nx.is_connected ( G )):
            avisoconexo="SI"
        else:
            avisoconexo="NO" 
    if(tipo=="dirigido" ):
        if(nx.is_semiconnected(G)):
            avisoconexo="SI"
        else:
            avisoconexo="NO"    

    if(nx.is_weighted(G)):
        textoponderado="SI"
    else:
        textoponderado="NO" 

    matrizcopia2 = nx.adjacency_matrix(G,weight=1).todense() 

    matrizcamino = matrizcopia
    matrizidentidad = np.identity(numerodenodos)
    cont=1
    
    for cont in range(numerodenodos-1):


        for i in range(numerodenodos):
            for j in range(numerodenodos):
                if(cont==numerodenodos-1):
                    
                    matrizcopia[i][j]=matrizcopia[i][j]+matrizidentidad[i][j]
                matrizelevada=np.linalg.matrix_power(matrizcamino, cont)
                matrizcopia[i][j] = matrizcopia[i][j] + matrizelevada[i][j]

    if(nx.check_planarity(G, False)):
        plano="SI"
    else:
        plano="NO"  
    
    if(nx.is_regular(G)):
        regular="SI"
    else:
        regular="NO" 

    caminoEuleriano = nx.has_eulerian_path(G, source=None)

    caminoHamiltoniano = hamilton(G)

    if (caminoHamiltoniano == None):
        caminoHamiltoniano = "false"    
    
    if(tipo!="dirigido" and tipo!="Multidigrafo"):
        NodoCiclo=nx.number_of_nodes(G)
        ciclo=nx.cycle_graph(NodoCiclo)
        if(nx.is_isomorphic(G, ciclo)==True):
            esciclo="si"
        else:
            esciclo="no"

    if(tipo!="dirigido" and tipo!="Multidigrafo"):
        NodoRueda=nx.number_of_nodes(G)
        Rueda=nx.wheel_graph(NodoRueda)
        if(nx.is_isomorphic(G, Rueda)==True):
            esrueda="si"
        else:
            esrueda="no" 

    return render_template("home.html", numerodenodos = numerodenodos,numerodenodos2 = numerodenodos2,
     numeroaristas = numeroaristas,numeroaristas2 = numeroaristas2, tipodelgrafo=tipo, tipodelgrafo2=tipo2, avisografo=avisoconexo, 
     avisografo2=avisoconexo2, matrizcopia2=matrizcopia2,matrizcopia3=matrizcopia3, textoponderado=textoponderado,textoponderado2=textoponderado2, 
     matrizcamino=matrizcopia,matrizcamino2=matrizcopia4, plano=plano,plano2=plano2, regular=regular, regular2=regular2 , caminoEuleriano=caminoEuleriano, 
     caminoHamiltoniano=caminoHamiltoniano, esrueda=esrueda,esciclo=esciclo)    

def hamilton(G):
    F = [(G, [list(G.nodes())[0]])]
    n = G.number_of_nodes()
    while F:
        graph, path = F.pop()
        confs = []
        neighbors = (node for node in graph.neighbors(path[-1])
                     if node != path[-1])  # exclude self loops
        for neighbor in neighbors:
            conf_p = path[:]
            conf_p.append(neighbor)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g, conf_p))
        for g, p in confs:
            if len(p) == n:
                return p
            else:
                F.append((g, p))
    return None    
                

@app.route('/ncromatico', methods=['POST'])
def Ncromatico():
    a=0
    b=0
    listaEmer=[]
    nodos = np.array(G.nodes)   # lista
    aristas = (G.edges)    # lista de listas
    nnodos=nx.number_of_nodes(G)    #calculo el numero de vertices que hay
    aristas = np.array(aristas)   # Calculo el numero de aristas que tiene
    listaEmer = aristas.flatten().tolist()  #transformo la lista de listas en una lista simple
    naristas=len(listaEmer) # Calculo la cantidad de elemtos que tiene la arista
    cromatico=0
      
    for a in range (nnodos-1):                  # bucle 1
        contador=0      
        for b in range (naristas-1):        # comparo cuantas veces se une una arista con el nodo en la posicion[a]

            if (nodos[a]==listaEmer[b]):        
                contador +=1                # si se une, sumo 1
    
        if (cromatico < contador):      # veo si se ha nombrado mas veces que el anterior, y si es asi, guardo la cantidad mayor de aristas conectadas a un nodo
            cromatico = contador


    cromatico +=1   #al terinar de comparar, le sumo 1 al numero de aristas, para calcular el numero cromatico, y se envia
    return render_template ("home.html",cromatico=cromatico)


   # return render_template("home.html", numerodenodos = numerodenodos, numeroaristas = numeroaristas, tipodelgrafo=tipo, avisografo=avisoconexo,matrizcopia2=matrizcopia2, textoponderado=textoponderado, matrizcopia=matrizdefinitiva)
@app.route('/nregion', methods=['POST'])
def numeroregon():
    numerodenodos=nx.number_of_nodes(G)             # calculo el numero de nodos
    numeroaristas=nx.number_of_edges(G)             # calculo el numero de aristas
    Numeroregiones = ((2-numerodenodos)+numeroaristas)  # para calcular el numero de regiones, se le resta 2 a la cantidad de nodos, y se suma la cantidad de aristas

    return render_template ("home.html",Numeroregiones=Numeroregiones)  #se envia
@app.route('/caminosSimples', methods=['POST'])
def caminosSimples():
    vertini= request.form["vertini"]
    print(vertini)
    vertfin= request.form["vertfin"]
    print(vertfin)
    arreglo = []
    for path in nx.all_simple_paths(G, source=vertini, target=vertfin):
        arreglo.append(path)

    return render_template("home.html",caminoSimple=arreglo)



if __name__ == '__main__':
    app.run(debug=True)