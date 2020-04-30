filename = "LPB.txt"
color  = "darkred"
me = "Santiago Olszevicki" 

others = ["Mauro","Lorant", "Oco", "Manuel Buchas", "Nacho Pintes", "Diegui Gonzalez"]




# TODO AUTOMATICO #

file_stripped = read_file(filename)
df = create_df(file_stripped)
df = add_msj_writer_groups(df, others)
df = df.set_index(np.array(range(len(df))))
df = filter_msj_group(df)
df = df.set_index(np.array(range(len(df))))
df = split_date(df)
df = df.set_index(np.array(range(len(df))))

df = add_elapsed_days(df)

word_count = count_words(df)
df.set_index(np.array(range(len(df))))


plot_daily_chat_group_moving_average(df, color = color, n = 7)
plt.savefig(str("daily_plot_" + filename[:-4] + ".jpg"),dpi=400)
plt.close()


countplotting_group(df, "hour", color)
plt.savefig(str("hour_count_plot_" + filename[:-4] + ".jpg"),dpi=400)
plt.close()

countplotting_group(df, "year", color)
plt.savefig(str("year_count_plot_" + filename[:-4]  + ".jpg"),dpi=400)
plt.close()

word_count = remove_names_for_wordcloud(others, word_count,me)
plot_word_cloud_group(word_count)
plt.savefig(str("wordcloud_plot_" + filename[:-4] + ".jpg"),dpi=400) #Ya lo guarda la función
plt.close()

plot_msj_count_group(df, color, solo_nombre=False)
plt.savefig(str("msj_count_plot_" + filename[:-4] + ".jpg"),dpi=400, bbox_inches='tight')
plt.close()

countplotting_group(df, "month", color)
plt.savefig(str("month_count_plot_" + filename[:-4] + ".jpg"),dpi=400)
plt.close()
