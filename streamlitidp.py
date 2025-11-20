import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

pasta = "./"

# ---------------------------------------------------------------
# CARREGAMENTO DO CSV
# ---------------------------------------------------------------
caminho_saldo = os.path.join(pasta, "saldo_migratorio_estados.csv")
df_saldo = pd.read_csv(caminho_saldo)
df_saldo = df_saldo[df_saldo['uf'] != 'BR']
df_saldo = df_saldo.loc[:, ~df_saldo.columns.str.contains('^Unnamed')]
df_saldo['taxa_migra'] = df_saldo['taxa_migra'].str.replace("%", "").str.replace(",", ".")
df_saldo['taxa_migra'] = pd.to_numeric(df_saldo["taxa_migra"]) / 100
nomes_estados = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

st.write("Por Kelly Ribeiro, Renata Nalim e Thiago Dionisio")

# Título e subtítulo da página
st.title("As novas fronteiras do Brasil em movimento")
st.subheader("Enquanto o país se divide entre quem chega, quem sai e quem volta, os números do Censo revelam um Brasil que se reconstrói em silêncio, dentro e fora de si mesmo.")

caminho_imagem = os.path.join(pasta, "agenciabrasilmarcelo.jpg")
st.image(caminho_imagem,
         caption="Foto: Marcelo Camargo/Agência Brasil")


# Texto introdutório
st.write("Nos últimos doze anos, o Brasil mudou de lugar. Ou melhor: os brasileiros mudaram dentro dele. Cruzaram fronteiras invisíveis entre estados, levaram sotaques e memórias em viagens que, somadas, redesenharam o mapa humano do país. Santa Catarina, que por décadas foi destino de europeus, hoje é o endereço de milhares de brasileiros em busca de emprego, segurança e sossego. Goiás e Mato Grosso, antes vistos como passagem, viraram ponto de chegada. Já o Rio de Janeiro e o Distrito Federal, antigos polos de atração, vivem o efeito contrário, o êxodo silencioso de quem busca recomeçar em outro canto.")
st.write("De acordo com os dados do Censo Demográfico 2022, compilados e analisados pelo Instituto Brasileiro de Geografia e Estatística (IBGE), mais de 4,6 milhões de brasileiros mudaram de estado entre 2017 e 2022. Esses números revelam um país em plena redistribuição interna, guiado por oportunidades econômicas, busca por qualidade de vida e custos mais acessíveis.")
st.write("Entre as milhares de pessoas que deixaram o Rio nos últimos anos está Elizabete Pereira, empresária do setor imobiliário, que se mudou para Goiânia em 2005 em busca de segurança e estabilidade.")
st.write("“O principal motivo para deixar o Rio foi a violência. No começo foi difícil, principalmente para conseguir uma boa colocação no mercado de trabalho e encontrar opções de lazer, as crianças sentiam muita falta da praia, mas hoje temos uma liberdade que lá não tínhamos: aqui a gente vai e vem sem aquele medo constante de assalto ou tiroteio”, conta. “Em alimentação e moradia não vejo tanta diferença de custo, mas aqui gastamos menos com locomoção e educação, e ganhamos em qualidade de vida, com escola e saúde melhores para a família.”")

st.subheader("Compreendendo os indicativos do IBGE")

st.write("Os dados extraídos do Censo apresentam alguns indicadores relevantes, entre eles o saldo migratório, definido como a diferença entre o número de pessoas que deixaram o estado e aquelas que passaram a residir nele. Esses valores podem ser visualizados no gráfico abaixo.")

df_saldo = df_saldo.sort_values("saldo_migratorio", ascending=True)

df_saldo["saldo_formatado"] = df_saldo["saldo_migratorio"].apply(
    lambda x: f"{x:,}".replace(",", ".")
)

df_saldo["estado_nome"] = df_saldo["uf"].map(nomes_estados)

fig = px.bar(
    df_saldo,
    x="saldo_migratorio",
    y="estado_nome",
    orientation="h",
    color="saldo_migratorio",
    color_continuous_scale=["red", "white", "green"],
    title="Mapa do saldo migratório por estado",
    labels={"estado_nome": "Estado", "saldo_migratorio": "Saldo migratório"},
    text="saldo_formatado"
)

