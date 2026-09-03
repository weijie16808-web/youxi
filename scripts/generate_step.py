"""Generate a neutral AP214 STEP model in millimetres.

The exchange model contains the primary enclosure, front lens bezel/lens,
rear I/O panel and four feet as closed faceted B-reps.  This intentionally
uses only portable STEP constructs for compatibility with Creo import.
"""
from pathlib import Path

entities=[]
def add(s): entities.append(s); return len(entities) + 14
def point(x,y,z): return add(f"CARTESIAN_POINT('',({x:.4f},{y:.4f},{z:.4f}))")
def poly_solid(name, verts, faces):
    # closed shell of polygonal planar faces
    p=[point(*v) for v in verts]
    fs=[]
    for face in faces:
        loop=add("POLY_LOOP('',("+','.join(f'#{p[i]}' for i in face)+"))")
        bound=add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
        fs.append(add(f"FACE('',(#{bound}))"))
    shell=add("CLOSED_SHELL('',("+','.join(f'#{x}' for x in fs)+"))")
    return add(f"FACETED_BREP('{name}',#{shell})")
def box(name, xmin,xmax,ymin,ymax,zmin,zmax):
    v=[(xmin,ymin,zmin),(xmax,ymin,zmin),(xmax,ymax,zmin),(xmin,ymax,zmin),
       (xmin,ymin,zmax),(xmax,ymin,zmax),(xmax,ymax,zmax),(xmin,ymax,zmax)]
    f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    return poly_solid(name,v,f)
def cylinder(name,cx,cy,cz,r,depth,n=24,axis='y'):
    v=[]
    for d in (0,depth):
      for i in range(n):
        import math
        a=2*math.pi*i/n
        if axis=='y': v.append((cx+r*math.cos(a),cy+d,cz+r*math.sin(a)))
        else: v.append((cx+r*math.cos(a),cy+r*math.sin(a),cz+d))
    f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    for i in range(n): f.append((i,(i+1)%n,(i+1)%n+n,i+n))
    return poly_solid(name,v,f)

# Product envelope: X 214, Y 168, Z 88.  Main shell leaves 6 mm feet clearance.
items=[box('PROJECTOR_HOUSING',-107,107,-84,84,-38,44)]
# prominent front optical group; front points towards -Y
items += [cylinder('LENS_BEZEL',-46,-88,2,28,5), cylinder('OPTICAL_LENS',-46,-90,2,22,3)]
# front IR/focus window
items += [box('FRONT_SENSOR',48,68,-87,-84,-4,8)]
# back recessed connection panel + connector blocks
items += [box('REAR_IO_RECESS',-82,82,84,88,4,30), box('HDMI_PORT',-68,-48,88,91,12,22),
          box('USB_A_1',-37,-22,88,91,12,21), box('USB_A_2',-14,1,88,91,12,21),
          cylinder('AUDIO_JACK',18,88,17,4,3), cylinder('AV_JACK',42,88,17,4,3),
          cylinder('DC_IN',68,88,17,5,3)]
# feet + underside mount
for x in (-85,85):
 for y in (-65,65): items.append(cylinder('RUBBER_FOOT',x,y,-44,8,6,axis='z'))
items.append(cylinder('TRIPOD_MOUNT',0,0,-41,5,3,axis='z'))

header="""ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Mini LCD smart projector','AP214 exchange model'),'2;1');
FILE_NAME('mini-smart-projector.stp','2026-09-03T00:00:00',('Youxi'),('Youxi'),'','Creo compatible','');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN'));
ENDSEC;
DATA;
#1=APPLICATION_CONTEXT('automotive design');
#2=APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2001,#1);
#3=PRODUCT_CONTEXT('',#1,'mechanical');
#4=PRODUCT('MINI_SMART_PROJECTOR','MINI_SMART_PROJECTOR','214x168x88 mm mini LCD smart projector',(#3));
#5=PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE('1','',#4,.MADE.);
#6=PRODUCT_DEFINITION_CONTEXT('part definition',#1,'design');
#7=PRODUCT_DEFINITION('design','',#5,#6);
#8=PRODUCT_DEFINITION_SHAPE('','',#7);
#9=SHAPE_REPRESENTATION_CONTEXT(3,'3D context','');
#10=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.));
#11=(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.));
#12=(NAMED_UNIT(*)SOLID_ANGLE_UNIT()SI_UNIT($,.STERADIAN.));
#13=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.01),#10,'distance_accuracy_value','');
#14=GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#13))GLOBAL_UNIT_ASSIGNED_CONTEXT((#10,#11,#12))REPRESENTATION_CONTEXT('','');
"""
for i,e in enumerate(entities,15): pass
# entities currently IDs started at #1 invalid due header static. Regenerate offset.
body='\n'.join(f'#{i+15}={e};' for i,e in enumerate(entities))
shape_items=','.join(f'#{i}' for i in items)
footer=f"""
#{15+len(entities)}=SHAPE_REPRESENTATION('',({shape_items}),#14);
#{16+len(entities)}=SHAPE_DEFINITION_REPRESENTATION(#8,#{15+len(entities)});
ENDSEC;
END-ISO-10303-21;
"""
Path('assets/mini-smart-projector.stp').write_text(header+body+footer)
print('wrote assets/mini-smart-projector.stp')
