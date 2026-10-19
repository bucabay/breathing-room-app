import {ArrowUpRight,Sparkles} from "lucide-react";

export function AiCareCard({placement="home",onOpen}:{placement?:"home"|"sidebar";onOpen:()=>void}){
  return <button type="button" className={`ai-care-card ${placement==="sidebar"?"sidebar-ai":"finding panel"}`} onClick={onOpen} aria-label="Explore AI care" aria-haspopup="dialog">
    {placement==="sidebar"?<span className="ai-care-eyebrow"><Sparkles size={20} aria-hidden="true"/>AI Care</span>:<span className="finding-icon orange"><Sparkles/></span>}
    {placement!=="sidebar"&&<strong className="ai-care-card-title">Automatic daily cleanup</strong>}
    <span className="ai-care-card-description">{placement==="sidebar"?"Daily cleanup. Only what you approve.":"Choose a time. Clean approved items, find new cleanup opportunities and see what’s filling your disk."}</span>
    <span className="ai-care-card-action">Explore AI care <ArrowUpRight size={16}/></span>
  </button>;
}