fig.update_layout(
    xaxis_title="Saldo migratório",
    yaxis_title="",
    yaxis=dict(showgrid=False, tickfont=dict(size=14)),
    xaxis=dict(showgrid=True, zeroline=True),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14),
    margin=dict(l=80, r=40, t=60, b=40),
    height=900,
    bargap=0.25
)

fig.update_traces(
    textposition="auto",
    textfont=dict(size=12),
    marker_line_color="black",
    marker_line_width=0.8,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Saldo migratório: %{text}<extra></extra>"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.write("Outro indicador apresentado é a taxa migratória, que expressa a variação proporcional de perda ou ganho de moradores oriundos de outros estados. Diferentemente do saldo absoluto, essa taxa considera apenas valores relativos, permitindo a comparação entre unidades da federação com populações de tamanhos distintos.")


# -----------------------------
# Mapa
# -----------------------------
df_saldo["taxa_formatada"] = df_saldo["taxa_migra"].apply(lambda x: f"{x*100:.2f}".replace(".", ",") + "%")
df_saldo["imigrantes_fmt"] = df_saldo["imigrantes"].apply(lambda x: f"{x:,}".replace(",", "."))
df_saldo["emigrantes_fmt"] = df_saldo["emigrantes"].apply(lambda x: f"{x:,}".replace(",", "."))
df_saldo["saldo_fmt"] = df_saldo["saldo_migratorio"].apply(lambda x: f"{x:,}".replace(",", "."))

fig = px.choropleth(
    df_saldo,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="uf",
    color="taxa_migra",
    color_continuous_scale=["#c90000", "#ffffff", "#1E0FF0"],
    featureidkey="properties.sigla",
    projection="mercator",
    title="Mapa com a taxa migratória de cada estado (arraste o mouse para verificar)",
)

fig.update_geos(fitbounds="locations", visible=False)

fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[3]}</b><br>"
        "Taxa migratória: %{customdata[0]}<br>"
        "Imigrantes: %{customdata[1]}<br>"
        "Emigrantes: %{customdata[2]}<br>"
        "Saldo migratório: %{customdata[4]}<extra></extra>"
    ),
    customdata=df_saldo[[
        "taxa_formatada",
        "imigrantes_fmt",
        "emigrantes_fmt",
        "uf",
        "saldo_fmt"
    ]]
)

fig.update_layout(
    margin={"r":0,"t":30,"l":0,"b":0}
)

st.plotly_chart(fig, config={"responsive": True})

st.write ("O movimento se torna ainda mais claro quando observamos os estados individualmente. Santa Catarina é o caso mais emblemático: registrou um saldo migratório positivo de 354 mil pessoas, o equivalente a quase 5% da população atual, o maior do país. Em segundo aparecem Goiás (+186 mil) e Mato Grosso (+103 mil), impulsionados pela expansão do agronegócio e da construção civil. A Paraíba desponta como exceção nordestina com saldo positivo (+30 mil), enquanto o Rio de Janeiro (-165 mil) e o Distrito Federal (-99 mil) estão entre os que mais perderam moradores.")
st.write ("Segundo Diego Moreira, doutorando em Geografia pela PUC-Rio, “todo fluxo migratório leva em consideração fatores de atração e de repulsão. No caso atual, os grandes centros tradicionais, como Rio de Janeiro, São Paulo, Belo Horizonte e Porto Alegre, estão saturados, com custo de vida muito elevado e serviços urbanos que funcionam mal. Isso empurra a população para polos médios que continuam crescendo.”")


st.subheader("O novo eixo migratório")

caminho_sampa = os.path.join(pasta, "prefeiturasp.jpg")
st.image(caminho_sampa,
         caption="Estado de São Paulo registrou saldo migratório negativo pela primeira vez - Foto: Divulgação/Prefeitura de São Paulo")

