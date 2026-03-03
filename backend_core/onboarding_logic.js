import { createClient } from '@supabase/supabase-js'

// CONFIGURAÇÃO (Trocar pelas suas chaves do Supabase)
const SUPABASE_URL = 'https://sua-url.supabase.co'
const SUPABASE_KEY = 'sua-chave-anon-public'
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

/**
 * RITMO BRASIL - MOTOR DE ONBOARDING INTELIGENTE
 * Este módulo transforma respostas em um plano de 4 semanas no banco de dados.
 */

export const OnboardingEngine = {

    async generateInitialPlan(userId, profileData) {
        console.log("🧠 Gerando plano de 4 semanas para:", profileData.name);

        const { level, objective, frequency, timeAvailable } = profileData;

        // 1. DEFINIÇÃO DE BASE (Baseado em nível e objetivo)
        let baseDistance = objective === '5km' ? 3.0 : objective === '10km' ? 6.0 : 2.0;
        let basePace = level === 'iniciante' ? "08:00" : level === 'intermediario' ? "06:30" : "05:00";

        const sessionsPerWeek = parseInt(frequency.replace('x', ''));
        let workouts = [];

        // 2. GERAÇÃO DE 4 SEMANAS (Regra do Ritmo Brasil)
        for (let week = 1; week <= 4; week++) {
            const isRegenerative = week === 4; // Semana 4 é sempre regenerativa (Recuperação)
            const loadFactor = isRegenerative ? 0.7 : 1.0 + (week - 1) * 0.1; // Evolução de 10% por semana

            for (let day = 1; day <= 7; day++) {
                // Exemplo de distribuição (Seg, Qua, Sex para 3x na semana)
                if ((sessionsPerWeek === 3 && [1, 3, 5].includes(day)) ||
                    (sessionsPerWeek === 4 && [1, 2, 4, 6].includes(day))) {

                    workouts.push({
                        user_id: userId,
                        scheduled_date: this._getNextDate(week, day),
                        workout_type: this._getWorkoutType(day, week),
                        target_distance_km: parseFloat((baseDistance * loadFactor).toFixed(2)),
                        target_pace: basePace,
                        status: 'PENDING',
                        is_regenerative_week: isRegenerative
                    });
                }
            }
        }

        // 3. INSERÇÃO NO SUPABASE
        const { data, error } = await supabase
            .from('training_schedule')
            .insert(workouts);

        if (error) {
            console.error("❌ Erro ao salvar plano:", error);
            return { success: false, error };
        }

        // 4. ATUALIZAR STATUS DO USUÁRIO
        await supabase.from('users').update({ profile_data: profileData }).eq('id', userId);

        return { success: true, message: "Plano gerado com sucesso! 4 semanas prontas." };
    },

    // Helpers de lógica secundária
    _getNextDate(week, day) {
        const d = new Date();
        d.setDate(d.getDate() + (week - 1) * 7 + day);
        return d.toISOString().split('T')[0];
    },

    _getWorkoutType(day, week) {
        if (day === 1) return 'Rodagem Leve';
        if (day === 4 || day === 3) return 'Intervalado (Explosão)';
        if (day === 6 || day === 5) return 'Longão de Base';
        return 'Treino de Ritmo';
    }
};
