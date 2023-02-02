# NLP_Tweets

## Introdução

Empresas de todo o mundo utilizam do marketing digital a fim de aumentar seu faturamento ou engajamento com a marca, no chamado brand awareness. Nesse contexto, as redes sociais surgem nas pessoas comentando sobre produtos e serviços que tais empresas disponibilizam e, ter uma forma de reconhecer se tais interações estão sendo positivas ou negativas é de grande ajuda no cálculo das métricas de eficiencia do marketing digital que está sendo realizado, tendo como fim uma melhor tomada de decisão de tal setor.

## Processamento de Linguagem Natural em comentários do Twitter

Tendo em vista a importância da análise de sentimento de comentários em redes sociais, este projeto utilizou de dados reais extraído do link: https://www.kaggle.com/competitions/tweet-sentiment-extraction/data, para o refino do treino de um modelo BERT. O modelo treinado foi implementado, no qual comentários do Twitter são analisados, em tempo real, e feita a classificação do comentario em: Positivo, Negativo ou Neutro. Os dados gerados pelo modelo são visualizados num Dashboard disponível no Power BI Online.
![image](https://user-images.githubusercontent.com/24653032/214043263-0ce56cd6-d2fb-45d8-919f-49d8df316b8d.png)

Devido a sua infraestrutura, com possibilidade de uso de GPU para o treino do modelo, o Google Colab foi utilizado para sua construção, utilizando o workflow de Data Science, seu link: https://colab.research.google.com/drive/1C51O337Qaab-bjfvh2HSN9pLy5UpQzwn?usp=sharing. Bem como, o link para uso do modelo já treinado: https://drive.google.com/file/d/1Lyci2V6VTwkFlAi2hmYrB1DQ3ovAFcTG/view?usp=share_link

## Referências

O modelo utilizado que já havia sido treinado com tweets: @inproceedings{barbieri-etal-2020-tweeteval,
                                                          title = "{T}weet{E}val: Unified Benchmark and Comparative Evaluation for Tweet Classification",
                                                          author = "Barbieri, Francesco  and
                                                            Camacho-Collados, Jose  and
                                                            Espinosa Anke, Luis  and
                                                            Neves, Leonardo",
                                                          booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2020",
                                                          month = nov,
                                                          year = "2020",
                                                          address = "Online",
                                                          publisher = "Association for Computational Linguistics",
                                                          url = "https://aclanthology.org/2020.findings-emnlp.148",
                                                          doi = "10.18653/v1/2020.findings-emnlp.148",
                                                          pages = "1644--1650"
                                                      }





