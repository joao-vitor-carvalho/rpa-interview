#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[15]:


# get_ipython().system('pip install selenium')


# In[16]:


# cada navedador tem o seu webdrive, no caso do navegador Chrome é o chromedriver

from selenium import webdriver #permite criar o navegador
from selenium.webdriver.common.keys import Keys #permite escrever no navegador
from selenium.webdriver.common.by import By #permite selecionar itens no navegador

navegador = webdriver.Chrome()

# Passo 1: Pegar a cotação do dólar
#entrar no google
navegador.get('https://www.google.com/')
#pesquisar no google por 'cotação dolar'
navegador.find_element('xpath', 
    '//*[@id="APjFqb"]').send_keys('cotação dólar')
navegador.find_element('xpath', 
    '//*[@id="APjFqb"]').send_keys(Keys.ENTER)
#pegar a cotação
cotacao_dolar = navegador.find_element('xpath', 
    '//*[@id="currency-v2-updatable_2"]/div/div[3]/div[1]/div[2]/span[1]').get_attribute('data-value')
print(cotacao_dolar)

# Passo 2: Pegar a cotação do euro
#entrar no google
navegador.get('https://www.google.com/')
#pesquisar no google por 'cotação euro'
navegador.find_element('xpath', 
    '//*[@id="APjFqb"]').send_keys('cotação euro')
navegador.find_element('xpath', 
    '//*[@id="APjFqb"]').send_keys(Keys.ENTER)
#pegar a cotação
cotacao_euro = navegador.find_element('xpath', 
    '//*[@id="APjFqb"]').get_attribute('data-value')
print(cotacao_euro)

# Passo 3: Pegar a cotação do ouro
#entrar no site melhor cambio
navegador.get('https://www.melhorcambio.com/ouro-hoje')
#pegar a cotação
cotacao_ouro = navegador.find_element('xpath', 
    '//*[@id="comercial"]').get_attribute('value')
cotacao_ouro = cotacao_ouro.replace(',', '.')
print(cotacao_ouro)

#fechar o navegador
navegador.quit()


# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# - Importando a base de dados

# In[17]:


# Passo 4: Importar a base de dados
import pandas as pd

#importar/ ler a base
tabela = pd.read_excel('Produtos.xlsx')
#display(tabela)


# - Atualizando os preços e o cálculo do Preço Final

# In[18]:


# Passo 5: Atualizar os preços

# atualizar o campo de Cotação
# estrutura do .loc -> tabela.loc[linha, coluna]
tabela.loc[tabela['Moeda'] == 'Dólar', 'Cotação'] = float(cotacao_dolar)
tabela.loc[tabela['Moeda'] == 'Euro', 'Cotação'] = float(cotacao_euro)
tabela.loc[tabela['Moeda'] == 'Ouro', 'Cotação'] = float(cotacao_ouro)

# atualizar o campo de Preço de Compra = Preço Original * Cotação
tabela['Preço de Compra'] = float(tabela['Preço Original'] * tabela['Cotação'])
# atualizar o campo Preço de Venda = Preço de Compra * Margem
tabela['Preço de Venda'] = float(tabela['Preço de Compra'] * tabela['Margem'])

#display(tabela)


# ### Agora vamos exportar a nova base de preços atualizada

# In[20]:


# Passo 6: Exportar a base de preços atualizada -- bug em geração de excel 
tabela.to_excel('Produtos Novo.xlsx', index=False)
