# Usando RAG e LLMs na nossa solução

## Apresentação

Este texto pretende explicar como resolver o problema principal desse case (Construir uma solução que extraia dados de um PDF), a partir de uma abordagem que use LLMs e RAG. Eu sou ex-jornalista, então tentarei descrever tudo da forma mais simples possível. *OBS.: Caso o leitor não queira pode pular a seção de contextualização e partir direto para a **seção da Solução**.

## Contextualizando: *RAG e Large Language Models (LLMs)*
### O que são LLMs

Antes de tudo, temos entender o que são *Large Language Models, ou LLMs*. Basicamente, são sistemas computacionais que utilizam redes neurais profundas para processar e gerar linguagem natural (Redes neurais são estruturas inspiradas no funcionamento do cérebro humano), a partir de uma área chamado Processamento de Linguagem Natural (NLP), que busca fazer o "computador" capaz de entender a fala humana. Todo esse processo é bastante complexo, mas algo importante de saber é que computadores só entendem números, não palavras, e existem diversas técnicas para transformar palavras e frases nesses números, chamados de vetores.

Essas redes são treinadas em grandes quantidades de dados textuais, provenientes de diversas fontes, como livros, artigos de jornais, páginas da web e muito mais. Durante o treinamento, o modelo aprende padrões na linguagem, como gramática, semântica e até mesmo nuances de estilo. Quanto mais dados o modelo tem acesso e quanto mais complexa é a arquitetura da rede, melhor será sua capacidade de compreensão e geração de texto.

A partir desse treinamento extensivo, os LLMs se tornam capazes de realizar uma variedade de tarefas linguísticas, como tradução automática, sumarização de textos, geração de conteúdo e até mesmo conversação, muitas vezes no formato de *chatbots*.

Quando interagimos com um LLM, existem 3 elementos importantes a serem considerados:

- **Entrada**: Geralmente definida por um comando, chamado de *prompt*, enviado pelo usuário. Como os modelos de inteligência artificial são, no fundo, equações matemáticas gigantescas, existe toda uma área dedicada a estudar as melhores maneiras de formular uma mensagem para uma IA, chamada *prompt engineering*.
- **Saída**: A saída gerada pelo modelo. Aqui, operam todos os algoritmos previsores que entregam uma resposta baseada na solicitação do usuário e nas limitações do sistema em que o modelo esteja sendo executado.
- **Janela de contexto**: Quando conversamos com uma pessoa, o diálogo costuma ter várias etapas onde os dois falam. Pense na janela de contexto como o 'histórico da conversa' que a IA usa para continuar entregando respostas relevantes para simular uma interação mais próxima possível da humana.

Além desses conceitos, existe algo fundamental quando falamos de modelos generativos: A não ser que haja alguma especificação do sistema, eles **sempre irão devolver uma resposta para a pergunta/solicitação do usuário**, mesmo que esteja errada. Além disso, quanto maior a janela de contexto, mais informações terão que ser levadas em consideração para a resposta. Todos esses fatores, entre outros, contribuem para o fenômeno chamado *hallucination*, onde a IA começa a dar respostas pouco coerentes com a realidade. Fora que, alguns modelos podem acabar sendo treinados com informações desatualizadas, influenciando negativamente na assertividade.

Para resolver isso, e melhorar ainda mais o desempenho, os profissionais desenvolvedores de LLMs executam diversas técnicas, como aperfeiçoamento das métricas de avaliação e retreinamento de uma parte do modelo com dados atualizados (Fine-tuning e transferência de aprendizado). Porém, uma técnica merece nossa atenção, por fornecer diversas possibilidades e ser rapidamente expansível, o RAG.

### O que é RAG?

*Retrieval-Augmented Generation* ou *Geração por Recuperação Aumentada*, ou simplesmente RAG, é uma técnica que consiste em fazer o modelo de IA complementar uma resposta gerada "pesquisando" dados externos. O Bing Chat, da Microsoft, usa esse conceito ao adicionar informações de páginas relevantes em seu motor de pesquisa, porém, o RAG também pode ser implementado com uma base de dados particular, a fim de resolver diversos problemas de negócio. Vale lembrar que o RAG não elimina completamente a ocorrência de "alucinações", mas é capaz de mitigar e melhorar as respostas entregues ao usuário.


### Como funciona o RAG?

O RAG é composto de seis principais componentes:

1. **Processamento de consulta do usuário**:
Quando um usuário faz uma pergunta (Envia um prompt), a consulta é processada para convertê-la em um vetor (Chamado de *Embedding*). Como vimos acima, isso envolve transformar a entrada de linguagem natural em uma representação numérica que captura o significado semântico da consulta.

