import statistics

class RBEngine:
    """
    Núcleo Matemático do Ritmo Brasil (RB).
    Especializado em Ciência de Dados aplicada ao Esporte.
    """

    def __init__(self, user_id):
        self.user_id = user_id

    # 1. CÁLCULO DE RITMO ALVO ADAPTATIVO
    def calculate_target_pace(self, recent_paces_seconds, level='intermediario', objective='5km', fatigue_score=0.0):
        """
        recent_paces_seconds: Lista de paces (segundos por km) dos últimos 7 treinos.
        fatigue_score: Índice de fadiga (0.0 a 1.0).
        """
        if not recent_paces_seconds:
            return "05:30" # Default base

        # Média ponderada (Recent Treinos valem mais)
        # Ex: [Pace-7, Pace-6... Pace-1 (Ontem)]
        weights = [i/sum(range(1, len(recent_paces_seconds)+1)) for i in range(1, len(recent_paces_seconds)+1)]
        weighted_avg = sum(p * w for p, w in zip(recent_paces_seconds, weights))

        # Fatores de Progressão
        factors = {
            'iniciante': 1.02,     # Foco em volume, ritmo conservador
            'intermediario': 1.0,  # Manutenção e leve ganho
            'avançado': 0.98       # Busca agressiva por velocidade
        }
        
        # Ajuste por fadiga
        # Se fadiga for alta, aumenta o pace (corre mais devagar)
        fatigue_adjustment = 1.0 + (fatigue_score * 0.1) 
        
        target_seconds = weighted_avg * factors.get(level, 1.0) * fatigue_adjustment
        
        return self._seconds_to_pace(target_seconds)

    # 2. ÍNDICE RB (0 a 100)
    def calculate_rb_index(self, consistency, pace_evolution, goal_compliance, recovery, frequency):
        """
        Valores de entrada de 0 a 100.
        """
        score = (consistency * 0.30) + (pace_evolution * 0.25) + \
                (goal_compliance * 0.20) + (recovery * 0.15) + \
                (frequency * 0.10)
        return round(score, 2)

    # 3. DETECÇÃO DE FADIGA SISTÊMICA
    def detect_fatigue(self, avg_hr_delta, performance_delta, cadence_delta):
        """
        avg_hr_delta: % de aumento da FC média para o mesmo pace.
        performance_delta: % de queda de pace no mesmo esforço perceptivo.
        cadence_delta: % de redução na cadência (passadas por minuto).
        """
        # Score de 0 a 1
        fatigue_score = (avg_hr_delta * 0.4) + (performance_delta * 0.4) + (cadence_delta * 0.2)
        
        return {
            "score": round(fatigue_score, 2),
            "status": "RECOVERY_MODE" if fatigue_score > 0.7 else "READY",
            "action": "Ativar semana regenerativa" if fatigue_score > 0.7 else "Seguir plano"
        }

    # 4. MONITOR DE CARGA SEMANAL (REGRA DOS 10%)
    def validate_weekly_load(self, last_week_km, planned_week_km):
        max_allowed = last_week_km * 1.10
        if planned_week_km > max_allowed:
            return {
                "safe": False,
                "recommended": max_allowed,
                "warning": "Aumento de carga superior a 10%. Risco de lesão detectado."
            }
        return {"safe": True}

    # Helpers
    def _seconds_to_pace(self, seconds):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _pace_to_seconds(self, pace_str):
        m, s = map(int, pace_str.split(':'))
        return m * 60 + s

# Simulação de Teste
if __name__ == "__main__":
    engine = RBEngine(user_id="user_01")
    
    # Testando ritmo alvo com leve fadiga
    paces = [340, 335, 330, 328, 325, 320, 315] # Evoluindo
    target = engine.calculate_target_pace(paces, level='avançado', fatigue_score=0.2)
    print(f"Novo Ritmo Alvo: {target} min/km")
    
    # Testando Índice RB
    rb_index = engine.calculate_rb_index(90, 80, 85, 70, 100)
    print(f"Índice RB do Atleta: {rb_index}/100")
