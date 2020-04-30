#!/usr/bin/env python
# coding: utf-8

# # PAQUETES Y FUNCIONES #

# In[3]:


import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import collections
from collections import Counter
import seaborn
import emoji
import os
from os import path
from wordcloud import WordCloud
get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib as mpl
mpl.rcParams['figure.dpi']= 400


def read_file(filename):
    """Reads the file and return as as stripped list"""
    with open(filename) as file:
        fr = file.readlines()    
        file_stripped = [line.strip() for line in fr]
        return file_stripped


def create_df(file_stripped):
    """Devuelve un dataframe con dos columnas: date y msj"""
    fechas = []
    msjs = []
    for line in file_stripped:
        if " - " in line:
            line_splitted=line.split(" - ")
            fechas.append(line_splitted[0])
            msjs.append(line_splitted[1])
            
    df = pd.DataFrame(data = [fechas, msjs]).T
    df.columns = ["date","msj"]
    return df



def add_msj_writter(df):
    """Agrega una columna para cada mensaje"""
    written_by_me = []
    for mensaje in df.msj:
        if mensaje[0:len(me)] == me:
            written_by_me.append(True)
        else:
            written_by_me.append(False)

    df["written_by_me"] = written_by_me

    written_by_other = []
    for mensaje in df.msj:
        if mensaje[0:len(other)] == other:
            written_by_other.append(True)
        else:
            written_by_other.append(False)

    df["written_by_other"] = written_by_other
    return df


def filter_messages(df):
    """Elimina mensajes sin autor, probablemente por un mal split"""
    real_msj = list(np.array(df.written_by_me) + np.array(df.written_by_other))
    df = df[real_msj]
    return df


def split_date(df):
    "Divide la fecha en columnas para año, mes, día y hora"

    years = []
    months = []
    days = []
    hours = []
    counter = 0
    for date in pd.to_datetime(df.date, dayfirst= True): 
            counter +=1
            years.append(date.year)
            months.append(date.month)
            days.append(date.day)
            hours.append(date.hour)

    df["year"] = years
    df["month"] = months
    df["day"] = days
    df["hour"] = hours
    return df


def countplotting(df, column, color):
    """Hace el barplot de la columna deseada del DF"""
    seaborn.countplot(x=column, data=df, color= color)
    plt.ylabel("messages count")
    plt.title(str("Mensajes según "+column+" con " + other))
    plt.xlabel(column)


def count_words(df):
    """Devuelve un diccionario con palabra:apariciones"""
    word_counts = {}
    for mensaje in df.msj:
        m = mensaje.lower() #pasa todo a minuscula
        skips = [",",".",";",":","''",'""',"-","'","?","/","#","*",'"',"!", "<multimedia", "omitido>"]
        for ch in skips:
            m = m.replace(ch, " ")

        for word in m.split(" "):
            #known word
            word.replace(" ","")
            if word in word_counts:
                word_counts[word]+=1
            #unseen word
            else:
                word_counts[word] = 1
    return word_counts


def add_elapsed_days(df):
    """Agrega una columna con los días que pasaron desde el primero(0) hasta el último"""
    timestamps = []
    for k in range(len(df)):
        timestamps.append(datetime.datetime.strptime(df.date.iloc[k] ,"%d/%m/%y %H:%M" ))

    elapsed_time = [time - timestamps[0] for time in timestamps]

    for i in range(len(elapsed_time)):
        elapsed_time[i]=elapsed_time[i].days

    df["elapsed_days"] = elapsed_time
    return df


def plot_daily_chat(df, color):
    days_count_dict = dict(df.elapsed_days.value_counts())
    day = sorted(days_count_dict.keys())
    msj_count = [days_count_dict[i] for i in day]
    plt.figure(figsize=(15,4))
    plt.plot(list(day), np.array(msj_count).flatten(), color = color, ms = 2, label = other)

    plt.title("Chats por día a lo largo de los años desde el "+ str(df.day[0])+ "/" + str(df.month[0]) + "/" + str(df.year[0]))
    plt.ylabel("message count")
    plt.xlabel("year")
    days_primer_año= days_until_first_next_year(df)

    ticks = [days_primer_año - 365, days_primer_año]
    a = 0
    for i in range(len(df.year.unique())-2):
        a += 365        
        ticks.append(days_primer_año + a)

    labels = df.year.unique()

    plt.xticks(ticks = ticks, labels = labels)
    plt.legend(prop={'size': 13});
    
