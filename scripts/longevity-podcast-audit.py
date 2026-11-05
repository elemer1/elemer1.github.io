#!/usr/bin/env python3
"""Longevity-podcast show-notes audit cited in "The Particle Builds It. The Pressure Detonates It."

Downloads the public RSS feeds of ten prevention/longevity podcasts (feed URLs from the
Apple Podcasts directory) and counts, per podcast, the episodes whose title or show notes
mention lipids (apoB, LDL, Lp(a), lipoprotein, cholesterol), blood pressure (blood pressure,
hypertension) and isometric training (isometric, wall sit/squat, handgrip), and how many
isometric mentions fall within 400 characters of a blood-pressure term.

Usage:
    python3 scripts/longevity-podcast-audit.py --data-dir /tmp/rss [--json out.json]

Show notes are summaries, not transcripts: absence from the notes is weaker evidence than
absence from what was said.
"""
import argparse, urllib.request, pathlib
FEEDS = {
    "attia_drive": "https://rss.libsyn.com/shows/121729/destinations/713489.xml",
    "huberman_lab": "https://feeds.megaphone.fm/hubermanlab",
    "foundmyfitness": "https://rss.libsyn.com/shows/51714/destinations/184296.xml",
    "bryan_johnson": "https://feeds.megaphone.fm/bryanjohnsonpodcast",
    "hyman": "https://feeds.megaphone.fm/thedoctorsfarmacy",
    "simon_hill_proof": "https://feeds.megaphone.fm/IHINL7082362864",
    "zoe": "https://feeds.megaphone.fm/ZOELIMITED9301524082",
    "model_health": "https://feeds.megaphone.fm/TMMOO1543465979",
    "rich_roll": "https://feeds.megaphone.fm/the-rich-roll-podcast",
    "dhru_purohit": "https://feeds.megaphone.fm/dhrupurohit",
}
import sys,glob,re,html,json,os
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
NS={"itunes":"http://www.itunes.com/dtds/podcast-1.0.dtd","content":"http://purl.org/rss/1.0/modules/content/"}
P={"lipid":r"\bapo ?b\b|apolipoprotein|\bldl\b|lp\(a\)|lipoprotein|cholesterol",
   "bp":r"blood pressure|hypertensi",
   "iso":r"\bisometric|\bwall[- ]?(sit|squat)s?\b|\bhand ?grip"}

def audit(data_dir):
    out={}
    for f in sorted(glob.glob(str(data_dir)+"/*.xml")):
        name=os.path.basename(f)[:-4]
        items=ET.parse(f).getroot().findall("./channel/item")
        c={"episodes":len(items),"lipid":0,"bp":0,"iso":0,"iso_bp_ctx":0,"iso_eps":[]}
        dates=[]
        for it in items:
            title=it.findtext("title") or ""
            d=" ".join(filter(None,[it.findtext("description"),it.findtext("content:encoded",namespaces=NS),it.findtext("itunes:summary",namespaces=NS)]))
            low=(title+" "+html.unescape(re.sub(r"<[^>]+>"," ",d))).lower()
            if it.findtext("pubDate"): dates.append(parsedate_to_datetime(it.findtext("pubDate")))
            for k in ("lipid","bp","iso"):
                if re.search(P[k],low): c[k]+=1
            for m in re.finditer(P["iso"],low):
                ctx=bool(re.search(P["bp"],low[max(0,m.start()-400):m.end()+400]))
                c["iso_eps"].append([title[:90],m.group(0),ctx])
                if ctx: c["iso_bp_ctx"]+=1; break
        dates.sort(); c["first"],c["last"]=str(dates[0].date()),str(dates[-1].date())
        out[name]=c
        print(f"{name:18s} eps={c['episodes']:5d} {c['first']}..{c['last']} lipid={c['lipid']:4d} bp={c['bp']:4d} iso={c['iso']:3d} iso_in_BP_context={c['iso_bp_ctx']}")
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir",type=pathlib.Path,required=True)
    ap.add_argument("--json",type=pathlib.Path)
    a=ap.parse_args(); a.data_dir.mkdir(parents=True,exist_ok=True)
    for name,url in FEEDS.items():
        p=a.data_dir/f"{name}.xml"
        if not p.exists():
            p.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=120).read())
    res=audit(a.data_dir)
    if a.json: a.json.write_text(json.dumps(res,indent=1))

if __name__=="__main__":
    main()
