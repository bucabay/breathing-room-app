export type PanelPage = "apps" | "space" | "activity";
export interface PanelNavigation {
  page: PanelPage;
  settings?: boolean;
  filter?: "all" | "files" | "processes";
  search?: string;
  appId?: string;
  eventId?: number;
  section?: "writers" | "timeline" | "feed";
}

export function panelNavigationUrl(destination: PanelNavigation): string {
  const query=new URLSearchParams({page:destination.page});
  for(const [key,value] of Object.entries(destination)) {
    if(key!=="page" && value!==undefined)query.set(key,String(value));
  }
  return `/?${query}`;
}

export function panelNavigationFromUrl(search:string):PanelNavigation|null {
  const query=new URLSearchParams(search);const page=query.get("page");
  if(page!=="apps" && page!=="space" && page!=="activity")return null;
  const destination:PanelNavigation={page};
  if(query.get("settings")==="true")destination.settings=true;
  const filter=query.get("filter");if(filter==="all"||filter==="files"||filter==="processes")destination.filter=filter;
  const section=query.get("section");if(section==="writers"||section==="timeline"||section==="feed")destination.section=section;
  if(query.has("search"))destination.search=query.get("search")!.slice(0,500);
  if(query.has("appId"))destination.appId=query.get("appId")!.slice(0,1000);
  const id=Number(query.get("eventId"));if(Number.isSafeInteger(id)&&id>0)destination.eventId=id;
  return destination;
}
