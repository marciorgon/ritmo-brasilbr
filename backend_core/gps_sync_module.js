import { createClient } from '@supabase/supabase-js'

// 1. CONFIGURAÇÃO DO CLIENTE (Substitua pelas suas chaves do Supabase)
const SUPABASE_URL = 'https://sua-url.supabase.co'
const SUPABASE_KEY = 'sua-chave-anon-public'
const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)

/**
 * RITMO BRASIL - MONITOR DE GPS SINCRONIZADO
 * Este módulo gerencia o envio do celular e a recepção no computador.
 */

export const GPSMonitor = {
  
  // A. LADO DO CELULAR (ENVIAR)
  async startLiveSession(userId, workoutId) {
    console.log("🚀 Iniciando sessão de GPS no celular...");
    
    // Simula a coleta de GPS (No app real, isso vem do Geolocator)
    const watchId = navigator.geolocation.watchPosition(
      async (position) => {
        const { latitude, longitude, speed } = position.coords;
        
        // Envia para o Supabase Realtime
        const { error } = await supabase
          .from('live_session_coords')
          .insert([
            { 
              user_id: userId, 
              workout_id: workoutId, 
              lat: latitude, 
              lng: longitude, 
              speed: speed,
              timestamp: new Date().toISOString()
            }
          ]);
          
        if (error) console.error("Erro ao sincronizar GPS:", error);
      },
      (err) => console.error(err),
      { enableHighAccuracy: true }
    );
    
    return watchId;
  },

  // B. LADO DO COMPUTADOR (RECEBER)
  subscribeToLiveSession(workoutId, onUpdate) {
    console.log(`📡 Monitorando treino ${workoutId} no computador...`);
    
    const channel = supabase
      .channel(`live-workout-${workoutId}`)
      .on(
        'postgres_changes', 
        { 
          event: 'INSERT', 
          schema: 'public', 
          table: 'live_session_coords',
          filter: `workout_id=eq.${workoutId}` 
        }, 
        (payload) => {
          // Quando o celular envia um ponto, o computador recebe aqui instantaneamente
          onUpdate(payload.new);
        }
      )
      .subscribe();
      
    return channel;
  }
};
