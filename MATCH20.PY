
import pandas as pd
from multiprocessing import Process

#https://docs.python.org/2/library/multiprocessing.html#
#https://www.geeksforgeeks.org/multiprocessing-python-set-1/

#DataFrame EXTRANJEROS
url="https://docs.google.com/spreadsheets/d/e/2PACX-1vRmFZT3OcFlVbzLSvYSkWgbY6fUz7_lxScDXc5sbFpt1jPC83hDDqwzU6tzvwtGOQLK1NyVXJ9DYkVA/pub?output=csv"
informacion=pd.read_csv(url)
df=pd.DataFrame(informacion)

#DataFrame TUTORES
url2="https://docs.google.com/spreadsheets/d/e/2PACX-1vSOnu6I8BcHqvLOPNV9dyW8A-umuMNcx-h8V1rUaHIlCcPl8eTgRdehUWnd-n0xWDWPBPn2uQ7XqEWn/pub?gid=609779175&single=true&output=csv"
tutores=pd.read_csv(url2)
df2=pd.DataFrame(tutores)

def match():
    #Definimos las dimensiones que necesitamos segun el TEST de Autoconcepto.

    dfAcademico=pd.DataFrame(informacion,columns=[
        '1) Hago bien los trabajos escolares (profesionales).',  
        '6) Mis profesores me consideran un buen trabajador.',
        '11) Trabajo mucho en clase.', 
        '16) Mis profesores me estiman.',
        '21)  Soy un buen estudiante.',
        '26) Mis profesores me consideran inteligente y trabajador.'
        ])

    dfSocial=pd.DataFrame(informacion,columns=[
        '2)  Hago fácilmente amigos.', '3) Tengo miedo de algunas cosas.',
        '7) Soy una persona amigable.', '8) Muchas cosas me ponen nervioso.',
        '12) Es difícil para mí hacer amigos.',
        '17) Soy una persona alegre.',
        '22) Me cuesta hablar con desconocidos.',
        '27) Tengo muchos amigos.'
        ])

    dfEmocional=pd.DataFrame(informacion,columns=[
        '3) Tengo miedo de algunas cosas.',
        '8) Muchas cosas me ponen nervioso.',
        '13) Me asusto con facilidad.', 
        '18) Cuando los mayores dicen algo me pongo muy nervioso.',
        '23) Me pongo nervioso cuando me pregunta el profesor.',
        '28) Me siento nervioso.'
        ])

    Academico = dfAcademico.sum(axis=1)/60
    Social = dfSocial.sum(axis=1)/60
    Emocional = (600-dfEmocional.sum(axis=1))/60

    Calculo = (Academico + Social + Emocional)/3

    new_df=df.assign(Calculo = (Calculo)).sort_values(by=['Calculo'], ascending=True)
    #Agregué la columna de Ranking.
    new_df2=new_df.assign(Ranking= (df.index+1))
    #print(new_df2)

    #NO PUDE AGREGAR LAS 2 COLUMNAS EN SIMULTANEO, seguro que hay alguna forma.

    #Match entre Extranjero y Alumno de la UM.
    new_df3=pd.merge(df2,new_df2,on='Ranking').sort_values(by=['Ranking'], ascending=True)
    #print(new_df3.columns)
    print(new_df3[['Ranking','ALUMNO UM',  'Correo','Calculo']])
   
if __name__ == '__main__':
    p = Process(target=match, )
    p.start()
    p.join()