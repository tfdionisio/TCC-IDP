import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# ==============================
# CONFIGURAÇÃO INICIAL
# ==============================

st.title("As novas fronteiras do Brasil em movimento")
st.subheader("Enquanto o país se divide entre quem chega, quem sai e quem volta, os números do Censo revelam um Brasil que se reconstrói em silêncio, dentro e fora de si mesmo.")

pasta = "./"

# Imagem de capa
caminho_imagem = os.path.join(pasta, "20220913_migracao_interna.jpg")
st.image(caminho_imagem)

# Introdução
st.write( "Nos últimos doze anos, o Brasil mudou de lugar. Ou melhor: os brasileiros mudaram dentro dele. Cruzaram fronteiras invisíveis entre estados, levaram sotaques e memórias em viagens que, somadas, redesenharam o mapa humano do país. Santa Catarina, que por décadas foi destino de europeus, hoje é o endereço de milhares de brasileiros em busca de emprego, segurança e sossego. Goiás e Mato Grosso, antes vistos como passagem, viraram ponto de chegada. Já o Rio de Janeiro e o Distrito Federal, antigos polos de atração, vivem o efeito contrário, o êxodo silencioso de quem busca recomeçar em outro canto.")
st.write( "Aqui entra aspas de personagem migrante interno:  alguém que deixou o Rio ou DF e se mudou para o Sul ou Centro-Oeste, explicando os motivos e as mudanças na rotina.")
st.write ("De acordo com os dados do Censo 2022, compilados e analisados pelo IBGE, mais de 4,6 milhões de brasileiros mudaram de estado entre 2017 e 2022. A movimentação revela um país em redistribuição interna, guiado por oportunidades econômicas, qualidade de vida e custos mais baixos.")


# ==============================
# TABELA 1 - SALDO MIGRATÓRIO
# ==============================

caminho_saldo = os.path.join(pasta, "saldo_migratorio_estados.csv")
df_saldo = pd.read_csv(caminho_saldo)

# Limpeza
df_saldo = df_saldo[df_saldo['uf'] != 'BR']
df_saldo = df_saldo.loc[:, ~df_saldo.columns.str.contains('^Unnamed')]
df_saldo['taxa_migra'] = df_saldo['taxa_migra'].str.replace("%", "").str.replace(",", ".")
df_saldo['taxa_migra'] = pd.to_numeric(df_saldo["taxa_migra"]) / 100

# Exibição direta
st.subheader("Saldo migratório brasileiro (Censo 2022)")
st.dataframe(df_saldo)

st.write ("Santa Catarina é o caso mais emblemático. O estado registrou um saldo migratório positivo de 354 mil pessoas, o equivalente a quase 5% da população atual, o maior do país. Em segundo lugar vêm Goiás (+186 mil) e Mato Grosso (+103 mil), impulsionados pela expansão do agronegócio e da construção civil. A Paraíba aparece como exceção nordestina com saldo positivo (+30 mil), enquanto o Rio de Janeiro (-165 mil) e o Distrito Federal (-99 mil) estão entre os que mais perderam moradores.")
st.write ("Aqui entra aspas de especialista 1: demógrafo ou geógrafo especializado em mobilidade populacional, por exemplo, José Eustáquio Diniz Alves ou Tânia Lago, explicando o que motiva o saldo migratório interno, o papel da economia regional e a fuga de grandes centros caros.")

st.subheader ("O novo eixo migratório")

# Mapa interativo
fig = px.choropleth(
    df_saldo,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="uf",
    color="taxa_migra",
    color_continuous_scale=["#c90000", "#ffffff", "#1E0FF0"],
    featureidkey="properties.sigla",
    projection="mercator",
    title="Saldo migratório por estado (Censo 2022)",
    hover_data={"taxa_migra": ":.2%", "imigrantes": ":,", "emigrantes": ":,", "saldo_migratorio": ":,", "uf": True}
)
fig.update_geos(fitbounds="locations", visible=False, bgcolor="#0e1117")
fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0},
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    geo=dict(bgcolor="#0e1117")
)
st.plotly_chart(fig, config={"responsive": True})
# ==============================
# TABELA 2 - POPULAÇÃO MIGRANTE
# ==============================

caminho_pop = os.path.join(pasta, "pop_migrantes.csv")
df_pop = pd.read_csv(caminho_pop)

st.subheader("Estados que mais receberam migrantes e suas origens")
st.dataframe(df_pop)