st.write ("Dessa forma, o que antes era uma rota quase automática para o Sudeste passou a se fragmentar em novos destinos. Santa Catarina e Paraná formam um “novo eixo migratório”, atraindo moradores de 13 estados diferentes, do Acre ao Pará, de Sergipe a Roraima.")
st.write ("“Santa Catarina se tornou um polo muito atrativo porque tem baixo índice de desemprego, economia em expansão e um nível de formalidade trabalhista muito alto. Isso é decisivo, porque muitas regiões do país ainda dependem de trabalho informal. Os contratos são mais estáveis e a renda per capita é maior, o que cria um ambiente capaz de absorver mão de obra, especialmente a mão de obra nordestina, que ainda é a mais barata do país’’, explica o geógrafo.")
st.write ("Já São Paulo registrou saldo migratório negativo pela primeira vez desde 1991, ano em que o IBGE passou a acompanhar esses fluxos de forma sistemática. O movimento está ligado à perda de ritmo da industrialização no estado e ao fortalecimento de novos polos econômicos em regiões próximas, que passaram a oferecer oportunidades de emprego e custo de vida mais atrativos.")
st.write ("O estado do Rio de Janeiro se destaca por apresentar um dos menores saldos migratórios do país. Mais de 165 mil fluminenses deixaram o estado em busca de novas oportunidades, em meio a um cenário marcado pelo agravamento da violência urbana, pela queda na oferta de empregos formais e pelo custo de vida elevado, especialmente na Região Metropolitana.")
st.write ("Embora São Paulo também registre saldo negativo, a intensidade da perda populacional do Rio evidencia suas fragilidades estruturais. ‘’No Rio de Janeiro, o principal fator não é apenas violência ou crise fiscal, é a saturação urbana. Os serviços funcionam muito pouco, o transporte é ruim, o custo de vida é altíssimo. O fluminense não vive: ele sobrevive. É natural que as pessoas busquem centros menos saturados. O Rio nunca teve uma economia tão dinâmica quanto São Paulo; atraía pela quantidade, não pela qualidade’’, afirma o geógrafo.")
st.write ("Já o Centro-Oeste emerge como nova fronteira demográfica. Goiás, por exemplo, recebe 41% de seus migrantes vindos de Minas Gerais e quase 11% do Distrito Federal, reflexo do “transbordamento” da capital federal, que perdeu população para as cidades vizinhas mais baratas e conectadas. Mato Grosso e Mato Grosso do Sul também aparecem no topo, alimentados pela expansão agrícola, pela indústria de alimentos e pela migração de trabalhadores qualificados.")

st.subheader("As populações de cada cidade")

st.write ("A base de dados do IBGE reúne informações sobre a origem das populações municipais por unidade da federação. Dessa forma, é possível identificar o total de habitantes de cada município e também o número de residentes nascidos em outros estados.")
st.write ("Com o objetivo de facilitar a consulta, os dados foram organizados em um hub interativo que permite selecionar o município de interesse e visualizar sua população total, a população migrante e o respectivo percentual.")

# ==============================
# HUB COM SELEÇÃO DE MUNICÍPIOS
# ==============================

caminho_municipios = os.path.join(pasta, "municipios.xlsx")

st.markdown("**Consulte a população migrante por município e Unidade Federativa**:")

def formatar_brasileiro(numero):
    return f"{numero:,}".replace(",", ".")

def formatar_percentual(valor):
    return f"{valor:.2f}%".replace(".", ",")  # padrão brasileiro


@st.cache_data
def carregar_dados():
    df = pd.read_excel(caminho_municipios)
    df.columns = [col.strip() for col in df.columns]
    df["População"] = df["População"].replace("-", 0).astype(int)
    return df

df = carregar_dados()

municipio = st.selectbox(
    "Selecione o município:",
    sorted(df["Município"].unique()),
    index=None,
    placeholder="Escolha um município..."
)

if municipio:

    # Filtrar município
    resultado = df[df["Município"] == municipio].copy()

    # Totais
    total_pop = resultado["População"].sum()
    maior_pop = resultado["População"].max()
    migrantes_totais = total_pop - maior_pop

    # Ordenar do maior para menor
    resultado = resultado.sort_values(by="População", ascending=False)

    # Criar coluna Percentual
    resultado["Percentual"] = (resultado["População"] / total_pop) * 100

    # Formatar colunas
    resultado_formatado = resultado.copy()
    resultado_formatado["População"] = resultado_formatado["População"].apply(formatar_brasileiro)
    resultado_formatado["Percentual"] = resultado_formatado["Percentual"].apply(formatar_percentual)

    st.subheader(f"População por Estado de Origem em {municipio}")

    st.dataframe(
        resultado_formatado[["Origem", "População", "Percentual"]],
        use_container_width=True,
        hide_index=True
    )

    # Caixa separada com totais
    st.subheader("Totais no município selecionado")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Migrantes totais",
            value=formatar_brasileiro(migrantes_totais)
        )

    with col2:
        st.metric(
            label="População total do município",
            value=formatar_brasileiro(total_pop)
        )

