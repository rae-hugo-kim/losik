"""Build v3 feedback revisions while retaining explicitly approved performances."""
from pathlib import Path
import json
import hashlib
import tide_v2 as engine
from v3_preserve import preserve_sections

IDS=[slug.replace('-v2','-v3') for slug in engine.IDS]
KEEP={
 'tide':[],
 'lantern':['Breath','Verse 1','Refrain 1','Turnaround','Verse 2','Refrain 2','Weightless','Open Sky','Drift'],
 'window':[section[0] for section in engine.FORMS['window']],
 'north':['Seven Steps','Distance'],
 'rain':['First Drops','Afterglow']}


def generate():
    # Changing the shared engine must never silently change the retained v2 editions.
    for slug in engine.IDS:
        data=json.loads((engine.SKETCHES/(slug+'.json')).read_text())
        rebuilt,_=engine.compose(data)
        original=(engine.SKETCHES/(slug+'.mid')).read_bytes()
        assert rebuilt==original,('v2 reproduction changed',slug)
    print('V2 reproduction unchanged: 5/5',flush=True)
    for slug in IDS:
        data=json.loads((engine.SKETCHES/(slug+'.json')).read_text())
        old_slug=slug.replace('-v3','-v2')
        old_smf=(engine.SKETCHES/(old_slug+'.mid')).read_bytes()
        old_manifest=json.loads((engine.SKETCHES/(old_slug+'-manifest.json')).read_text())
        smf,manifest=engine.compose(data)
        kept=KEEP[data['style']]
        if kept:
            smf,manifest=preserve_sections(smf,manifest,old_smf,old_manifest,kept)
        manifest['preserved_from_v2']=kept
        manifest['revision_note']=data['revision_note']
        manifest['sha256_midi']=hashlib.sha256(smf).hexdigest()
        if data['style']=='rain':
            assert 200<=manifest['duration_seconds']<=210
        (engine.SKETCHES/(slug+'.mid')).write_bytes(smf)
        (engine.SKETCHES/(slug+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
        print(slug,manifest['bars'],round(manifest['duration_seconds'],3),[(t['role'],t['notes']) for t in manifest['tracks']],flush=True)


if __name__=='__main__':
    generate()
