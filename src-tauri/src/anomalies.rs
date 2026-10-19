//! Sample-driven alert episodes. Acknowledged episodes stay quiet until recovery.
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "camelCase", default)]
pub struct AlertConfig {
    pub enabled: bool,
    pub cpu_enabled: bool,
    pub writes_enabled: bool,
    pub cpu_threshold: f64,
    pub write_mb_per_second: f64,
    pub sustained_seconds: u64,
    pub cooldown_seconds: u64,
}
impl Default for AlertConfig {
    fn default() -> Self {
        Self { enabled: true, cpu_enabled: true, writes_enabled: true, cpu_threshold: 100.0,
            write_mb_per_second: 50.0, sustained_seconds: 30, cooldown_seconds: 300 }
    }
}
impl AlertConfig {
    pub fn validate(&self) -> Result<(), String> {
        if !self.cpu_threshold.is_finite() || !(1.0..=10000.0).contains(&self.cpu_threshold)
            || !self.write_mb_per_second.is_finite() || !(0.1..=10000.0).contains(&self.write_mb_per_second)
            || !(5..=600).contains(&self.sustained_seconds) || !(0..=3600).contains(&self.cooldown_seconds) {
            return Err("Choose valid alert thresholds, 5–600 seconds sustained, and 0–3600 seconds cooldown".into());
        }
        Ok(())
    }
}
#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Anomaly {
    pub id: u64, pub kind: String, pub name: String, pub path: String,
    pub value: f64, pub threshold: f64, pub since: u64, pub acknowledged: bool,
}
struct Episode { since: u64, recovery: Option<u64>, alert: Option<Anomaly> }
#[derive(Default)]
pub struct Detector {
    episodes: HashMap<String, Episode>, sequence: u64, last_sample: Option<u64>,
    config: Option<AlertConfig>, last_open: Option<u64>,
}
impl Detector {
    pub fn reset(&mut self) { self.episodes.clear(); self.last_sample = None; }
    pub fn expire_stale(&mut self, at:u64, interval:u64) {
        if self.last_sample.is_some_and(|last|at.saturating_sub(last)>interval*2+2) {self.reset();}
    }
    pub fn acknowledge(&mut self) {
        for episode in self.episodes.values_mut() {
            if let Some(alert) = &mut episode.alert { alert.acknowledged = true; }
        }
    }
    pub fn active(&self) -> Vec<Anomaly> {
        let mut alerts: Vec<_> = self.episodes.values().filter_map(|e|e.alert.clone()).collect();
        alerts.sort_by_key(|a|a.id); alerts
    }
    /// Values are (stable app identity, display name, path, metric kind, value).
    pub fn sample(&mut self, at: u64, interval: u64, config: &AlertConfig, values: Vec<(String,String,String,String,f64)>) {
        if self.config.as_ref() != Some(config) {
            self.reset(); self.config = Some(config.clone());
        }
        if !config.enabled { self.reset(); return; }
        if self.last_sample.is_some_and(|last| at <= last || at-last > interval*2+2) { self.reset(); }
        self.last_sample = Some(at);
        let mut seen = HashSet::new();
        for (identity,name,path,kind,value) in values {
            if !value.is_finite() || (kind == "cpu" && !config.cpu_enabled) || (kind == "writes" && !config.writes_enabled) { continue; }
            let threshold = if kind == "cpu" { config.cpu_threshold } else { config.write_mb_per_second*1e6 };
            let key = format!("{kind}:{identity}"); seen.insert(key.clone());
            if value < threshold && !self.episodes.contains_key(&key) { continue; }
            let episode = self.episodes.entry(key.clone()).or_insert(Episode { since:at, recovery:None, alert:None });
            if let Some(alert) = &mut episode.alert { alert.value = value; }
            if value < threshold*0.8 {
                let recovery = *episode.recovery.get_or_insert(at);
                if episode.alert.is_none() || at.saturating_sub(recovery) >= config.sustained_seconds { self.episodes.remove(&key); }
                continue;
            }
            episode.recovery = None;
            if episode.alert.is_none() && value < threshold { self.episodes.remove(&key); }
            else if episode.alert.is_none() && at.saturating_sub(episode.since) >= config.sustained_seconds {
                self.sequence += 1;
                episode.alert = Some(Anomaly { id:self.sequence,kind,name,path,value,threshold,since:episode.since,acknowledged:false });
            }
        }
        // Missing metrics/processes cannot sustain an alert.
        self.episodes.retain(|key,_|seen.contains(key));
    }
    pub fn can_open(&self, at:u64, cooldown:u64) -> bool {
        self.active().iter().any(|a|!a.acknowledged) && !self.last_open.is_some_and(|last|at.saturating_sub(last)<cooldown)
    }
    pub fn mark_opened(&mut self, at:u64) { self.last_open=Some(at); self.acknowledge(); }
    #[cfg(test)]
    pub fn should_open(&mut self, at:u64, cooldown:u64) -> bool {
        if !self.can_open(at,cooldown) {return false;} self.mark_opened(at); true
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn sample(d:&mut Detector,t:u64,v:f64,c:&AlertConfig) {
        d.sample(t,5,c,vec![("app".into(),"App".into(),"/App.app".into(),"cpu".into(),v)]);
    }
    #[test] fn sustained_acknowledged_and_rearmed() {
        let c=AlertConfig{ sustained_seconds:10,..Default::default() }; let mut d=Detector::default();
        sample(&mut d,100,120.0,&c); sample(&mut d,105,120.0,&c); assert!(d.active().is_empty());
        sample(&mut d,110,120.0,&c); assert!(d.should_open(110,0)); assert!(!d.should_open(115,0));
        for t in [115,120,125] {sample(&mut d,t,20.0,&c);} assert!(d.active().is_empty());
        for t in [130,135,140] {sample(&mut d,t,120.0,&c);} assert!(d.should_open(140,0));
    }
    #[test] fn gaps_missing_metrics_and_config_changes_reset() {
        let mut c=AlertConfig{ sustained_seconds:10,..Default::default() }; let mut d=Detector::default();
        sample(&mut d,100,120.0,&c); sample(&mut d,200,120.0,&c); assert!(d.active().is_empty());
        sample(&mut d,205,120.0,&c); d.sample(210,5,&c,vec![]); sample(&mut d,215,120.0,&c); assert!(d.active().is_empty());
        c.cpu_threshold=110.0; sample(&mut d,220,120.0,&c); assert!(d.active().is_empty());
    }
    #[test] fn cooldown_queues_new_episode_and_hysteresis() {
        let c=AlertConfig{ sustained_seconds:5,..Default::default() }; let mut d=Detector::default();
        sample(&mut d,100,120.0,&c); sample(&mut d,105,120.0,&c); assert!(d.should_open(105,30));
        sample(&mut d,110,90.0,&c); assert_eq!(d.active().len(),1);
        d.sample(115,5,&c,vec![]); sample(&mut d,120,120.0,&c); sample(&mut d,125,120.0,&c);
        assert!(!d.should_open(125,30)); assert!(d.should_open(135,30));
    }
    #[test] fn invalid_preferences_rejected_and_old_preferences_default() {
        let c:AlertConfig=serde_json::from_str("{}").unwrap(); assert!(c.validate().is_ok());
        assert!(AlertConfig{ cpu_threshold:f64::NAN,..c }.validate().is_err());
    }
    #[test] fn disk_writes_and_cpu_have_independent_episodes() {
        let c=AlertConfig{ sustained_seconds:5,..Default::default() };let mut d=Detector::default();
        let values=vec![("app".into(),"App".into(),"/App.app".into(),"writes".into(),60e6),("app".into(),"App".into(),"/App.app".into(),"cpu".into(),120.0)];
        d.sample(100,5,&c,values.clone());d.sample(105,5,&c,values);assert_eq!(d.active().len(),2);
        d.acknowledge();assert!(!d.can_open(105,0));
        let disabled=AlertConfig{enabled:false,..c};d.sample(110,5,&disabled,vec![]);assert!(d.active().is_empty());
    }
    #[test] fn dip_before_trigger_requires_a_new_full_duration() {
        let c=AlertConfig{ sustained_seconds:10,..Default::default() };let mut d=Detector::default();
        sample(&mut d,100,120.0,&c);sample(&mut d,105,90.0,&c);sample(&mut d,110,120.0,&c);sample(&mut d,115,120.0,&c);
        assert!(d.active().is_empty());sample(&mut d,120,120.0,&c);assert_eq!(d.active().len(),1);
    }
    #[test] fn stale_episode_cannot_open_after_sleep() {
        let c=AlertConfig{ sustained_seconds:5,..Default::default() };let mut d=Detector::default();
        sample(&mut d,100,120.0,&c);sample(&mut d,105,120.0,&c);assert!(d.can_open(105,0));
        d.expire_stale(200,5);assert!(!d.can_open(200,0));assert!(d.active().is_empty());
    }
}