def days_until_first_next_year(df):
    """Sirve para armar el vector de labels, más que nada, en el gráfico de dias"""
    for i in range(len(df.year)):
        if df.year[i] != df.year.unique()[0]:
            return df.elapsed_days[i]


def remove_name_from_msj(me, other, df):
    msjs = []
    for i in df.msj: 
        if i[0:len(me)] == me:
            msjs.append(i[len(me) +2:])
        if i[0:len(other)] == other:
            msjs.append(i[len(other) +2:])

    df.msj = msjs
    return df

def emoji_count(df):
    emojis = ["😀", "😃", "😁","😅","😉","🥰","😍","😘","😋","😜","🤗",
              "🤐","😏","😬","😒", "🥵","😎","🙁", "😲", "😳","🥺", "😰",
              "😥","😭","😓","😤","👻", "💚","❤","🖤","💥","👋","👌","✌","🤟","🤙","👍",
             "👏","💪","👀","🤔","🙄"]

    emojis_dict = {}

    for emoji in emojis:
        emojis_dict[emoji] = 0

    for emoji in emojis_dict:
        for men in df.msj:
            if emoji in men:
                emojis_dict[emoji] += 1
                
    emojis_dict = {k: v for k, v in sorted(emojis_dict.items(), key=lambda item: item[1])}

    pd.DataFrame(emojis_dict, index = range(1)).to_json(str("emojis_with_"+other+".json"))
    


def plot_word_cloud(word_count):
        # Generate a word cloud image
    word_count_filtered = word_count.copy()
    for key in word_count:
        if len(key) < 5:
            del word_count_filtered[key]

    wordcloud = WordCloud(max_font_size=200, max_words=200, background_color="white", height= 920, width = 1080).generate_from_frequencies(word_count_filtered)
    wordcloud.to_file("wordcloud_plot_" + other + ".jpg")
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title("Top 200 palabras más usadas con "+ other, fontsize=15, color = "grey")
    plt.axis("off")
    

def plot_author_pie(df):

    pieLabels = [me, other]
    mine = df.written_by_me.value_counts()[True]
    others = df.written_by_me.value_counts()[False]

    my_perc = mine / (mine + others) *100
    others_perc = 100 - my_perc

    share = [my_perc, others_perc]

    textprops = {"color":"white","fontname":"serif", "weight":"light","size":"small"}

    plt.pie(share, colors = ["grey", color], labels= pieLabels, autopct = "%1.1f", labeldistance= 1.1, textprops = textprops)

    plt.title("Porcentaje de mensajes enviados por cada usuario", size = 10)

def add_msj_writer_groups(df, others):
    """Agrega una columna para cada mensaje"""
    written_by_me = []
    for mensaje in df.msj:
        if mensaje[0:len(me)] == me:
            written_by_me.append(True)
        else:
            written_by_me.append(False)

    df[str("written_by_"+ me)] = written_by_me

    
    for other in others: 
        written_by_other = []
        for mensaje in df.msj:
            if mensaje[0:len(other)] == other:
                written_by_other.append(True)
            else:
                written_by_other.append(False)

        df[str("written_by_"+ other)] = written_by_other
        
    return df


def plot_daily_chat_group(df, color):
    days_count_dict = dict(df.elapsed_days.value_counts())
    day = sorted(days_count_dict.keys())
    msj_count = [days_count_dict[i] for i in day]
    plt.figure(figsize=(15,4))
    plt.plot(list(day), np.array(msj_count).flatten(), color = color, ms = 2, label = filename[:-4])

    plt.title("Chats por día a lo largo de los años desde el "+ str(df.day[0])+ "/" + str(df.month[0]) + "/" + str(df.year[0]))
    plt.ylabel("message count")
    plt.xlabel("year")
    days_primer_año= days_until_first_next_year(df)

    ticks = [days_primer_año - 365, days_primer_año]
    a = 0
    for i in range(len(df.year.unique())-2):
        a += 365        
        ticks.append(days_primer_año + a)

    labels = df.year.unique()

    plt.xticks(ticks = ticks, labels = labels)
    plt.legend(prop={'size': 13});
    
