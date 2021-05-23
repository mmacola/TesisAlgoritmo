import pandas as pd
from multiprocessing import Process
import numpy as np

#https://docs.python.org/2/library/multiprocessing.html#
#https://www.geeksforgeeks.org/multiprocessing-python-set-1/

#DataFrame TUTORES
url0="https://docs.google.com/spreadsheets/d/e/2PACX-1vSOnu6I8BcHqvLOPNV9dyW8A-umuMNcx-h8V1rUaHIlCcPl8eTgRdehUWnd-n0xWDWPBPn2uQ7XqEWn/pub?gid=609779175&single=true&output=csv"
tutores=pd.read_csv(url0)
df0=pd.DataFrame(tutores)

#DataFrame EXTRANJEROS
url1="https://docs.google.com/spreadsheets/d/e/2PACX-1vRmFZT3OcFlVbzLSvYSkWgbY6fUz7_lxScDXc5sbFpt1jPC83hDDqwzU6tzvwtGOQLK1NyVXJ9DYkVA/pub?output=csv"
informacion=pd.read_csv(url1)
df=pd.DataFrame(informacion)


def academico():
    #Definimos las dimensiones que necesitamos segunGRAC el TEST de Autoconcepto.

    dfAcademico=pd.DataFrame(informacion,columns=[
        '1) Hago bien los trabajos escolares (profesionales).',  
        '6) Mis profesores me consideran un buen trabajador.',
        '11) Trabajo mucho en clase.', 
        '16) Mis profesores me estiman.',
        '21)  Soy un buen estudiante.',
        '26) Mis profesores me consideran inteligente y trabajador.'
        ])
    return dfAcademico.sum(axis=1)/60

def social():
    dfSocial=pd.DataFrame(informacion,columns=[
        '2)  Hago fácilmente amigos.', '3) Tengo miedo de algunas cosas.',
        '7) Soy una persona amigable.', '8) Muchas cosas me ponen nervioso.',
        '12) Es difícil para mí hacer amigos.',
        '17) Soy una persona alegre.',
        '22) Me cuesta hablar con desconocidos.',
        '27) Tengo muchos amigos.'
        ])
    return dfSocial.sum(axis=1)/60
    
def emocional():
    dfEmocional=pd.DataFrame(informacion,columns=[
        '3) Tengo miedo de algunas cosas.',
        '8) Muchas cosas me ponen nervioso.',
        '13) Me asusto con facilidad.', 
        '18) Cuando los mayores dicen algo me pongo muy nervioso.',
        '23) Me pongo nervioso cuando me pregunta el profesor.',
        '28) Me siento nervioso.'
        ])
    return (600-dfEmocional.sum(axis=1))/60

def Match():
    calculo = (academico() + social() + emocional())/3

    df1=df.assign(calculo = (calculo)).sort_values(by=['calculo'], ascending=True)
    #Agregué la columna de Ranking.
    df2=df1.assign(Ranking= (df.index+1))
    #Match entre Extranjero y Alumno de la UM.
    df3=pd.merge(df0,df2,on='Ranking').sort_values(by=['Ranking'], ascending=True)
    #Buscar por un usuario
    a = df3.loc[df3['ALUMNO UM'] == user]
    b = df3.loc[df3['Correo'] == user]
    if a.empty or b.empty:
        if a.empty and b.empty:
            print('Este alumno, NO tiene Match!')
        else:
            if a.empty:
                print("\nTu MATCH es:")
                print(b[['ALUMNO UM']])
            else:
                print("\nTu MATCH es:")
                print(a[['Correo']])


if __name__ == '__main__':

    user = input("Enter your mail: ")
    p = Process(target=Match, )
    p.start()
    p.join()
