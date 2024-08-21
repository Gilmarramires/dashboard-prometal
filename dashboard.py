import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuração inicial da página
st.set_page_config(page_title="Dashboard Prometal EPIs", layout="wide", initial_sidebar_state="collapsed")

# Caminho da imagem (ajuste conforme necessário)
image_path = 'logo.png'  # Altere para o caminho correto

# Exibir o logotipo no título
st.image(image_path, width=200)  # Ajusta a largura da imagem para 200px
st.markdown("<h1 style='text-align: center; color: #013283;'>Dashboard Dados Prometal EPIs</h1>", unsafe_allow_html=True)

# Carregando os dados
data_path = 'data/dados_prometal.csv'
df = pd.read_csv(data_path)

# Calcular a variação percentual entre meses
def calculate_percentage_change(df, column):
    df[f'{column} % Change'] = df[column].pct_change() * 100
    return df

# Aplicar o cálculo de variação percentual
df = calculate_percentage_change(df, 'Visitas Site 2024')
df = calculate_percentage_change(df, 'Conversões 2024')
df = calculate_percentage_change(df, 'Leads 2024')
df = calculate_percentage_change(df, 'Solicitação de Acesso 2024')
df = calculate_percentage_change(df, 'Novos Seguidores Instagram 2024')
df = calculate_percentage_change(df, 'Novos Seguidores Facebook 2024')

# Função para criar gráficos com estilo moderno e escalas ajustadas
def create_figure(title, x_data, y_data, text_data, line_color, marker_color, fill_color=None, is_bar=False, yaxis_title=None):
    fig = go.Figure()
    if is_bar:
        fig.add_trace(go.Bar(
            x=x_data,
            y=y_data,
            text=text_data,
            marker=dict(color=marker_color, line=dict(width=1.5, color='black')),
            textposition='outside',
            textfont=dict(size=14, color='black'),
            opacity=0.8,
            hovertemplate='%{x}: %{y}<extra></extra>'  # Tooltip com detalhes
        ))
    else:
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers+text',
            line=dict(color=line_color, width=3),
            marker=dict(size=10, color=marker_color, line=dict(width=1, color='black')),
            text=text_data,
            textposition='top center',
            textfont=dict(size=14, color='black'),
            fill='tozeroy' if fill_color else None,
            fillcolor=fill_color,
            hovertemplate='Mês: %{x}<br>Valor: %{y}<br>Variação: %{text}<extra></extra>'  # Tooltip com detalhes
        ))

    fig.update_layout(
        title=title,
        template="plotly_white",
        title_font_size=28,
        title_font_family="Arial, sans-serif",
        title_font_color="#013283",
        plot_bgcolor='#ffffff',
        paper_bgcolor='#f5f5f5',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title_font=dict(size=14, family="Arial, sans-serif", color='#013283'),
            tickangle=45,
            tickfont=dict(size=12, family="Arial, sans-serif", color='#013283'),
            tickvals=x_data,
            ticktext=[f"<b>{month}</b>" for month in x_data],  # Nomes dos meses em negrito
            range=[-0.5, len(x_data)-0.5],
            tickmode='array'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title_font=dict(size=14, family="Arial, sans-serif", color='#013283'),
            title_text=yaxis_title,
            tickfont=dict(size=12, family="Arial, sans-serif", color='#013283'),
            range=[0, max(y_data) * 1.2],
            tickmode='array'
        ),
        margin=dict(l=80, r=80, t=80, b=80),
        font=dict(size=14, family="Arial, sans-serif", color='#013283'),
        autosize=True
    )

    return fig

# Adicionar legendas explicativas
def add_legends(fig):
    fig.update_layout(
        annotations=[
            dict(
                xref='paper', yref='paper',
                x=0.02, y=0.98,
                showarrow=False,
                text="<b style='color: #013283;'>Legenda:</b><br><span style='color: #faae03;'>% = Crescimento ou Diminuição</span><br><span style='color: #faae03;'>Total do Mês = Valor Total</span>",
                align='left',
                font=dict(size=12, color='#013283'),
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='#013283',
                borderwidth=1
            )
        ]
    )
    return fig

# Gráficos com números e porcentagens em cores diferenciadas
figures = {
    'Visitas ao Site - 2024': add_legends(create_figure(
        'Visitas ao Site - 2024', df['Mês'], df['Visitas Site 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Visitas Site 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Visitas Site 2024'])],
        '#013283', '#013283', 'rgba(1,50,100,0.2)'
    )),
    'Conversões - 2024': add_legends(create_figure(
        'Conversões - 2024', df['Mês'], df['Conversões 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Conversões 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Conversões 2024'])],
        '#faae03', '#faae03', None, is_bar=True
    )),
    'Leads - 2024': add_legends(create_figure(
        'Leads - 2024', df['Mês'], df['Leads 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Leads 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Leads 2024'])],
        '#013283', '#013283', 'rgba(1,50,100,0.2)'
    )),
    'Solicitações de Acesso - 2024': add_legends(create_figure(
        'Solicitações de Acesso - 2024', df['Mês'], df['Solicitação de Acesso 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Solicitação de Acesso 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Solicitação de Acesso 2024'])],
        '#013283', '#013283', 'rgba(1,50,100,0.2)'
    )),
    'Novos Seguidores no Instagram - 2024': add_legends(create_figure(
        'Novos Seguidores no Instagram - 2024', df['Mês'], df['Novos Seguidores Instagram 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Novos Seguidores Instagram 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Novos Seguidores Instagram 2024'])],
        '#013283', '#013283', 'rgba(1,50,100,0.2)'
    )),
    'Novos Seguidores no Facebook - 2024': add_legends(create_figure(
        'Novos Seguidores no Facebook - 2024', df['Mês'], df['Novos Seguidores Facebook 2024'],
        [f"<b style='color: #013283;'>{val:,}</b><br><span style='color:#faae03;'>{df.loc[i, 'Novos Seguidores Facebook 2024 % Change']:.1f}%</span>" 
         for i, val in enumerate(df['Novos Seguidores Facebook 2024'])],
        '#013283', '#013283', None, is_bar=True
    ))
}

# Função para mostrar gráficos em um slider com botões de navegação
def show_slider(figures):
    # Configurar a sessão para controle do índice do gráfico atual
    if 'index' not in st.session_state:
        st.session_state.index = 0

    # Layout para os botões de navegação
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('Anterior', key='prev_button'):
            st.session_state.index = (st.session_state.index - 1) % len(figures)
    with col2:
        if st.button('Próximo', key='next_button'):
            st.session_state.index = (st.session_state.index + 1) % len(figures)

    # Mostrar o gráfico atual
    option = list(figures.keys())[st.session_state.index]
    fig = figures[option]
    st.plotly_chart(fig, use_container_width=True)

show_slider(figures)























