def days_until_first_next_year(df):
    """Sirve para armar el vector de labels, más que nada, en el gráfico de dias"""
    for i in range(len(df.year)):
        if df.year[i] != df.year.unique()[0]:
            return df.elapsed_days[i]



def plot_daily_chat_moving_average(df, color, n = 7):

    days_count_dict = dict(df.elapsed_days.value_counts())
    for i in range(df.elapsed_days.max()):
        if i in days_count_dict:
            continue
        else:
            days_count_dict[i] = 0
    day = sorted(days_count_dict.keys())
    msj_count = [days_count_dict[i] for i in day]
    plt.figure(figsize=(15,4))
    
    values_to_plot = np.array(msj_count)
    N = n
    cumsum, moving_aves = [0], []
    for i, x in enumerate(values_to_plot, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
        else:
            moving_aves.append(i)
    
    plt.plot(list(day), moving_aves, color = color, ms = 2, label = other)

    plt.title("Chats por día a lo largo de los años desde el "+ str(df.day[0])+ "/" + str(df.month[0]) + "/" + str(df.year[0]))
    plt.ylabel("message count")
    plt.xlabel("year")
    days_primer_año= days_until_first_next_year(df)

    ticks = [days_primer_año - 365, days_primer_año]
    a = 0
    for i in range(len(df.year.unique())-2):
        a += 365        
        ticks.append(days_primer_año + a)

    labels = df.year.unique()

    plt.xticks(ticks = ticks, labels = labels)
    plt.legend(prop={'size': 13});


def countplotting_group(df, column, color):
    """Hace el barplot de la columna deseada del DF"""
    seaborn.countplot(x=column, data=df, color= color)
    plt.ylabel("messages count")
    plt.title(str("Mensajes según "+column+" con " + filename[:-4].replace("_"," ")))
    plt.xlabel(column)



def remove_names_for_wordcloud(others, word_count,me):
    otros = others + [me]
    to_delete = [a.split(" ") for a in otros]
    to_delete = [item for sublist in to_delete for item in sublist]
    to_delete = [a.lower() for a in to_delete]
    for a in to_delete:
        if a in word_count:
            del word_count[a]
    return word_count


def plot_msj_count_group(df, color, solo_nombre):

    cantidad_de_msjs = {}
    for i in df.columns[2:-5]:
        cantidad_de_msjs[i] = df[i].value_counts()[True]

    D= cantidad_de_msjs

    D = {k: v for k, v in sorted(D.items(), key=lambda item: item[1])}

    plt.bar(range(len(D)), list(D.values()), align='center', color = color)


    if solo_nombre == True:
        labels = [name[11:].split(" ")[0] for name in D.keys()]
        plt.title("Cantidad de mensajes por miembro del grupo " + filename[:-4].replace("_"," "), fontsize = 10)
        plt.ylabel("Cantidad de mensajes enviados")
        plt.xticks(range(len(D)), list(labels), rotation = 90, fontsize=8);
    else:
        labels = [name[11:] for name in D.keys()]
        plt.title("Cantidad de mensajes por miembro del grupo " + filename[:-4].replace("_"," "), fontsize = 10)
        plt.ylabel("Cantidad de mensajes enviados")
        plt.xticks(range(len(D)), list(labels), rotation = 90, fontsize=8);


def plot_word_cloud_group(word_count):
        # Generate a word cloud image
    word_count_filtered = word_count.copy()
    for key in word_count:
        if len(key) < 5:
            del word_count_filtered[key]

    wordcloud = WordCloud(max_font_size=200, max_words=200, background_color="white", height= 920, width = 1080).generate_from_frequencies(word_count_filtered)
    wordcloud.to_file("wordcloud_plot_" + filename[:-4] + ".jpg")
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title("Top 200 palabras más usadas con "+ filename[:-4].replace("_"," "), fontsize=15, color = "grey")
    plt.axis("off")
    

def filter_msj_group(df):
    remove_indexes = []
    for i in range(len(df)):
        suma =  df.iloc[i,2:].sum()

        if suma == False:
            remove_indexes.append(i)
    
    remove_indexes.reverse()
    for index in remove_indexes:
        df = df.drop(df.index[index])
    
    return df








