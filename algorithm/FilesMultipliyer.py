import skrf as rf
import numpy
import matplotlib.pyplot as plt

thefile = 'sunam_ideal_1601.s2p'
filenoise = str(thefile) + '_noise'
folderloc = 'sunam_ideal_1601var80'

amountoffiles = 100

varianceofnoise = numpy.sqrt(10**(-6))

file_name = 'C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/PublicationData/' + str(thefile)


ring_slot = rf.Network(file_name)
df = ring_slot.to_dataframe()  # Convert .s2p to dataframe in order to work with the data
s21 = ring_slot.s[:,1,0] # S21 values from the S-Parameter Matrix in .s2p file
s12 = ring_slot.s[:,0,1]
s11 = ring_slot.s[:,0,0]
s22 = ring_slot.s[:,1,1]
re11 = s11.real # X = REAL part of S21
im11 = s11.imag # Y = IMAGINARY part of S21
re21 = s21.real # X = REAL part of S21
im21 = s21.imag # Y = IMAGINARY part of S21
re12 = s12.real # X = REAL part of S21
im12 = s12.imag # Y = IMAGINARY part of S21
re22 = s22.real # X = REAL part of S21
im22 = s22.imag # Y = IMAGINARY part of S21
f = df['s_db 21'].index

Listofnoise = numpy.random.normal(0, numpy.sqrt(10 ** (-8)), len(re21))
squarednoise = []

for h in Listofnoise:
    squarednoise.append(h**2)

print(numpy.average(squarednoise))

for i in range(amountoffiles):

    re11noise = re11 + numpy.random.normal(0,varianceofnoise,len(re21))
    im11noise = im11 + numpy.random.normal(0,varianceofnoise,len(re21))
    re21noise = re21 + numpy.random.normal(0, varianceofnoise, len(re21))
    im21noise = im21 + numpy.random.normal(0, varianceofnoise, len(re21))
    re12noise = re12 + numpy.random.normal(0, varianceofnoise, len(re21))
    im12noise = im12 + numpy.random.normal(0, varianceofnoise, len(re21))
    re22noise = re22 + numpy.random.normal(0, varianceofnoise, len(re21))
    im22noise = im22 + numpy.random.normal(0, varianceofnoise, len(re21))

    DataToSave = []
    DataToSave.append(numpy.column_stack((f, re11, im11, re21noise, im21noise, re12, im12, re22, im22)))

    data_top = '! Created Tue Mar 24 16:12:56 2020 \n' + '# hz S RI R 50\n' + '! 2 Port Network Data from SP2.P NOISEADDED\n'

    with open('C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/PublicationData/' + str(folderloc) + "/"  + str(filenoise) + str(i) + '.s2p', 'w') as filetosave:
        filetosave.write(str(data_top) + '\n')
        for data in DataToSave:
            numpy.savetxt(filetosave, data, delimiter="    ", fmt='%s')
    filetosave.close()

"""
plt.plot(f, re21, '-', label= 'S21 re')
plt.plot(f, im21, '-', label='S21 im')
plt.plot(f, re21noise, '-', label= 'S21 re Noise')
plt.plot(f, im21noise, '-', label='S21 im Noise')
plt.xlabel('freq')
plt.ylabel('s21')
plt.grid()
plt.legend()
plt.show()
"""
print("THIS IS DONE OH YEAH!")
