import csv
from bs4 import BeautifulSoup


def extract_apostas_from_html(html_file, csv_file):
    # Abrir o arquivo HTML local
    with open(html_file, 'r', encoding='utf-8') as file:
        # Ler o conteúdo do arquivo
        html_content = file.read()
        
        # Utilizar BeautifulSoup para analisar o conteúdo HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Abrir o arquivo CSV para escrever as informações coletadas
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            # Definir os cabeçalhos do arquivo CSV
            fieldnames = ["Tipo_Aposta", "Equipe_Casa", "Equipe_Fora", "Resultado", "Odds", "Market", "Informação Extra", "Data", "Montante", "Ganhos"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Encontrar todos os elementos bet-card
            bet_cards = soup.find_all('bet-card')
            
            # Iterar sobre cada bet-card e extrair informações relevantes
            for bet_card in bet_cards:
                tipo_aposta = bet_card.find('div', class_='betCard_headerTitle').text.strip()
                
                tag_label_element = bet_card.find('span', class_='tag_label')
                if tag_label_element:
                    resultado = tag_label_element.text.strip()
                else:
                    resultado = "Informação não disponível"
                
                equipes_elements = bet_card.find_all('span', class_='scoreboard_contestantLabel')
                
                if len(equipes_elements) >= 2:
                    equipe_casa = equipes_elements[0].text.strip()  # A primeira equipe é a equipe da casa
                    equipe_fora = equipes_elements[1].text.strip()  # A segunda equipe é a equipe visitante
                else:
                    equipe_casa = "Informação não disponível"
                    equipe_fora = "Informação não disponível"
                
                odds_element = bet_card.find('span', class_='oddValue')
                if odds_element:
                    odds = odds_element.text.strip()
                else:
                    odds = "Informação não disponível"
                
                market_element = bet_card.find('div', class_='marketBets_label')
                if market_element:
                    market = market_element.text.strip()
                else:
                    market = "Informação não disponível"
                
                # Encontrar o elemento com a classe "marketBets_value" para obter a informação
                market_value_element = bet_card.find('div', class_='marketBets_value')
                if market_value_element:
                    informacao_extra = market_value_element.text.strip()
                else:
                    informacao_extra = "Informação não disponível"
                
                # Encontrar a data da aposta
                data_element = bet_card.find('div', class_='scoreboard_date')
                if data_element:
                    data = data_element.text.strip()
                else:
                    data = "Informação não disponível"
                
                # Encontrar os elementos de montante e ganhos
                montante_element = bet_card.find('div', class_='summaryBets_listItemLabel', string='Montante')
                if montante_element:
                    montante_value = montante_element.find_next('div', class_='summaryBets_listItemValue').text.strip()
                else:
                    montante_value = "Informação não disponível"
                
                if resultado == "Perdida":
                    ganhos_value = "0,00 €"
                elif resultado == "Ganhos":
                    montante_value_float = float(montante_value.replace(',', '.').split()[0])  # Convertendo para float
                    odds_float = float(odds.replace(',', '.'))  # Convertendo para float
                    ganhos_value = "{:.2f} €".format(montante_value_float * odds_float)  # Calculando os ganhos
                else:
                    ganhos_value = "Informação não disponível"
                
                # Escrever as informações coletadas no arquivo CSV
                writer.writerow({
                    "Tipo_Aposta": tipo_aposta,
                    "Equipe_Casa": equipe_casa,
                    "Equipe_Fora": equipe_fora,
                    "Resultado": resultado,
                    "Odds": odds,
                    "Market": market,
                    "Informação Extra": informacao_extra,
                    "Data": data,
                    "Montante": montante_value,
                    "Ganhos": ganhos_value
                })


# Nome do arquivo HTML local
html_file = "html.txt"
# Nome do arquivo CSV para salvar os dados
csv_file = "apostas.csv"

# Chamar a função para extrair as informações do arquivo HTML e gravar no arquivo CSV
extract_apostas_from_html(html_file, csv_file)


