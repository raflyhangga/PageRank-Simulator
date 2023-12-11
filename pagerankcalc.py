import os
import copy
import matplotlib.pyplot as plt

"""
Fungsi Pembantu Operasi
"""
def isAdjacent(stateA:int,stateB:int,matrix) -> bool :
    # Mengembalikan true jika stateA -> stateB
    return matr[stateB][stateA] == 1

def countEdgeOut(stateA:int, matrix) -> int :
    # Mengembalikan dout (deraja keluar) dari suatu vertices
    count = 0
    for value in matrix[stateA]:
        if value == 1:
            count+=1
    return count

def pageRankAccumulator(state:int,pageRank,matrix) -> float:
    # Mengembalikan nilai float PageRank 
    jumlah = 0
    accumulator = 0
    jumlah += (1-0.85)
    for i in range(0,len(pageRank)):
        if i != state and isAdjacent(state,i,matrix):
            accumulator += pageRank[i] / countEdgeOut(i,matrix)
    jumlah += 0.85 * accumulator
    return jumlah

def stateViewer(adjMatrix,pageRank):
    # Menampilkan keadaan state
    print("\n================= KEADAAN STATE =================")
    print("Adjacency Matriks:")
    for x in range(len(adjMatrix[0])):
        for y in range(len(adjMatrix)):
            print(adjMatrix[x][y], end=" ")
        print()
    print("\nPage Rank:")
    total = 0
    for i in range(0,len(pageRank)):
        print("Situs"+str(i+1) + ": " ,end="")
        print(pageRank[i])
        total += pageRank[i]
    print(f"\nAverage PR: "+str(total/len(pageRank)))

def isThresholdSatisfied(oldPageRank,newPageRank,threshold) -> bool:
    # Mengembalikan nilai true apabila nilai threshold sudah tercapai
    panjang = len(oldPageRank)
    cek = True
    i = 0
    while(cek and i < panjang):
        difference = abs(newPageRank[i] - oldPageRank[i])
        if difference < threshold*0.1:
            cek = True
        else:
            cek = False
        i+= 1
    return cek

""" INISIALISASI DATA """
os.system('cls') # Menghapus command prompt
program = True # Menyatakan status program
pageRank = [] # Menyinpan nilai pageRank setiap state
prevPageRank = pageRank # Menyimpan nilai pageRank lama


""" INPUT PROGRAM """
# Input nilai matriks
N = int(input("Ada berapa page yang ingin dimasukan?: "))
matr = [[0 for i in range(N)] for j in range(N)]
os.system('cls')
print("Tentukan hubungan setiap pagenya! (Y/N)")
for i in range (0,N):
    for j in range (0,N):
        if j != i:
            masukan=input(f"Situs {str(i+1)} -> Situs {str(j+1)}: ")
            if (masukan == 'Y'):
                print("masuk")
                matr[i][j] = 1

# Input probabilitas / PageRank awal setiap situs
os.system('cls')
print("Tentukan peluang awal setiap situs! (Nilai positif)")
for i in range(0,N):
    masukan = float(input(f"Situs {str(i+1)}: "))
    pageRank.append(masukan)
iterasi = 1

# Input threshold distribusi
os.system('cls')
threshold = float(input("Masukan threshold yang diinginkan (contoh: 0.001): "))
os.system('cls')

# Initialize the plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
lines = [ax.plot([], [], label=f"Situs {i+1}")[0] for i in range(len(pageRank))]

# Initialize data for each line
line_data = [[] for _ in range(len(pageRank))]

""" PROSES UTAMA """
while(program):

    prevPageRank = copy.deepcopy(pageRank) # Menyimpan nilai PageRank sebelum berubah

    # Setup Plot
    for state, line in enumerate(lines):
        line_data[state].append(pageRank[state])
        line.set_xdata(range(len(line_data[state])))
        line.set_ydata(line_data[state])

    # Mengubah pageRank setiap state
    for state in range(0,len(pageRank)):
        pageRank[state] = pageRankAccumulator(state,pageRank,matr)

    # Plot the current PageRank values
    ax.relim()
    ax.autoscale_view()

    plt.title(f"Grafik Page Rank")
    plt.xlabel("Iteration")
    plt.ylabel("PageRank")
    plt.legend()

    plt.show()
    plt.pause(0.1)   

    # Menampilkan keadaan setiap situs
    stateViewer(matr,pageRank)
    print(f"Threshold: {str(threshold)}")
    print(f"\nIterasi ke-{str(iterasi)}")

    # Mengecek apakah threshold terpenuh atau tidak
    if(isThresholdSatisfied(prevPageRank,pageRank,threshold) and iterasi != 1):
        print("Threshold is satisfied")
        program = False # Apabila terpenuhi, program akan berhenti
    else:
        print("Threshold is not satisfied")
    iterasi+=1

# Menutup layar interaktif
plt.ioff()
plt.show()