st.write("Se antes a migração brasileira tinha um destino óbvio, São Paulo, agora as rotas se multiplicam. Os dados do IBGE mostram que Santa Catarina e Paraná formam um “novo eixo migratório”, atraindo moradores de 13 estados diferentes, do Acre ao Pará, de Sergipe a Roraima.")
st.write("O fenômeno tem razões práticas e simbólicas: segurança pública, empregos industriais e uma narrativa de prosperidade que circula nas redes e nas conversas. Cidades como Itajaí, Joinville e Florianópolis viraram o ideal de “vida estável”, principalmente para famílias jovens.")
st.write("A jornalista Laura Machado, de 27 anos, faz parte desse movimento recente. Natural de Macapá (AP), ela se mudou para a capital catarinense em 2023 em busca de melhores oportunidades de trabalho e qualidade de vida. Meses antes da mudança, havia visitado a cidade e se encantado com a paisagem, o ritmo mais tranquilo e as opções de lazer.")
st.write("Embora reconheça que São Paulo concentra mais oportunidades no jornalismo, Laura nunca se imaginou morando lá e acredita que Florianópolis se encaixou melhor em suas expectativas.")
st.write("A mudança, porém, trouxe desafios. Laura conta que os salários são um pouco mais altos do que em sua cidade de origem, mas o custo de vida — sobretudo com moradia — é elevado. Segundo ela, as opções mais acessíveis costumam ficar distantes ou em condições precárias. Ainda assim, destaca que a sensação de segurança compensa parte das dificuldades")
st.write("“Me sinto mais segura aqui, mais tranquila para andar sozinha nas ruas, com menos medo de assaltos e furtos”, destaca. ")
st.write("Enquanto isso, o Centro-Oeste emerge como nova fronteira demográfica. Goiás, por exemplo, recebe 41% de seus migrantes vindos de Minas Gerais e quase 11% do Distrito Federal, reflexo do “transbordamento” da capital federal, que perdeu população para as cidades vizinhas mais baratas e conectadas. Mato Grosso e Mato Grosso do Sul também aparecem no topo, alimentados pela expansão agrícola, pela indústria de alimentos e pela migração de trabalhadores qualificados.")


# ==============================
# TABELA 1.1 - POPULAÇÃO NATIVA
# ==============================

st.subheader("População nativa por região (Censo 2022)")
st.write ("Os números mostram que, por mais que o Brasil se mova, parte dele permanece fortemente enraizada. O Nordeste é a região mais “nativa” do país, 96,6% dos nordestinos vivem em sua própria região. Isso é acompanhado de um fenômeno novo: a migração de retorno. Estados como Paraíba e Ceará passaram a atrair antigos emigrantes, aposentados, empreendedores e famílias que decidiram voltar após anos em outras regiões. ")
# Criar DataFrame
df_nativos = pd.DataFrame({
    "População nativa": [
        "Nordestinos que moram no Nordeste",
        "Sulistas que moram no Sul",
        "Sudestinos que moram no Sudeste",
        "Nortistas que moram no Norte",
        "Centro-oestinos que moram no Centro-Oeste"
    ],
    "Porcentagem": [96.6, 91.9, 88.7, 87.0, 73.4]
})

st.dataframe(df_nativos, use_container_width=True, hide_index=True)

st.write("Para o professor Carlos de Almeida Toledo, do Departamento de Geografia da FFLCH/USP, o fenômeno da migração de retorno se deve, junto a outros fatores, ao desenvolvimento econômico das cidades nordestinas. “Na segunda metade do século XX, muitas pessoas deixaram o Nordeste em busca de oportunidades de emprego em outras regiões do país, especialmente no Sudeste. Com o avanço da modernização, impulsionado pela migração rural-urbana, pelo crescimento econômico e pela chegada de programas como o Luz para Todos e a ampliação da telefonia, as pequenas cidades nordestinas começaram a se transformar. A melhoria da infraestrutura e da qualidade de vida abriu espaço para o fenômeno da migração de retorno, com muitas famílias voltando à região em busca de novas oportunidades ou apenas uma vida mais estável.” Concluiu.")
st.write("Aspas de personagem que voltou do Sudeste para o Nordeste, explicando por que retornou, custo de vida, família, ritmo de vida, etc.")
st.write("Já o Centro-Oeste é o inverso: a região mais cosmopolita do país. Quase 27% de seus moradores nasceram fora dali. No topo está o Distrito Federal, onde quase metade da população é de origem goiana. O crescimento urbano de Goiânia, Cuiabá e Campo Grande revela um Brasil interiorizado, que agora disputa protagonismo com o litoral.")



# ==============================
# TABELA 3 - MATRIZ DE MIGRAÇÃO (NASCIMENTO x RESIDÊNCIA)
# ==============================
st.subheader("Compreendendo o fluxo com uma Matriz de Confusão ")

st.write ("O Fluxo migratório leva em consideração o local de nascimento e o local de nascimento das populações das cinco regiões brasileiras. Na matriz, que apresenta somente os 19,6 milhões de migrantes brasileiros, conseguimos verificar que quase 10 milhões de nordestinos deixaram o Nordeste nas últimas décadas, a maioria rumo ao Sudeste (6,7 milhões) e ao Centro-Oeste (1,8 milhão).")


# Carregar dados de migração
caminho_matriz = os.path.join(pasta, "pop_migrantes_rodolfo.csv")
df_migracao = pd.read_csv(caminho_matriz)

# Criar matriz pivot
matriz = df_migracao.pivot(index='local_nasc', columns='local_resid', values='pop')

# Ordem das regiões
ordem_regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
matriz = matriz.reindex(index=ordem_regioes, columns=ordem_regioes)