else:
    st.info("Os dados serão exibidos aqui")


st.write("No caso de Porto Alegre, por exemplo, o Censo registra aproximadamente 1,3 milhão de habitantes, dos quais cerca de 94% são naturais do Rio Grande do Sul.")

st.subheader("Em busca de uma vida estável")

caminho_floripa = os.path.join(pasta, "florianopolis.jpg")
st.image(caminho_floripa,
         caption="Florianópolis é um dos principais destinos para migrantes brasileiros - Foto: Divulgação/Prefeitura de Florianópolis")

st.write("Enquanto as grandes metrópoles perderam atratividade, outras cidades passaram a representar o ideal de “vida estável”, especialmente entre os jovens. Em Santa Catarina, por exemplo, se destacam Itajaí, Joinville e Florianópolis.")
st.write("A escolha da jornalista Laura Machado, de 27 anos, ilustra essa tendência. Natural de Macapá (AP), ela se mudou para a capital catarinense em 2023 em busca de melhores oportunidades de trabalho e qualidade de vida. Meses antes da mudança, ela visitou a cidade e se encantou com a paisagem, o ritmo mais tranquilo e as opções de lazer.")
st.write("A mudança, porém, trouxe desafios. Laura conta que os salários são um pouco mais altos do que em sua cidade natal, mas o custo de vida, sobretudo com moradia, é elevado. Segundo ela, as opções mais acessíveis costumam ficar distantes ou em condições precárias. Ainda assim, destaca que a sensação de segurança compensa parte das dificuldades.")
st.write("“Me sinto mais segura aqui, mais tranquila para andar sozinha nas ruas, com menos medo de assaltos e furtos”, destaca.")

st.subheader("De onde vêm e para onde vão")

# ==============================
# CARDS COM PULAÇÃO MIGRANTE
# ==============================
     
