
Olá, meu nome é Sergio 👋
• 🔭 Atualmente estou trabalhando em projetos de análise de dados.
• 🌱 Atualmente estou aprendendo sobre inteligência artificial e machine learning.
• 👯 Estou procurando colaborar em iniciativas open-source voltadas para ciência de dados.
• 🤔 Estou buscando ajuda com boas práticas de deploy em nuvem.
• 📫 Como me encontrar: sergiolmendes2026@gmail.com

# Multi-Agentes-de-IA-Para-Planejamento-de-Viagens

https://multi-agentes.streamlit.app/



Agente de IA Viagens LM é um assistente inteligente para planejamento de viagens baseado em múltiplos agentes de IA (Multi-Agentes). Em vez de apenas responder perguntas, ele coleta as informações da viagem e gera um roteiro personalizado.

As funções que ele aparenta ter são:

✈️ 1. Planejamento do roteiro

O usuário informa:

Cidade ou país de destino (ex.: Paris, França);
Quantidade de dias;
Interesses (museus, gastronomia, natureza, compras, etc.).
---------------------------------------------------------------------------------------------

Com isso, o agente monta um roteiro dia a dia.

🧠 2. Uso de múltiplos agentes de IA

A ideia de "Multi-Agentes" significa que diferentes IAs podem trabalhar em conjunto, por exemplo:

Agente Planejador
Organiza o cronograma da viagem.
Agente Turístico
Sugere atrações famosas e locais menos conhecidos.
Agente Gastronômico
Recomenda restaurantes e comidas típicas.
Agente Logístico
Calcula deslocamentos entre os pontos turísticos.
Agente Financeiro
Estima gastos da viagem.

Cada agente é especializado em uma tarefa e depois as respostas são combinadas.

📅 3. Criação automática do roteiro

Exemplo para Paris em 3 dias:

Dia 1

Torre Eiffel
Rio Sena
Museu do Louvre

Dia 2

Catedral de Notre-Dame
Bairro Latino
Café tradicional francês

Dia 3

Palácio de Versalhes
Jardim de Luxemburgo
Compras na Champs-Élysées
🌍 4. Personalização

Dependendo do interesse informado, o roteiro muda.

Se o usuário escrever:

"Natureza e trilhas"

O roteiro prioriza parques e áreas verdes.

Se escrever:

"Compras"

Ele prioriza shoppings, outlets e ruas comerciais.

🔑 5. Uso das APIs

Na lateral da aplicação aparecem:

Groq API Key
Responsável por executar o modelo de linguagem (LLM), gerando o texto do roteiro.
Tavily API Key
Permite pesquisar informações atualizadas na internet, como atrações, horários e recomendações.
📱 6. Suporte integrado

Também há:

botão de contato por e-mail;
botão para WhatsApp;
aviso de que as respostas da IA devem ser verificadas.
