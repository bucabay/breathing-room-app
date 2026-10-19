/** Align a panel destination below the sticky status dock, after layout settles. */
export function scrollPanelDestination(findTarget?:()=>HTMLElement|null):()=>void {
  let stopped=false;let frame=0;
  const main=document.querySelector<HTMLElement>(".main-content");
  const clearSpace=()=>{main?.removeAttribute("data-panel-scroll");main?.style.removeProperty("--panel-scroll-extra");main?.style.removeProperty("--panel-scroll-base");};
  clearSpace();
  const basePadding=main?getComputedStyle(main).paddingBottom:"130px";
  const align=()=>{
    if(stopped)return;
    const target=findTarget?.();
    if(findTarget && !target)return;
    const dock=document.querySelector<HTMLElement>(".status-dock");
    const offset=dock?Math.max(0,parseFloat(getComputedStyle(dock).top)||0)+dock.getBoundingClientRect().height+16:16;
    const top=target?Math.max(0,window.scrollY+target.getBoundingClientRect().top-offset):0;
    if(target && main) {
      // A last item in a filtered feed otherwise hits the document's scroll limit
      // before its heading can reach the status dock. Add only the missing room.
      const extra=parseFloat(main.style.getPropertyValue("--panel-scroll-extra"))||0;
      const maximum=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
      const needed=Math.max(0,Math.ceil(top-maximum+extra));
      if(needed!==extra){main.style.setProperty("--panel-scroll-base",basePadding);main.style.setProperty("--panel-scroll-extra",`${needed}px`);main.setAttribute("data-panel-scroll","");}
    }
    if(Math.abs(window.scrollY-top)>1)window.scrollTo({top,behavior:"instant"});
  };
  const schedule=()=>{cancelAnimationFrame(frame);frame=requestAnimationFrame(()=>{frame=requestAnimationFrame(align);});};
  const observer=new ResizeObserver(schedule);
  const dock=document.querySelector(".status-dock");
  if(main)observer.observe(main);if(dock)observer.observe(dock);
  const stop=()=>{stopped=true;cancelAnimationFrame(frame);observer.disconnect();clearTimeout(timeout);for(const event of events)window.removeEventListener(event,stop);};
  const events=["wheel","touchstart","pointerdown","keydown"];
  for(const event of events)window.addEventListener(event,stop,{passive:true});
  const timeout=setTimeout(stop,1500);
  void document.fonts.ready.then(()=>{if(!stopped)schedule();});
  schedule();return()=>{stop();clearSpace();};
}