# Calcular percentuais por linha (onde os nascidos em cada região migraram)
matriz_pct = matriz.div(matriz.sum(axis=1), axis=0) * 100

# Criar texto para exibir nas células (percentual + população)
text_display = []
for i in range(len(matriz)):
    row_text = []
    for j in range(len(matriz.columns)):
        pop_val = int(matriz.iloc[i, j]) if not pd.isna(matriz.iloc[i, j]) else 0
        pct_val = matriz_pct.iloc[i, j] if not pd.isna(matriz_pct.iloc[i, j]) else 0

        if pop_val == 0:
            row_text.append("—")
        else:
            row_text.append(f"{pct_val:.1f}%<br>{pop_val:,}".replace(",", "."))
    text_display.append(row_text)

# Criar heatmap de confusão
fig = go.Figure(data=go.Heatmap(
    z=matriz.values,
    x=matriz.columns,
    y=matriz.index,
    colorscale='rdpu',
    text=text_display,
    texttemplate="%{text}",
    textfont={
        "family": "Sora, Medium",
        "size": 11,
        "color": "#000000"
    },
    hovertemplate='<b>Nascimento:</b> %{y}<br><b>Residência:</b> %{x}<br><b>População:</b> %{z:,.0f}<extra></extra>',
    colorbar=dict(
        title=dict(
            text="População",
            font={"family": "Sora, Medium", "size": 14, "color": "#f5f5f5"}
        ),
        tickfont={"family": "Sora, Medium", "size": 12, "color": "#f5f5f5"}
    )
))

fig.update_layout(
    title="Matriz de Confusão - Fluxo Migratório por Região de Nascimento e Residência",
    title_font={"family": "Sora, Medium", "size": 18, "color": "#f5f5f5"},
    xaxis_title="Local de Residência Atual",
    yaxis_title="Local de Nascimento",
    xaxis_title_font={"family": "Sora, Medium", "size": 16, "color": "#f5f5f5"},
    yaxis_title_font={"family": "Sora, Medium", "size": 16, "color": "#f5f5f5"},
    xaxis_tickfont={"family": "Sora, Medium", "size": 14, "color": "#f5f5f5"},
    yaxis_tickfont={"family": "Sora, Medium", "size": 14, "color": "#f5f5f5"},
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    height=600,
)

st.plotly_chart(fig, config={"responsive": True})

# Adicionar explicação em um botão expansível
with st.expander("❓ Não entendeu a matriz? Clique aqui para mais detalhes:"):
    st.write("- **Diagonal (—)**: Representa a própria região (migrantes não computados)")
    st.write("- **Percentuais**: Proporção de nascidos em cada região que migraram para outras")
    st.write("- **Valores absolutos**: População total que migrou entre as regiões")


st.subheader ("O Brasil que fica e o que chega")
st.write ("INSERIR TABELA COM OS IMIGRANTES POR NACIONALIDADE")
st.write ("Enquanto o país se movimenta internamente, estrangeiros também voltaram a escolher o Brasil.Depois de décadas de retração migratória, o número de imigrantes e naturalizados quase dobrou entre 2010 e 2022, saltando de 592 mil para mais de 1 milhão.")
st.write ("Mas o perfil mudou completamente: menos europeus e asiáticos, mais latino-americanos e africanos. A América Latina e o Caribe são hoje o epicentro da nova imigração, representando 64% de todos os estrangeiros no país. A Venezuela lidera o ranking: de 2.869 pessoas em 2010 para 271 mil em 2022, um aumento de mais de 9.000%. Em seguida vêm Haiti, Bolívia, Colômbia e Paraguai.")
st.write ("(Aqui entra aspas de especialista 2: sociólogo ou antropólogo especializado em migração internacional, por exemplo, Rosana Baeninger ou João Carlos Jarochinski Silva, explicando o novo perfil das comunidades estrangeiras no Brasil, a Operação Acolhida e a integração desses grupos.")
st.write ("O refúgio humanitário substituiu o antigo modelo de imigração de trabalho. Venezuelanos, haitianos e colombianos chegam em busca de proteção, estudo e recomeço, concentrando-se em cidades do Norte e Sudeste. Enquanto isso, portugueses, italianos e espanhóis reduziram presença: a imigração europeia caiu 23% no período, e muitos se naturalizaram ou retornaram a seus países de origem.")
st.write ("Entre os que escolheram o Brasil para estudar está o geógrafo haitiano Wisnel Joseph, apresentador do podcast O Haiti também é aqui. Ele vive no país há sete anos e veio para o país para cursar mestrado em sua área de formação. Defendeu a dissertação em fevereiro de 2020, pouco antes do início da pandemia, e decidiu permanecer. Hoje, cursa o doutorado e diz estar satisfeito com o caminho que construiu no país.")
st.write ("“A vida por aqui tem sido tranquila. Estou feliz por ter essa oportunidade de fazer meus estudos superiores. Agora estou focado em concluir o doutorado”, conta.")


# ==============================
# OBSERVAÇÕES FINAIS
# ==============================

## Para visualizar no navegador: "streamlit run streamlitidp.py" no terminal
