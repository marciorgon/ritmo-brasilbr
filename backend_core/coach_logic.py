import json
from datetime import datetime

class RitmoCoach:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.name = "RitmoCoach"
        self.tone = "Motivador e Brasileiro"

    def analyze_session(self, session_data, goal_data):
        """
        Analítica de performance e geração de feedback via IA simulada.
        
        session_data: {distancia, tempo, ritmo_medio, fc_media}
        goal_data: {distancia_alvo, ritmo_alvo}
        """
        dist_real = session_data['distancia']
        dist_alvo = goal_data['distancia_alvo']
        pace_real = self._pace_to_seconds(session_data['ritmo_medio'])
        pace_alvo = self._pace_to_seconds(goal_data['ritmo_alvo'])

        # Cálculo de performance
        dist_diff = (dist_real / dist_alvo) - 1
        pace_diff = (pace_alvo / pace_real) - 1  # Pace menor é melhor

        # Lógica de Selo
        if dist_diff >= 0 and pace_diff >= 0.05:
            seal = "EXCELENTE"
            message = f"Mandou muito bem hoje 🔥! Você superou o ritmo alvo em {abs(pace_diff):.0%}. Mantém essa pegada!"
        elif dist_diff >= -0.1 and pace_diff >= -0.1:
            seal = "CONSISTENTE"
            message = "A consistência está fazendo efeito! Treino entregue conforme o plano. Amanhã tem mais 💪."
        else:
            seal = "PRECISA MELHORAR"
            message = "Hoje foi mais pesado, né? Normal. O importante é não parar. Vamos ajustar o ritmo de amanhã para você recuperar forte."

        return {
            "seal": seal,
            "feedback": message,
            "adjustment_needed": dist_diff < -0.2 or pace_diff < -0.2
        }

    def _pace_to_seconds(self, pace_str):
        # Converte "5:20" para 320 segundos
        m, s = map(int, pace_str.split(':'))
        return m * 60 + s

# --- EXEMPLO DE USO ---
if __name__ == "__main__":
    player_profile = {"nome": "Marcio", "nivel": "intermediario", "objetivo": "5km"}
    coach = RitmoCoach(player_profile)

    last_run = {"distancia": 5.02, "ritmo_medio": "5:19", "tempo": "26:42"}
    target = {"distancia_alvo": 5.0, "ritmo_alvo": "5:30"}

    result = coach.analyze_session(last_run, target)
    print(f"[{coach.name}]: {result['feedback']}")
    print(f"Selo de Performance: {result['seal']}")
