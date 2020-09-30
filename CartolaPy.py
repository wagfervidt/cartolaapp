#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[1]:


import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.stats as stats


# # Carregar tabelas

# In[2]:


# Carrega informações de todas as tabelas, menos a 'GERAL.csv'
def load_attributes(inputPath):
    df = pd.read_csv(inputPath, header=0, index_col=0)
    return df

# Carrega 'GERAL.csv'
def load_geral(inputPath):
    df = pd.read_csv(inputPath, header=0, index_col=1)
    return df


# # Visão Detalhada - Jogador

# In[3]:


def jogadores(df, pts_time, jogs, key):
    # Itera por todos os jogadores selecionados
    for j in jogs:
        # Interface - Jogador
        st.header(j)
        st.dataframe(df.loc[j, 'Posição':'Preço'].to_frame().T)
        # Intervalo de Rodadas
        value = st.slider('Selecione um intervalo de rodadas',
                          1, 11, (1, 11), key=str(key))

        # Pontuações - Informações Gerais
        pts = pts_time.loc[j, str(value[0]):str(value[1])]
        sum_pts = np.sum(pts)
        df.loc[j, 'Pontuação Total'] = float("{:.1f}".format(sum_pts))
        mean_pts = np.mean(pts[pts != 0]) if len(pts[pts != 0]) > 0 else 0
        partidas = np.count_nonzero(pts)
        df.loc[j, 'Partidas'] = float("{:.0f}".format(partidas))
        df.loc[j, 'Média'] = float("{:.2f}".format(mean_pts))
        df.loc[j, 'Média por C$'] = float("{:.2f}".format(
            mean_pts/df.loc[j, 'Preço']))
        std_pts = np.std(pts[pts != 0])
        
        st.table(df.loc[j, 'Pontuação Total':'Média por C$'].to_frame().T)

        # O jogador não disputou nenhuma partida no intervalo
        if sum_pts == 0:
            st.write(
                '**Ops!** O jogador não disputou nenhuma partida nesse intervalo de rodadas.'
                ' Para visualizar seus gráficos, tente outro intervalo.')
        else:
            # Pontuações - CheckBox
            pts_check = st.checkbox(
                'Pontuação na rodada '+str(value[0]), key=str(key), value=True) if value[0] == value[1] else st.checkbox(
                'Pontuações da ' + str(value[0])+'ª à '+str(value[1])+'ª rodada', key=str(key), value=True)
            if pts_check:
                pts_frame = pts.to_frame()
                ax = pts_frame.plot.bar(rot=0, color=np.where(
                    pts_frame.values > 0, 'tab:green', 'tab:red').T, legend=None)

                for p in ax.patches:
                    ax.annotate("{:.1f}".format(p.get_height()), (p.get_x()+p.get_width()/2, p.get_height()),
                                (0, 1), textcoords='offset points', ha='center', va='bottom')
                st.pyplot()

            # Distribuição Normal - CheckBox
            if value[0] != value[1] and len(pts[pts != 0]) > 1:
                dn_check = st.checkbox('Distribuição dos pontos da ' +
                                       str(value[0])+'ª à '+str(value[1])+'ª rodada', key=str(key), value=True)
                if dn_check:
                    pts_sorted = sorted(pts[pts != 0])
                    x = np.linspace(pts_sorted[0], pts_sorted[-1], 1000)
                    y = stats.norm.pdf(x, mean_pts, std_pts)
                    plt.plot(x, y, color='black')
                    pt1 = mean_pts+std_pts
                    pt2 = mean_pts-std_pts
                    plt.plot([pt1, pt1], [np.amin(y), stats.norm.pdf(
                        pt1, mean_pts, std_pts)], color='black')
                    plt.plot([pt2, pt2], [np.amin(y), stats.norm.pdf(
                        pt2, mean_pts, std_pts)], color='black')
                    ptx = np.linspace(pt1, pt2, 10)
                    pty1 = stats.norm.pdf(ptx, mean_pts, std_pts)
                    pty2 = np.amin(y)
                    plt.fill_between(
                        ptx, pty1, pty2, color='#89bedc', alpha=1.0)
                    plt.grid()
                    blue_patch = mpatches.Patch(
                        color='#89bedc', label='Região de maior probabilidade de pontuação')
                    plt.legend(handles=[blue_patch], loc='upper right', bbox_to_anchor=(
                        0., 1.02, 1., .102), borderaxespad=0.)
                    plt.xlabel('Pontuações')
                    plt.yticks([])
                    st.pyplot()
            else:
                st.write(
                    '**Ops!** Para visualizar a distribuição de pontuações, ' +
                    'o jogador precisa ter disputado ao menos duas partidas no intervalo selecionado.')
        key += 1