2. **Base de conhecimento**:
Sistemas RAG dependem de uma base de conhecimento (Que pode ser uma *vectorstore/vectordatabase*) que contém pedaços de texto. Esses blocos são pré-processados e convertidos em *embeddings* também. Cada pedaço representa uma informação/documento que o chatbot pode usar para gerar respostas.

3. ***Semantic Search***:
Técnica consolidada em outros ramos de NLP. Aqui, usamos cálculos para medir a similaridade entre o vetor de entrada e os vetores dos textos na base de conhecimento. O objetivo é identificar textos/documentos que estão semanticamente próximos do que foi perguntado pelo usuário.

4. **Identificação de contexto**:
Os blocos de texto identificados por meio do *semantic search* servem como contexto para gerar respostas. Ao selecionar partes relevantes que se alinham com prompt, o chatbot garante que as respostas geradas sejam contextualmente apropriadas. É como se mandássemos informações com parte da resposta diretamente pro modelo de IA, juntamente com a pergunta.

5. **Geração de Linguagem Natural (NLG)**:
Uma vez que o contexto é estabelecido, o modelo recebe o prompt do usuário e os textos da base de conhecimento. Depois, todos os textos são convertidos em uma resposta coerente e em linguagem natural. 

6. **Apresentação de respostas**:
A etapa final envolve apresentar a resposta gerada ao usuário. Todo o processo pode ser feito diretamente na aplicação por formato de API ou com auxílio de uma interface visual. Existe uma ferramenta no mercado bem adequada para o contexto de chatbots alimentados por IA, falaremos dela mais em breve.

**Extra: Vectorstore**

Bancos de dados normais trabalham com dados em formato, muitas vezes 'legível' para os seres humanos, mas um modelo de IA não consegue entender esse tipo de informação facilmente. Por isso, no contexto de RAG, montamos nossas bases de conhecimentos em bases de dados conhecidas como vectorstores, que funcionam como armazenadores de vetores que representam formas textuais. Em escala maior e para dados persistidos, pode-se usar Vector Databases, que aplicam o mesmo conceito de uma vectorstore a um banco de dados convencional.

## A solução
### Overview

Num cenário normal, a API já apresentaria uma boa solução para resolver o problema, porém, considerando que ela é limitada a um escopo extremamente específico pelo processamento ser feito quase que inteiramente por padrões com *regex*, uma solução utilizando IA pode funcionar bem, por ser amplamente adaptável a diversos modelos de dados. Aqui, a ideia é simples e pode ter duas abordagens: 
1. **O usuário pedindo para extrair informações de um PDF utilizando IA**: Um LLM já consegue, muitas vezes, resolver esse tipo de problema sem necessidade de fine-tuning, mas o RAG pode servir para apresentar formatos específicos de arquivos para o LLM analisar, afim de mitigar erros por alguns serem muito parecidos.
2. **O usuário quer saber informações contidas em documentos diversos**: Cenário que, na minha opinião, seria mais apropriado para implementar um RAG. Temos um banco de dados vetorial ou uma vectorstore, de fato, que armazena as informações dos documentos, que nesse caso são recibos. Então, o usuário pode fazer uma pergunta relevante sobre algo contido nesses recibos. Após a consulta, o sistema procura o documento mais relevante para a resposta e ela é enviada ao usuário. Essa aplicação pode ser facilmente expansível para outros contextos, como análises sobre os próprios dados em tempo real, mostrando qual produto vendeu mais sem a necesidade de um analista de dados para construir esses relatórios. Aqui, já entra o conceito de um *agente*, que é uma aplicação de IA feita para executar tarefas específicas.

### Arquitetura

Não importa a abordagem, a arquitetura da nossa aplicação vai funcionar de forma parecida para ambas, conforme pode ser visto na imagem abaixo:

![Alt text2](/include/images/arch_rag.png?raw=true)

Aqui, a solução consiste na seguinte lógica:

