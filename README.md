# Fall For It
Projeto de recurso da UC-Fundamentos da Programação 

Leonardo Jorge Mendes Tavares 

GIT: https://github.com/Leojmtavares/Fall_For_It

## Arquitetura da solução 
Este código é uma implementação de um jogo utilizando a biblioteca de *Pygame*. No início são criadas várias variáveis estáticas, as quais vão ser usadas ao longo do código. Neste código estão incluídas 5 classes: *Player*, *WorldMap*, *UserInterface*, *Button* e *WindowSelector*. 

####Player
Esta classe representa a personagem que o jogador controla no mundo. Inclui métodos para a sua inicialização, fazer a atualização da sua posição e animações. Também é responsável por detetar todas as colisões no jogo e quando o jogador perde vidas. 
- No método ***\__init__*** da classe são inicializadas várias variáveis necessárias, como a posição inicial de jogador, as imagens que representam o seu movimento (animações), a sua dimensão, velocidade, entre outras. 
- O método ***update*** é um método que irá correr em cada *tick* de jogo, atualiza aspetos como posição do jogador, deteção de colisões e imagens da figura do jogador. 
  - Foi utilizada a biblioteca *Pygame* para a deteção de eventos. Com isto é possível detetar cliques por parte do utilizador nas setas que se traduzem no movimento do jogador e a mudança da representação do jogador face à direção do seu movimento.
  - É também neste método que é calculada a variável de *scroll*. Esta variável tem como função calcular o deslocamento do mapa em função daquilo que seria o movimento vertical positivo do jogador. Através disto é possível deslocar todo o mapa para cima, mantendo a posição vertical do jogador no ecrã igual, o que cria uma perceção de queda.   
  - Para a deteção de colisões é utilizada um método da biblioteca *Pygame*, o método *colliderect*. Através deste método é possível detetar uma colisão entre a *hitbox* do jogador e os *tiles* do mapa do jogo.    
- ***damage_player*** é o método que é chamado quando é detetada uma colisão entre o jogador e um *tile* do tipo *spike*. É neste método que são descontados *hitpoints* ao jogador e onde é detetado o final de jogo. 
- ***reset_player_pos*** é um método que quando chamado reestabelece a posição do jogado na sua posição inicial. É chamado quando o colide com blocos que lhe tiram vidas. 
- O método ***did_player_take_damage*** é um *boolean* que indica quando o jogador acabou de perder uma vida. 
- Por fim o método ***full_player_reset*** reestabelece por total o jogador (número de vidas, posição inicial). Grava também a pontuação do jogador. 

####WorldMap
Esta classe representa o mundo do jogo. 
- ***\__init__*** é o método que inicializa vários atributos da classe *“WorldMap”*. Define as possíveis posições dos blocos e das armadilhas na grelha e carrega todas as imagens, que por sua vez, vão substituir todos os espaços desta grelha. 
- O método ***update_player*** cria um *link* do objeto do *Player* e uma variável dentro do objeto com a classe *WorldMap*. 
- ***update_scolling_map*** é responsável por atualizar a grelha sempre que existe um *scroll* por parte do *player* maior que o tamanho de um bloco. Quando tal acontece a primeira linha de blocos é apagada, todos os outros blocos são movidos para cima, e é acrescentada uma linha nova à grelha em baixo. Esta nova linha de blocos pode ser uma linha com apenas as paredes ou então uma variação (escolhida de forma *random*) das possíveis posições das armadilhas definidas no *\__init__*. 
- ***draw*** é o método que desenha o mapa lendo a grelha e usando a função *blit*, que corresponde às imagens dos blocos de terra e armadilhas. Atualiza também a posição de todos os blocos se baseando no valor do *scroll* vertical.  
- O método ***reset_map*** reinicia a grelha para o modo inicial (só paredes).

####UserInterface
Esta classe representa a *User Interface* do jogo. Inclui métodos para que apresentam a vida do jogador e a sua pontuação. A vida do jogador é representada por corações vermelhos e a pontuação por uma fonte customizada. 
- O método ***\__init__*** recebe dois parâmetros, *player* e *world* que são os objetos com as classes *Player* e *WorldMap* que são instanciados ao correr o jogo. Aqui também são carregadas as imagens que representam a vida do jogador e o tipo de letra utilizado para a pontuação. 
- ***display_hp*** é o método que é responsável por mostrar a vida do jogador. Recebe o parâmetro *“curr_hp”*, o qual representa as vidas que o jogador ainda tem numa sessão. 
- O método ***draw_score*** é responsável por apresentar o score do jogador dentro do ecrã de jogo. O cálculo da pontuação do jogador é feito através da soma de todo *scroll* feito pelo jogador, ou seja, quanto mais fundo o jogador conseguir atingir, maior o seu score e se o jogador ficar apenas parado numa plataforma o seu score permanece igual. Através do método *size* da classe Font é possível obter o tamanho que o texto iria ocupar no ecrã em pixéis e é utilizado esse valor para centrar constantemente o valor de score no ecrã. 
  - **Nota**: No enunciado do projeto a pontuação do jogador era calculada com base no tempo em que a personagem estava viva, mas com as implementações que foram feitas, este sistema de pontuação não iria funcionar. 

- O método ***draw_ui*** “desenha” toda a *User Interface*. Aqui são chamados os métodos *“draw_score”* e *“display_hp”*. 

####Button 
Como a biblioteca *Pygame* não oferece nenhuma solução simples para botões, foi desenvolvida esta classe para representar os botões usados em todo o jogo.
- ***\__init__*** é o método que inicializa a classe, este recebe vários parâmetros como a posição, tamanhos estando, ou não, com o rato sobre o botão e a imagem desse botão.  
- O método ***update*** é responsável por desenhar os botões no ecrã de jogo. Quando é atualizado o tamanho de o botão este método redesenha-o no ecrã. 
- ***checkMousePosition*** é o método responsável por verificar a posição do cursor e atualizar o tamanho dos botões quando o cursor passa por cima destes. 
  - Este método recebe o parâmetro *mousePos*, que representa a posição atual do rato, a posição atual do rato é obtida através do método *get_pos* associado ao objeto *mouse* da biblioteca de *Pygame*.

####WindowSelector 
A classe *WindowSelector* é responsável por orientar os diferentes menus/estados no jogo. 
- O método ***\__init__*** inicializa vários objetos e botões. Aqui está a variável curr_menu que indica o menu/estado do jogo. 
- ***main_menu*** é o método responsável por exibir o ecrã de *“main menu”* e detetar os cliques dos botões. É responsável também por detetar eventos como mudança de janela (através dos botões) e saída do jogo.
- O método ***play_game*** representa um *loop* no qual o jogo é jogado. Aqui é atualizado o estado do jogo, detetando se o jogador perde ou se sai diretamente do jogo. 
- O método ***game_over*** apresenta o ecrã *“Game Over”*, o qual corre só durante um pequeno período e no fim faz a transição para o menu de *leaderboard*. 
- ***leaderboard*** é o método que apresenta o ecrã onde aparece as pontuações dos 10 jogadores com a melhor pontuação. Se a pontuação do jogador for melhor que alguma destas, o jogador é proposto a escrever as suas iniciais (máximo 4) e é introduzido nesta lista. Caso não haja um *highscore* a janela de *leaderboard* aparece durante alguns segundos antes de voltar para o *main menu*. 

#####Execução de Código 

Para a execução do jogo, é inicializado o *Pygame*, o relógio do jogo, é criado o ecrã de jogo com as dimensões pedidas no enunciado, algumas alterações e implementações na janela de jogo, música é executada e é criado o *loop “while window_running”* que é responsável por indicar a janela/função que está a correr de momento. 

#####Referências  
Neste projeto todas as referências que usufruí foi de tutoriais que encontrei no Youtube: 
Tutorial geral de como fazer um jogo 2D em *Python*: 
- https://www.youtube.com/watch?v=Ongc4EVqRjo&ab_channel=CodingWithRuss 

- https://www.youtube.com/watch?v=5FMPAt0n3Nc&list=RDCMUCPrRY0S-VzekrJK7I7F4-Mg&start_radio=1&t=653s&ab_channel=CodingWithRuss 

- https://www.youtube.com/watch?v=FfWpgLFMI7w&ab_channel=freeCodeCamp.org

Tutorial de como fazer botões e janelas: 
- https://www.youtube.com/watch?v=GMBqjxcKogA&t=230s&ab_channel=BaralTech 

- https://www.youtube.com/watch?v=2iyx8_elcYg&t=812s&ab_channel=CodingWithRuss 

- https://www.youtube.com/watch?v=G8MYGDf_9ho&t=581s&ab_channel=CodingWithRuss 

Salvo as referências dos tutoriais, também tive trocas de ideias e a orientação do meu explicador. 