# # Visão Detalhada - Time

# In[4]:


def time(sigla, key):
    df = load_attributes('times/'+sigla+'.csv')
    pts = load_attributes('times/'+sigla+'_PTS.csv')
    
    # Interface - Time
    titles = {
        'CAP': 'Athletico-PR', 'ACG': 'Atlético-GO',
        'CAM': 'Atlético-MG', 'BAH': 'Bahia',
        'BOT': 'Botafogo', 'CEA': 'Ceará',
        'COR': 'Corinthians', 'CTB': 'Coritiba',
        'FLA': 'Flamengo', 'FLU': 'Fluminense',
        'FOR': 'Fortaleza', 'GOI': 'Goiás',
        'GRE': 'Grêmio', 'INT': 'Internacional',
        'PAL': 'Palmeiras', 'RBB': 'Red Bull Bragantino',
        'SAN': 'Santos', 'SAO': 'São Paulo',
        'SPO': 'Sport', 'VAS': 'Vasco'
    }
    
    multis = {
        'CAP': 'Escolha os jogadores do Athletico-PR', 
        'ACG': 'Escolha os jogadores do Atlético-GO',
        'CAM': 'Escolha os jogadores do Atlético-MG', 
        'BAH': 'Escolha os jogadores do Bahia',
        'BOT': 'Escolha os jogadores do Botafogo',
        'CEA': 'Escolha os jogadores do Ceará',
        'COR': 'Escolha os jogadores do Corinthians',
        'CTB': 'Escolha os jogadores do Coritiba',
        'FLA': 'Escolha os jogadores do Flamengo',
        'FLU': 'Escolha os jogadores do Fluminense',
        'FOR': 'Escolha os jogadores do Fortaleza',
        'GOI': 'Escolha os jogadores do Goiás',
        'GRE': 'Escolha os jogadores do Grêmio',
        'INT': 'Escolha os jogadores do Internacional',
        'PAL': 'Escolha os jogadores do Palmeiras',
        'RBB': 'Escolha os jogadores do Red Bull Bragantino',
        'SAN': 'Escolha os jogadores do Santos',
        'SAO': 'Escolha os jogadores do São Paulo',
        'SPO': 'Escolha os jogadores do Sport',
        'VAS': 'Escolha os jogadores do Vasco'
    }
    st.title(titles[sigla])
    jogs = st.multiselect(multis[sigla], df.index)
    jogadores(df, pts, jogs, key)


# # Main

# In[5]:


st.sidebar.markdown("<h1 style='text-align: center;'><span style='color: #000000'>"
                    "Cartola</span><span style='color: #ff6600'>Py</span></hi>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>"
                    "Estatísticas para você mitar à vontade!</p>", unsafe_allow_html=True)
st.sidebar.info('Última Atualização: 24/09/20')
st.sidebar.header('Menu')
op = st.sidebar.selectbox('', ('Visão Geral', 'Visão Detalhada'), index=0)


# # Visão Geral

# In[10]:


if op == 'Visão Geral':
    st.markdown("<p style='text-align: justify;'>"
                "Para ordenar os jogadores conforme determinada estatística,"
                " clique no nome da <b>coluna</b> que você deseja ordenar na tabela."
                " Você pode ordenar de forma <b>ascendente</b> (1 clique) ou"
                " de forma <b>descendente</b> (2 cliques).</p>", unsafe_allow_html=True)
    st.markdown(
        'Amplie a tabela clicando no ícone de **expansão** no seu canto superior direito.')
    st.title('')

    # Carrega Informações
    df = load_geral("geral/GERAL.csv")
    pts = load_attributes("geral/GERAL_PTS.csv")
    # Intervalo de Rodadas
    value = st.slider('Selecione um intervalo de rodadas', 1, 11, (1, 11))

    # Filtro por Posição
    pos = st.selectbox('Filtro por Posição', ('Geral', 'Goleiro',
                                              'Lateral', 'Zagueiro', 'Meia', 'Atacante'))

    # Pontuações - Informações Gerais
    pts_df = pts.loc[:, str(value[0]):str(value[1])]
    sum_pts = np.sum(np.array(pts_df), axis=1, keepdims=True)
    df.loc[:, 'Pontuação Total'] = [pt for pt in sum_pts]
    partidas = np.count_nonzero(np.array(pts_df), axis=1, keepdims=True)
    df.loc[:, 'Partidas'] = [ptd for ptd in partidas]
    mean_pts = np.nanmean(np.array(pts_df[pts_df != 0]), axis=1, keepdims=True)
    df.loc[:, 'Média'] = [pt for pt in mean_pts]
    mean_pts = np.squeeze(mean_pts)
    df.loc[:, 'Média por C$'] = [pt for pt in mean_pts/df.loc[:, 'Preço']]

    # Constroi o Dataframe com filtros
    # Não mostra os jogadores que não atuaram no intervalo de rodadas
    df = df[df['Partidas']!=0]
    df = df[df['Partidas'].notna()]
    
    # Filtro por posição
    filtro_pos = {
        'Geral': df,
        'Goleiro': df.loc[df['Posição'] == 'G'],
        'Lateral': df.loc[df['Posição'] == 'L'],
        'Zagueiro': df.loc[df['Posição'] == 'Z'],
        'Meia': df.loc[df['Posição'] == 'M'],
        'Atacante': df.loc[df['Posição'] == 'A']
    }
    df = filtro_pos[pos]
    
    # Plot
    plt_df = df.sort_values(by=['Preço'], ascending=False).reset_index().style
    for j in df.columns[3:]:
        plt_df = plt_df.background_gradient(
            cmap='RdYlGn', subset=pd.IndexSlice[:, [j]])

    plt_df.format({'Preço': '{:.2f}', 'Pontuação Total': '{:.1f}',
                   'Partidas': '{:.0f}', 'Média': '{:.2f}', 'Média por C$': '{:.2f}'})
    st.dataframe(plt_df)

    # ColorBar
    st.markdown("<p style='text-align: center;'><b>Qualidade do jogador na estatística</b></p>",
                unsafe_allow_html=True)
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    fig, ax = plt.subplots(figsize=(20, 1))
    ax.imshow(gradient, aspect='auto', cmap='RdYlGn')
    ax.set_axis_off()
    pos = list(ax.get_position().bounds)
    x_text = pos[0] + 0.125
    y_text = pos[1] + pos[3]/2.
    fig.text(x_text, y_text, 'Ruim', va='center', ha='center', fontsize=30)
    x_text = (pos[0] + 0.125 + pos[2])/2
    y_text = pos[1] + pos[3]/2.
    fig.text(x_text, y_text, 'Na Média', va='center', ha='center', fontsize=30)
    x_text = pos[2]
    y_text = pos[1] + pos[3]/2.
    fig.text(x_text, y_text, 'Bom', va='center', ha='center', fontsize=30)
    st.pyplot()

    # Copyright
    st.write('---')
    st.write('Autor: **Túlio Souza**')
    st.write(
        '[Github](https://github.com/tuliosouza99/CartolaPy)')
    st.write('')


# # Call Visão Detalhada

# In[8]:


if op == 'Visão Detalhada':
    time_op = st.sidebar.selectbox(
        'Escolha um Time', ('', 'Athletico-PR', 'Atlético-GO', 'Atlético-MG', 'Bahia',
                            'Botafogo', 'Ceará', 'Corinthians', 'Coritiba',
                            'Flamengo', 'Fluminense', 'Fortaleza', 'Goiás',
                            'Grêmio', 'Internacional', 'Palmeiras', 'Red Bull Bragantino',
                            'Santos', 'São Paulo', 'Sport', 'Vasco'))

    time2siglakey = {
        'Athletico-PR': ('CAP', 0), 'Atlético-GO': ('ACG', 50),
        'Atlético-MG': ('CAM', 100), 'Bahia': ('BAH', 150),
        'Botafogo': ('BOT', 200), 'Ceará': ('CEA', 250),
        'Corinthians': ('COR', 300), 'Coritiba': ('CTB', 350),
        'Flamengo': ('FLA', 400), 'Fluminense': ('FLU', 450),
        'Fortaleza': ('FOR', 500), 'Goiás': ('GOI', 550),
        'Grêmio': ('GRE', 600), 'Internacional': ('INT', 650),
        'Palmeiras': ('PAL', 700), 'Red Bull Bragantino': ('RBB', 750),
        'Santos': ('SAN', 800), 'São Paulo': ('SAO', 850),
        'Sport': ('SPO', 900), 'Vasco': ('VAS', 950)
    }

    if time_op != '':
        sigla, key = time2siglakey[time_op]
        time(sigla, key)
    else:
        st.markdown("<p style='text-align: justify;'>"
                    "<b>Tenha acesso a estatísticas únicas para mitar no Cartola"
                    " com apenas dois passos!</b></p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: justify;'>"
                    "<b>1.</b> Clique na caixa <b>'Escolha um time'</b> no Menu"
                    " e selecione uma equipe.</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: justify;'>"
                    "<b>2.</b> Depois, é só escolher quantos e quais jogadores você quiser desse time para"
                    " analisar seus dados e gráficos de forma detalhada!</p>", unsafe_allow_html=True)


# # Converte para .py

# In[9]:


