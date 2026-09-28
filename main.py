import random
import copy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.metrics import sp, dp

# Dados base do Quiz
PERGUNTAS_BASE = [
    {
        "pergunta": "QUAL SUA ESTAÇÃO PREFERIDA?",
        "opcoes": [
            ("INVERNO", "S"),
            ("PRIMAVERA", "L"),
            ("VERÃO", "G"),
            ("OUTONO", "C")
        ]
    },
    {
        "pergunta": "QUAL SEU ELEMENTO PREFERIDO?",
        "opcoes": [
            ("TERRA", "C"),
            ("AR", "L"),
            ("ÁGUA", "G"),
            ("FOGO", "S")
        ]
    },
    {
        "pergunta": "ESCOLHA UM PASSEIO?",
        "opcoes": [
            ("DESFILE DE MODA", "S"),
            ("LIVRARIA", "C"),
            ("ZOOLÓGICO", "L"),
            ("PARQUE DE DIVERSÕES", "G")
        ]
    },
    {
        "pergunta": "QUAL SEU AMBIENTE PREFERIDO?",
        "opcoes": [
            ("PRAIA", "G"),
            ("CIDADE", "S"),
            ("BOSQUE", "L"),
            ("MONTANHA", "C")
        ]
    },
    {
        "pergunta": "QUEM É VOCÊ NA PROVA?",
        "opcoes": [
            ("NÃO PASSO E NEM PEÇO COLA", "C"),
            ("PASSO E PEÇO COLA", "G"),
            ("SÓ PASSO COLA", "L"),
            ("SÓ PEÇO COLA", "S")
        ]
    },
    {
        "pergunta": "QUAL ANIMAL VOCÊ SERIA?",
        "opcoes": [
            ("CACHORRO", "G"),
            ("GATO", "S"),
            ("LEBRE", "L"),
            ("GOLFINHO", "C")
        ]
    },
    {
        "pergunta": "QUAL ARMA VOCÊ CARREGARIA?",
        "opcoes": [
            ("REVÓLVER", "S"),
            ("ESPADA", "G"),
            ("ARCO E FLECHA", "C"),
            ("VENENO", "L")
        ]
    },
    {
        "pergunta": "QUAL SEU ESTILO MUSICAL?",
        "opcoes": [
            ("ROCK & ROLL", "S"),
            ("MÚSICA CLÁSSICA", "C"),
            ("COUNTRY", "L"),
            ("DANCE/POP", "G")
        ]
    },
    {
        "pergunta": "QUAL PROFISSÃO VOCÊ PREFERE?",
        "opcoes": [
            ("MÉDICO", "L"),
            ("PROFESSOR", "C"),
            ("POLICIAL", "G"),
            ("JUIZ", "S")
        ]
    },
    {
        "pergunta": "O QUE LHE ATRAI MAIS?",
        "opcoes": [
            ("LEALDADE", "L"),
            ("JUSTIÇA", "G"),
            ("LIDERANÇA", "S"),
            ("CONHECIMENTO", "C")
        ]
    }
]

CASAS_NOMES = {
    "C": "CORVINAL",
    "G": "GRIFINÓRIA",
    "L": "LUFA-LUFA",
    "S": "SONSERINA"
}

# Cores exigidas para cada casa
CASAS_CORES = {
    "S": (0, 1, 0, 1),    # Verde (Sonserina)
    "G": (1, 0, 0, 1),    # Vermelho (Grifinória)
    "C": (0, 0.4, 1, 1),  # Azul (Corvinal)
    "L": (1, 1, 0, 1)     # Amarelo (Lufa-Lufa)
}

class QuizHogwartsApp(App):
    def build(self):
        self.evento_piscar = None
        self.labels_vencedoras = []
        
        self.layout_principal = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )
        
        self.reiniciar_jogo()
        return self.layout_principal

    def reiniciar_jogo(self, instance=None):
        # Para o pisca-pisca se estiver ativo
        if self.evento_piscar:
            self.evento_piscar.cancel()
            self.evento_piscar = None

        self.labels_vencedoras = []
        
        # Reseta pontuação
        self.pontuacao = {"C": 0, "G": 0, "L": 0, "S": 0}
        self.indice_pergunta = 0

        # Cria uma cópia e embaralha as perguntas e respostas
        self.perguntas = copy.deepcopy(PERGUNTAS_BASE)
        random.shuffle(self.perguntas)
        for p in self.perguntas:
            random.shuffle(p["opcoes"])

        self.exibir_pergunta()

    def exibir_pergunta(self):
        self.layout_principal.clear_widgets()

        pergunta_atual = self.perguntas[self.indice_pergunta]

        # Rótulo do Progresso
        label_progresso = Label(
            text=f"PERGUNTA {self.indice_pergunta + 1} DE {len(self.perguntas)}",
            font_size=sp(16),
            color=(1, 1, 1, 1),
            size_hint_y=0.1
        )
        self.layout_principal.add_widget(label_progresso)

        # Rótulo do Texto da Pergunta
        label_pergunta = Label(
            text=pergunta_atual["pergunta"],
            font_size=sp(22),
            color=(1, 1, 1, 1),
            size_hint_y=0.25,
            halign='center',
            valign='middle'
        )
        label_pergunta.bind(size=lambda instance, val: setattr(instance, 'text_size', val))
        self.layout_principal.add_widget(label_pergunta)

        # Layout com as 4 opções de resposta
        layout_opcoes = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=0.65)

        for texto_opcao, casa_code in pergunta_atual["opcoes"]:
            btn_opcao = Button(
                text=texto_opcao,
                font_size=sp(16),
                color=(1, 1, 1, 1)
            )
            # Permite que textos longos de botões façam quebra de linha
            btn_opcao.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0] - dp(20), None)))
            btn_opcao.halign = 'center'
            btn_opcao.valign = 'middle'
            
            # Associa o clique à função de processar a resposta passando a casa
            btn_opcao.bind(on_press=lambda inst, c=casa_code: self.processar_resposta(c))
            layout_opcoes.add_widget(btn_opcao)

        self.layout_principal.add_widget(layout_opcoes)

    def processar_resposta(self, casa):
        self.pontuacao[casa] += 1
        self.indice_pergunta += 1

        if self.indice_pergunta < len(self.perguntas):
            self.exibir_pergunta()
        else:
            self.exibir_resultado()

    def exibir_resultado(self):
        self.layout_principal.clear_widgets()

        # Ordena as pontuações em ordem decrescente
        resultado_ordenado = sorted(self.pontuacao.items(), key=lambda item: item[1], reverse=True)
        
        # Maior pontuação para identificar vencedores (mesmo em empate)
        maior_pontuacao = resultado_ordenado[0][1]

        label_titulo = Label(
            text="RESULTADO DO CHAPÉU SELETOR:",
            font_size=sp(20),
            color=(1, 1, 1, 1),
            size_hint_y=0.15,
            halign='center'
        )
        self.layout_principal.add_widget(label_titulo)

        layout_ranking = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.7)

        total_perguntas = len(self.perguntas)

        for casa_code, pontos in resultado_ordenado:
            porcentagem = int((pontos / total_perguntas) * 100)
            nome_casa = CASAS_NOMES[casa_code]
            
            # Formato da mensagem solicitado
            texto_resultado = f"VOCÊ É {porcentagem}% {nome_casa}"
            
            lbl_casa = Label(
                text=texto_resultado,
                font_size=sp(20),
                color=CASAS_CORES[casa_code],  # Aplica cor específica da casa
                halign='center',
                valign='middle'
            )
            lbl_casa.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
            layout_ranking.add_widget(lbl_casa)

            # Adiciona à lista de piscar se for o vencedor (ou empatado no topo)
            if pontos == maior_pontuacao:
                self.labels_vencedoras.append(lbl_casa)

        self.layout_principal.add_widget(layout_ranking)

        # Inicia o pisca-pisca de 0,5 segundo para o(s) vencedor(es)
        self.evento_piscar = Clock.schedule_interval(self.piscar_vencedores, 0.5)

        # Botão para jogar novamente
        btn_reiniciar = Button(
            text="JOGAR NOVAMENTE",
            font_size=sp(18),
            color=(1, 1, 1, 1),
            size_hint_y=0.15
        )
        btn_reiniciar.bind(on_press=self.reiniciar_jogo)
        self.layout_principal.add_widget(btn_reiniciar)

    def piscar_vencedores(self, dt):
        for label in self.labels_vencedoras:
            r, g, b, a = label.color
            label.color = (r, g, b, 0 if a == 1 else 1)

if __name__ == "__main__":
    QuizHogwartsApp().run()