st.markdown(
    """
    <div style="border: 2px solid #ccc; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        👉 87% da população do Norte nasceu lá; 6,8% veio do Nordeste, 2,1% do Sudeste, 1,3% do Sul e 1,7% do Centro-Oeste.
    </div>

    <div style="border: 2px solid #ccc; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        👉 96,6% da população do Nordeste nasceu lá; 0,4% veio do Norte, 2,2% do Sudeste, 0,2% do Sul e 0,4% do Centro-Oeste.
    </div>

    <div style="border: 2px solid #ccc; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        👉 88,7% da população do Sudeste nasceu lá; 0,4% veio do Norte, 8% do Nordeste, 1,6% do Sul e 0,6% do Centro-Oeste.
    </div>

    <div style="border: 2px solid #ccc; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        👉 91,9% da população do Sul nasceu lá; 0,8% veio do Norte, 1,7% do Nordeste, 4% do Sudeste e 0,6% do Centro-Oeste.
    </div>

    <div style="border: 2px solid #ccc; padding: 12px; border-radius: 8px; margin-bottom: 12px;">
        👉 73,4% da população do Centro-Oeste nasceu lá; 3,1% veio do Norte, 11,5% do Nordeste, 7,7% do Sudeste e 3,7% do Sul.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("Apesar da intensa mobilidade, uma parte significativa do país permanece fortemente enraizada. O Nordeste é a região mais “nativa” do país: 96,6% dos nordestinos vivem na própria região. Esse dado é acompanhado de um fenômeno recente: a migração de retorno. Estados como Paraíba e Ceará passaram a atrair antigos emigrantes, incluindo aposentados, empreendedores e famílias que decidiram voltar após anos vivendo em outras regiões.")
st.write("Para o professor Carlos de Almeida Toledo, do Departamento de Geografia da Universidade de São Paulo (FFLCH/USP), o fenômeno da migração de retorno se deve, entre outros fatores, ao desenvolvimento econômico e social observado nas cidades nordestinas nas últimas décadas. Segundo ele, “com o avanço da modernização, impulsionado pela migração rural-urbana, pelo crescimento econômico e pela chegada de programas como o Luz para Todos e a ampliação da telefonia, as pequenas cidades nordestinas começaram a se transformar”.")
st.write("Essa transformação, explica Toledo, se refletiu em melhorias na infraestrutura urbana, no acesso a serviços e na qualidade de vida, fatores que têm reconfigurado decisões familiares e despertado o desejo de retorno. Mas esse deslocamento não envolve apenas quem volta: também atrai pessoas de outras regiões que encontram no Nordeste um caminho possível para recomeçar.")
st.write("É o caso de Alex, que deixou o Rio de Janeiro, escolheu João Pessoa para criar a filha e tornou-se um dos mais de 13 mil fluminenses que residem na capital da Paraíba. “Eu queria que ela crescesse em um lugar com boa infraestrutura e mais seguro e tranquilo. João Pessoa, mesmo sendo capital, tem características interioranas, é mais calma e com custo de vida muito mais baixo. Hoje consigo morar em uma área valorizada, perto da praia, com uma qualidade de vida que no Rio seria impossível”, conta.")
st.write("A adaptação, porém, não foi simples. “Apesar disso, o processo de adaptação foi extremamente difícil. Estou aqui há cinco anos e ainda enfrento desafios, porque o ritmo é completamente diferente, tudo aqui é mais devagar. Culturalmente é outro mundo. Também há dificuldade na área profissional: trabalha-se muito e paga-se pouco. Ainda existe uma cultura de trabalho muito desgastante, quase exploratória, o que torna esse processo de adaptação ainda mais complexo para mim.”")



# ==============================
# TABELA - MATRIZ DE MIGRAÇÃO (NASCIMENTO x RESIDÊNCIA)
# ==============================
st.subheader("Compreendendo o fluxo com uma Matriz de Confusão ")

st.write("A análise dos dados divulgados pelo IBGE possibilitou novas formas de observar esse cenário. A matriz de confusão oferece uma visualização mais precisa dos fluxos mais frequentes percorridos pelos migrantes brasileiros. O fluxo migratório considera o local de nascimento e o local de residência das populações das cinco regiões do país.")
st.write("Na matriz, que contempla exclusivamente os 19,6 milhões de migrantes brasileiros, é possível identificar que quase 10 milhões de nordestinos deixaram o Nordeste nas últimas décadas, deslocando-se majoritariamente para o Sudeste (6,7 milhões) e para o Centro-Oeste (1,8 milhão).")

caminho_matriz = os.path.join(pasta, "pop_migrantes_rodolfo.csv")
df_migracao = pd.read_csv(caminho_matriz)

matriz = df_migracao.pivot(index='local_nasc', columns='local_resid', values='pop')

ordem_regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']
matriz = matriz.reindex(index=ordem_regioes, columns=ordem_regioes)

matriz_pct = matriz.div(matriz.sum(axis=1), axis=0) * 100

text_display = []
for i in range(len(matriz)):
    row_text = []
    for j in range(len(matriz.columns)):
        pop_val = int(matriz.iloc[i, j]) if not pd.isna(matriz.iloc[i, j]) else 0
        pct_val = matriz_pct.iloc[i, j] if not pd.isna(matriz_pct.iloc[i, j]) else 0

        if pop_val == 0:
            row_text.append("—")
        else:
            pct_formatada = f"{pct_val:.1f}".replace(".", ",") + "%"
            pop_formatado = f"{pop_val:,}".replace(",", ".")
            row_text.append(f"{pct_formatada}<br>{pop_formatado}")
    text_display.append(row_text)

fig = go.Figure(data=go.Heatmap(
    z=matriz.values,
    x=matriz.columns,
    y=matriz.index,
    colorscale='rdpu',
    text=text_display,
    texttemplate="%{text}",
    hovertemplate='<b>Nascimento:</b> %{y}<br><b>Residência:</b> %{x}<br><b>População:</b> %{z:,.0f}<extra></extra>',
))

st.plotly_chart(fig, config={"responsive": True})

with st.expander("❓ Não entendeu a matriz? Clique aqui para mais detalhes:"):
    st.write("- **Diagonal (—)**: Representa a própria região (migrantes não computados)")
    st.write("- **Percentuais**: Proporção de nascidos em cada região que migraram para outras")
    st.write("- **Valores absolutos**: População total que migrou entre as regiões")

st.write("O que ocorre no Nordeste contrasta com o cenário do Centro-Oeste, hoje a região mais cosmopolita do país. Grande parte de seus moradores nasceram em outras regiões. No topo desse movimento está o Distrito Federal, cuja população é formada majoritariamente por migrantes. Quase metade dela  é de origem goiana. O crescimento urbano de Goiânia, Cuiabá e Campo Grande revela a fotografia de um Brasil interiorizado, no qual cidades longe do litoral passam a disputar protagonismo econômico e demográfico com as grandes capitais costeiras. Compreendendo o fluxo com uma Matriz de Confusão:")




st.subheader("O perfil de quem fica mudou: Um panorama dos imigrantes")

caminho_imagem2 = os.path.join(pasta, "agenciasenado.jpg")
st.image(
    caminho_imagem2,
    caption="Imigrantes venezuelanas entram em território brasileiro por cidades de Roraima - Foto: Marcelo Camargo/Ag. Brasil. Agência Senado"
)

st.write("Ao mesmo tempo em que o país se movimenta internamente, estrangeiros também voltaram a escolher o Brasil como moradia. Depois de décadas de retração migratória, o número de imigrantes e naturalizados quase dobrou entre 2010 e 2022, saltando de 592 mil para mais de 1 milhão.")

caminho = "imigrantes.xlsx"

df_imigr = pd.read_excel(caminho)
df_imigr.columns = [str(col).strip() for col in df_imigr.columns]
df_imigr = df_imigr[~df_imigr["País/Região"].str.contains("Total", case=False, na=False)]

paises = ["Venezuela", "Portugal", "Bolívia", "Colômbia", "Haiti", "Paraguai", "Argentina", "Japão", "Itália", "China", "Uruguai", "Peru", "Estados Unidos", "Angola"]
df_imigr = df_imigr[df_imigr["País/Região"].isin(paises)]

df_imigr = df_imigr[["País/Região", "2010", "2022"]]

df_long = df_imigr.melt(id_vars="País/Região", var_name="Ano", value_name="População")
fig_imigr = px.line(
    df_long,
    x="Ano",
    y="População",
    color="País/Região",
    markers=True,
    title="Evolução do número de imigrantes por país (2010–2022)",
    labels={"População": "Número de imigrantes", "Ano": "Ano"}
)

fig_imigr.update_layout(
    xaxis=dict(tickmode="array", tickvals=["2010", "2022"]),
    yaxis_title="Número de imigrantes",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14),
    height=600,
    legend_title_text="País/Região"
)

st.plotly_chart(fig_imigr, use_container_width=True)

st.write("Conforme indicado no gráfico, o perfil migratório passou por uma mudança significativa: observa-se redução no contingente de europeus e asiáticos e um crescimento expressivo no número de latino-americanos e africanos.")
st.write("A América Latina e o Haiti são hoje o epicentro da nova imigração, e juntos representam 64% de todos os estrangeiros no país. No entanto, a  Venezuela lidera o ranking: saltou de 2 mil 869 pessoas em 2010 para 271 mil em 2022, um aumento de mais de 9.000%. Em seguida estão  Haiti, Bolívia, Colômbia e Paraguai.")
caminho_imagemwisnel = os.path.join(pasta, "wisnel.png")

st.image(caminho_imagemwisnel,
         caption="Wisnel Joseph ao lado de Laís Menenguello, antropóloga e co-host do podcast O Haiti é também aqui. - Foto: Reprodução")

st.write("‘’Esses países vivem crises econômicas severas. O Brasil, por contraste, mantém fronteiras acessíveis e não adota práticas de deportação em massa, o que fortalece ainda mais sua atratividade. O Brasil se tornou um dos poucos destinos acessíveis, legalizados e com acolhimento humanitário. Isso explica o salto gigantesco desse fluxo’’,  explica o sociólogo, Caio Felipe.")
st.write("O refúgio humanitário substituiu o antigo modelo de imigração baseada no  trabalho. Venezuelanos e haitianos chegam em busca de proteção, estudo e recomeço, concentrando-se em cidades das regiões Norte e Sudeste.")
st.write("No caso  venezuelano, a migração coincide com a crescente instabilidade política ocasionada pelo governo de Nicolás Maduro e, por consequência, pela hiperinflação, escassez de alimentos, falta de medicamentos e de produtos básicos.")
st.write("Já a imigração haitiana está ligada à grave crise humanitária desencadeada pelo terremoto de 2010, que destruiu parte do país, deixou mais de 300 mil mortos e agravou a pobreza, o desemprego e a instabilidade política. Diante desse cenário, o Brasil se tornou um destino possível, especialmente após a criação, em 2012, de um visto humanitário específico para haitianos, que facilitou a entrada e a permanência no país.")
st.write("Enquanto isso, portugueses, italianos e espanhóis reduziram sua presença: a imigração europeia caiu 23% no período, e muitos optaram por se naturalizar ou retornaram a seus países de origem.")

st.subheader("As dificuldades de quem decide permanecer")
st.write("Entre aqueles que escolheram o Brasil como novo lar está o haitiano Wisnel Joseph, apresentador do podcast O Haiti também é aqui. Ele chegou ao país em 2018 para cursar o mestrado em sua área e defendeu sua dissertação em fevereiro de 2020, pouco antes da pandemia de Covid-19. Desde então, decidiu permanecer.")
st.write("Sua trajetória, no entanto, se soma à de outros conterrâneos que enfrentam dificuldades para ingressar no mercado de trabalho, mesmo com formação superior. Muitos haitianos e haitianas acabam exercendo funções de baixa remuneração, apesar de seus títulos de graduação e pós-graduação, pela dificuldade de conseguir vagas compatíveis com sua especialização.")
st.write("O apresentador também enfrentou esse impasse. Depois de concluir o mestrado na Universidade Federal de Mato Grosso, não conseguiu colocação na própria área e precisou recorrer a uma rede de apoio formada por haitianos no Brasil, um coletivo que auxiliava conterrâneos na busca por moradia, trabalho e condições de vida dignas.")
st.write("Agora, vivendo ao lado da esposa e do filho recém nascido no país, a rotina finalmente ganhou estabilidade. “A vida por aqui tem sido tranquila. Estou feliz por ter a oportunidade de continuar meus estudos. No momento, estou focado em concluir o doutorado”, afirma à reportagem. Wisnel pesquisa a reterritorialização de haitianos no país.")
st.write("Mesmo com resultados ainda preliminares, os dados do Censo Demográfico 2022 deixam claro que a migração brasileira já não segue uma única direção nem se limita às trajetórias históricas conhecidas. Os deslocamentos se espalham por diferentes regiões, redesenhando a geografia humana do país e apontando tendências essenciais para a formulação de políticas públicas, planejamento urbano e compreensão das transformações sociais que moldam o Brasil contemporâneo.")


# ==============================
# OBSERVAÇÕES FINAIS
# ==============================
st.subheader("O país em deslocamento permanente")

st.write("De um lado, estados que crescem acima da média e reconfiguram a geografia urbana. De outro, regiões que perdem habitantes, mas reencontram laços e histórias de volta. O que antes parecia um movimento unidirecional, do interior para o litoral, do Nordeste para o Sudeste, agora se dispersa em várias direções.")
st.write("Santa Catarina e Goiás tornaram-se símbolos de um novo tempo, onde o crescimento não se mede apenas por PIB, mas pela promessa de segurança e estabilidade. Ao mesmo tempo, o Nordeste aparece não mais como ponto de partida, mas como destino de quem quer recomeçar.")
st.write("O Brasil voltou a receber estrangeiros, em especial latino-americanos, que cruzam fronteiras fugindo da fome ou de crises políticas e humanitárias em busca de um chão possível. E dentro desse mesmo território, milhões de brasileiros continuam a fazer o mesmo: mudar de endereço para tentar mudar de vida.")


## Para visualizar no navegador: "streamlit run streamlitidp.py" no terminal