1. O usuário interage com o modelo de IA através de uma aplicação com interface construída com o framework Chainlit, esta, por sua vez, envia o prompt para um sistema gerenciado e desenvolvido através do Llama-index.
2. O prompt é transformado em vetor através de um modelo de conversão de texto para vetor (Embeddings) da OpenAI. Algo importante a ser considerado é que o embedding precisa se adaptar ao modelo que irá recebê-lo. Como estaremos usando o modelo gpt 4-turbo da OpenAI, usaremos um Embedding apropriado para ele.
3. Após o processo de *embedding*, o prompt é enviado ao retriever, que é o componente que procura documentos relevantes relacionados à consulta. O escolhido aqui é o FAISS, retriever desenvolvido pela Meta.
4. Depois do processo de recuperação pelo retriever, o prompt e o contexto são enviados como um único prompt para o modelo ```gpt-4-turbo```.
5. O modelo de IA gera uma resposta. Todo o processo dos passos 2 a 4 são gerenciados pelo Llama-index. Agora, a resposta seré enviada para a aplicação do Chainlit.
6. O Chainlit exibe a resposta pro usuário, que pode continuar interagindo com a aplicação.

**Importante lembrar**: Toda essa arquitetura é uma sugestão básica de implementação. Em um cenário de produção, diversos outros elementos podem (E devem) ser considerados, como mudar o parâmetro ```chat_mode``` do modelo openAI para '*context*', de forma a levar em consideraçao também, na resposta, o histórico de conversa. Nesse caso, poderíamos adicionar mais uma etapa ao nosso fluxo, ao lado do prompt enviado pelo usuário, e que seria correspondente a todo o fluxo de conversa.

### Ferramentas

As ferramentas utilizadas nessa solução seriam:

- **Chainlit**: Framework para construir a interface da aplicação. Ele facilita a interação do usuário com o modelo de IA, gerenciando a comunicação e apresentando as respostas de forma clara e intuitiva. Nunca usei, mas tenho curiosidade. Realizei um projeto parecido mas usando Streamlit.
- **Llama-Index**: Sistema que gerencia e desenvolve a lógica de processamento e recuperação de informações. Ele coordena as etapas de embedding, recuperação de documentos e integração com o modelo de IA. Também nunca usei, pois sempre implementei projetos com Langchain, porém, o Llama-index me pareceu bem adequado por simplificar diversos passos relacionados à implementação de RAG e chatbots.
- **OpenAI Embeddings**: Modelos de conversão de texto para vetor fornecidos pela OpenAI. Esses embeddings são essenciais para transformar o prompt em vetores que podem ser processados pelo retriever e pelo modelo de IA. Os embeddings devem ser compatíveis com o modelo gpt-4-turbo da OpenAI.
- **FAISS (Facebook AI Similarity Search)**: Ferramenta desenvolvida pela Meta para busca de similaridade de alta eficiência. É utilizada como retriever para encontrar documentos relevantes com base nos vetores gerados pelos embeddings.
- **GPT-4 Turbo da OpenAI**: Modelo de IA responsável pela geração de respostas. Recebe o prompt original, o contexto relevante e o histórico de chat (quando configurado) para produzir uma resposta coerente e contextualizada.


## Outras abordagens

Além da arquitetura utilizada, podemos implementar nosso sistema RAG de outras formas

### Fine-tuning para RAG

O RAG, como todo sistema, tem seus pontos fracos, e aqui, o maior desafio é garantir que o retriever esteja recuperando os blocos de textos corretos. Uma das técnicas é treinar o próprio modelo de embeddings para capturar as nuances específicas daquele dataset, ou fazer fine-tuning em algoritmos de *semantic search*. Existem modelos específicos que fazem o processo de busca em bases vetoriais, como o ColBERT e SparseEmbed, e que podem ser ajustados para se adaptarem melhor ao contexto desejado.

### Ecossistema Azure

A Microsoft hoje é uma das maiores investidoras da OpenAI, e fornece diversas soluções integradas aos modelos GPT. Quando falamos de implemetação de RAG, a Azure, sistema de computação em nuvem da Microsoft, tem serviços que melhoram, tanto o processo, quanto a assertividade das respostas. O sistema do chatbot pode ser construído com o [*Azure Bot Services*](https://azure.microsoft.com/pt-br/products/ai-services/ai-bot-service), a base de conhecimento pode ser implementada com [*CosmosDB*](https://azure.microsoft.com/pt-br/products/cosmos-db) e a recuperação com o exclusivo [*Azure AI Search*](https://azure.microsoft.com/en-us/products/ai-services/ai-search), que possui diversas funcionalidades para melhorar o processo de busca e, por fim, o modelo de IA pode ser acessado através da integração direta com o ChatGPT no [*Azure OpenAI Service*](https://azure.microsoft.com/pt-br/products/ai-services/openai-service).

*Disclaimer: Criei essa sessão porque eu ando procurando obter a certificação AI-102 (Azure AI Engineer Associate), e é sempre bom exercitar conhecimento* :sunglasses: .

## Conclusão

Espero que possamos implementar uma dessas ou alguma outra solução. Valeu!